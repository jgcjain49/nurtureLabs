import re
from asgiref.sync import sync_to_async
from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.core import serializers
from nurtureApp.models import User, Advisor, Booking
from nurtureApp.serializers import AdvisorSerializer, UserSerializer, BookingSerializer
from werkzeug.security import generate_password_hash, gen_salt, _hash_internal
from django.utils.decorators import decorator_from_middleware
from nurtureApp.middleware.AuthenticationNSS import AuthenticationMiddleware
import json
import jwt
# Create your views here.

jwtSecret = "KWNMRDPOUC"


@api_view(['POST'])
def CreateAdvisor(request):
    advisor_data = JSONParser().parse(request)
    if not('name' in advisor_data.keys() and 'pic' in advisor_data.keys()):
        return JsonResponse({"success": False, "message": "Missing Parameters"}, status=status.HTTP_400_BAD_REQUEST)

    advisor_serializer = AdvisorSerializer(data=advisor_data)
    if advisor_serializer.is_valid():
        advisor_serializer.save()
        return JsonResponse(advisor_serializer.data, status=status.HTTP_200_OK)
    return JsonResponse(advisor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def CreateUser(request):
    user_data = JSONParser().parse(request)
    if not('name' in user_data.keys() and 'email' in user_data.keys() and 'password' in user_data.keys()):
        return JsonResponse({"success": False, "message": "Missing Parameters"}, status=status.HTTP_400_BAD_REQUEST)

    oldUser = getUser(user_data['email'])
    if oldUser:
        return JsonResponse({"success": False, "message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    salt = gen_salt(6)
    passwordHash = getHash(salt=salt, password=user_data["password"])

    user_data["hash"] = passwordHash[0]
    user_data["salt"] = salt

    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user_serializer.save()
        token = generateToken(payload={
                              "name": user_serializer.data["name"], "email": user_serializer.data["email"]})

        return JsonResponse({"token": token, "user_id": user_serializer.data['id']}, status=status.HTTP_200_OK, safe=False)
    return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def LoginUser(request):
    login_data = JSONParser().parse(request)

    if not('email' in login_data.keys() and 'password' in login_data.keys()):
        return JsonResponse({"success": False, "message": "Missing Parameters"}, status=status.HTTP_400_BAD_REQUEST)

    oldUser = getUser(login_data['email'])
    if not(oldUser):
        return JsonResponse({"success": False, "message": "No User Found. Please register first."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(email=login_data['email'])
    user_serializer = UserSerializer(user)
    passwordHash = getHash(
        salt=user_serializer.data['salt'], password=login_data['password'])

    token = generateToken(payload={
                          "name": user_serializer.data["name"], "email": user_serializer.data["email"]})

    if passwordHash[0] != user_serializer.data['hash']:
        return JsonResponse({"success": False, "message": "Incorrect Password"}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"token": token, "user_id": user_serializer.data['id']}, status=status.HTTP_200_OK)


@api_view(['GET'])
def ListAdvisor(request, user_id):
    advisor_data = Advisor.objects.all()
    return JsonResponse({"success": True, "data": list(advisor_data.values())}, status=status.HTTP_200_OK)


@api_view(['POST'])
def BookCall(request, user_id, advisor_id):
    advisor_data = Advisor.objects.get(id=advisor_id)

    booking_data = {
        'advisor_name': advisor_data.name,
        'advisor_pic': advisor_data.pic,
        'time': request.data['time'],
        'user_id': user_id,
        'advisor_id': advisor_id
    }

    booking = BookingSerializer(data=booking_data)
    if booking.is_valid():
        booking.save()
        return JsonResponse(booking.data, status=status.HTTP_200_OK)
    return JsonResponse(booking.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ListBooking(request, user_id):
    booking_data = Booking.objects.all()
    filterData = Booking.objects.filter(user_id=user_id)
    print(filterData)
    return JsonResponse({"success": True, "data": list(filterData.values())}, status=status.HTTP_200_OK, safe=False)


def getUser(email):
    user = User.objects.filter(email=email)
    if user.exists():
        return User.objects.get(email=email)
    else:
        return False


def generateToken(payload):
    return jwt.encode(payload, jwtSecret, algorithm="HS256")


def getHash(salt, password):
    return _hash_internal(
        method="pbkdf2:sha1:100", salt=salt, password=password)
