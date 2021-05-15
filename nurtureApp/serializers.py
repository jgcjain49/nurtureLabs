from rest_framework import serializers
from nurtureApp.models import Advisor, User, Booking


class AdvisorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advisor
        fields = ('id', 'name', 'pic')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'hash', 'salt')


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ('id', 'advisor_id', 'time', 'user_id')
