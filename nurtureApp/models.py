from django.db import models

# Create your models here.


class Advisor(models.Model):
    name = models.CharField(max_length=20)
    pic = models.TextField()


class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    hash = models.TextField()
    salt = models.TextField()


class Booking(models.Model):
    user_id = models.CharField(max_length=20)
    advisor_id = models.CharField(max_length=20)
    advisor_name = models.CharField(max_length=20)
    advisor_pic = models.TextField()
    time = models.DateTimeField()
