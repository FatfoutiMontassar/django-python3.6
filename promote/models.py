from django.db import models
from datetime import datetime

# Create your models here.

class Promote(models.Model):
	name        = models.CharField(max_length=200)
	product    = models.ForeignKey('shop.Product',blank=True,null=True,related_name='promote_products')
	collection = models.ForeignKey('collection.Collection',blank=True,null=True,related_name='promote_collections')
	startTime   = models.DateTimeField(default=datetime.now, blank=True)
	endTime     = models.DateTimeField(default=datetime.now, blank=True)
	cover       = models.IntegerField(null=True,default=0)
	maxCover    = models.IntegerField(null=True,default=0)
	activationChoices = (
	    (True, "Yes I acknowledge this"),
	    (False, "No, I do not like this")
	)
	isActive = models.NullBooleanField(choices = activationChoices,default=True)
	def __str__(self):
		return self.name

	def type(self):
		if(self.product):
			return "P"
		elif(self.collection):
			return "C"
		else:
			return "?"
