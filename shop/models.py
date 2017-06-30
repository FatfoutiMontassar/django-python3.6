# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from datetime import datetime

from django.conf import  settings

# Create your models here.
def rename(instance,name):
	return instance.user.username.replace('@','_')+'/'+instance.name+'/'+str(instance.created_at)+name

def renameP(instance,name):
	return instance.store.user.username.replace('@','_')+'/'+instance.store.name + '/' + instance.name + '/' +str(instance.created_at)+name

class Store(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	img = models.ImageField(null=True,upload_to=rename)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	created_at = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	description = models.TextField()
	quantity = models.IntegerField(null=True,default=1)
	img = models.ImageField(null=True,upload_to=renameP)
	img1 = models.ImageField(null=True,upload_to=renameP)
	img2 = models.ImageField(null=True,upload_to=renameP)
	img3 = models.ImageField(null=True,upload_to=renameP)
	created_at = models.DateTimeField(default=datetime.now, blank=True)
	#storeName = models.CharField(max_length=200, blank=True, null=True)
	store = models.ForeignKey(Store, on_delete=models.CASCADE,null=True)
	categorie_choices = (
		('Vétement et accessoires','Vétement et accessoires')
		,('Bijoux','Bijoux')
		,('Founiture créatives','Founiture créatives')
		,('Mariages','Mariages')
		,('Maison','Maison')
		,('Enfant et bébé','Enfant et bébé'))
	categorie = models.CharField(max_length=200,null=True,choices = categorie_choices)
	activationChoices = (
	    (None, "I do not know now"),
	    (True, "Yes I acknowledge this"),
	    (False, "No, I do not like this")
	)
	isActive = models.NullBooleanField(choices = activationChoices)

	def __str__(self):
		return self.name

class Contact(models.Model):
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	subject = models.CharField(max_length=200)
	text = models.TextField()
	created_at = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return self.subject
