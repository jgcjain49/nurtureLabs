from rest_framework import serializers
from nurtureApp.models import Advisor, User, Booking


class AdvisorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advisor
        depth = 1
        fields = ('id', 'name', 'pic')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        depth = 1
        fields = ('id', 'name', 'email', 'hash', 'salt')


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        depth = 1
        fields = ('id', 'advisor_id', 'advisor_name',
                  'advisor_pic', 'time', 'user_id')
