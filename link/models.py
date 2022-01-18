from django.db import models

class User(models.Model):
    chat_id = models.CharField(max_length=100,verbose_name="Chat ID: ")
    full_name = models.CharField(max_length=100,verbose_name="Full Name: ")
    username = models.CharField(max_length=100,verbose_name="Username: ")

class Link(models.Model):
    link = models.CharField(max_length=100, verbose_name="Link: ", null=True, blank=True)