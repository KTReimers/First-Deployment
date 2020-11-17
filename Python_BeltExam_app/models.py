from django.db import models
import re
import bcrypt
from datetime import date
class userManager(models.Manager):
    def userValidation(self, postData):
        errors={}
        userEmailMatch=User.objects.filter(email=postData['email'])

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) ==0:
            errors['fnameReq'] = "First Name is required"
        elif len(postData['fname']) <2:
            errors['fnameLength'] = "First Name must be at least 2 characters long"
        if len(postData['lname']) ==0:
            errors['lnameReq'] = "Last Name is required"
        elif len(postData['lname']) <2:
            errors['lnameLength'] = "Last Name must be at least 2 characters long"
        if len(postData['email']) ==0:
            errors['emailReq'] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['emailPattern'] = "Invalid email address!"
        elif len(userEmailMatch) > 0:
            errors['emailTaken']= "Email is already registered"
        if len(postData['pw']) == 0:
            errors['pwReq']= "Password is required"
        elif len(postData['pw']) < 8:
            errors['pwLength'] = "Password must be at least 8 characters"
        if postData['pw'] != postData['cpw']:
            errors['cpwMatch'] = "Confirm Password does not match Password"
        return errors

    def LoginValidation(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        userEmailMatch=User.objects.filter(email=postData['email'])
        if not EMAIL_REGEX.match(postData['email']):
            errors['emailPattern'] = "Invalid email address!"
        elif len(userEmailMatch)==0:
            errors['email'] = "This email is not yet registered"
        elif not bcrypt.checkpw(postData['pw'].encode(), userEmailMatch[0].password.encode()):
            errors['pwWrong']="Incorrect Password"
        if len(postData['pw']) == 0:
            errors['pwReq']= "Password is required"
        elif len(postData['pw']) < 8:
            errors['pwLength'] = "Password must be at least 8 characters"
        return errors

class tripManager(models.Manager):
    def tripValidator(self, postData):
        errors = {}
        today= str(date.today())
        if len(postData['Job']) == 0:
            errors['JobLength'] = "Destination required"
        if len(postData['Plan']) ==0:
            errors['planLength'] = "Description required"
        if len(postData['Start']) == 0:
            errors['startLength']="Travel Date From required"
        elif postData['Start'] < today:
            errors['startInPast']= "Travel Date From cannot be in the past"
        if len(postData['End']) == 0:
            errors['startLength']="Travel Date To required"
        elif postData['End']< postData['Start']:
            errors['EndBeforeStart'] = "Travel Date To cannot be before Travel Date From"
        elif postData['End']< today:
            errors['EndInPast'] = "Travel Date To cannot be in the past"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length= 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= userManager()

class Destination(models.Model):
    job = models.CharField(max_length=255)
    travel_date_from = models.DateField()
    travel_date_to = models.DateField()
    plan = models.TextField()
    planned_trip = models.ForeignKey(User, related_name= 'trip_planned',on_delete = models.CASCADE)
    travelers = models.ManyToManyField(User, related_name="traveler")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= tripManager()
