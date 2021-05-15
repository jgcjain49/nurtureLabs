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
from nurtureApp.models import User
from nurtureApp.serializers import AdvisorSerializer, UserSerializer, BookingSerializer
from werkzeug.security import generate_password_hash, gen_salt, _hash_internal
from django.utils.decorators import decorator_from_middleware
import json
import jwt
# Create your views here.

jwtSecret = "KWNMRDPOUC"


def verifyToken(request):
    try:
        token = request.headers['Authorization']
        jwt.decode(token, jwtSecret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return JsonResponse({"success": False, "reason":  "Expired Token"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidSignatureError:
        return JsonResponse({"success": False, "reason": "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)


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
        token = jwt.encode(
            {"name": user_serializer.data["name"], "email": user_serializer.data["email"]}, jwtSecret, algorithm="HS256")

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


# @decorator_from_middleware(verifyToken)
@api_view(['POST'])
def ListAdvisor(request, user_id):
    return JsonResponse(True, status=status.HTTP_200_OK)


@api_view(['POST'])
def BookCall(req, user_id, advisor_id):
    random = [{
        'advisor_name': 'Antul',
        'pic': 'http://rna.some.com/2734',
        'advisor_id': '5esadjkfwe3',
        'booking_time': '15:33:00',
        'booking_id': '5rovwhbjk243',
        'user_id': user_id,
        'advisor_id': advisor_id
    }]
    return JsonResponse(random, safe=False)


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
