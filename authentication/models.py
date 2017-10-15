from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from shop.models import Product ,Table
from collection.models import Collection
# Create your models here.
def rename(instance,name):
	return instance.user.username.replace('@','_')+'/profile/'+str(instance.created_at)+name

class Activity(models.Model):
	user       = models.ForeignKey(User       ,default=1)  
	product    = models.ForeignKey(Product    ,null=True,related_name="visited_product"   )
	table      = models.ForeignKey(Table      ,null=True,related_name="visited_table"     )
	collection = models.ForeignKey(Collection ,null=True,related_name="visited_collection")
	created_at = models.DateTimeField(default=datetime.now,blank=True)
	def __str__(self):
		if self.product:
			return self.product.name
		elif self.table:
			return self.table.name
		else:
			return self.collection.name 

class Profile(models.Model):
	user              = models.OneToOneField(User,default=1)
	url               = models.CharField(max_length=50, null=True, blank=True)
	job_title         = models.CharField(max_length=50, null=True, blank=True)
	picture           = models.ImageField(null=True,upload_to=rename)
	created_at        = models.DateTimeField(default=datetime.now, blank=True)
	wishedProducts    = models.ManyToManyField(Product,blank=True,related_name="wished_products")
	wishedCollections = models.ManyToManyField(Collection,blank=True,related_name="wished_collections")
	location          = models.CharField(max_length=50, null=True, blank=True)
	message           = models.CharField(max_length=250, null=True, blank=True)
	history           = models.ManyToManyField(Activity,blank=True,related_name="history")
	balance           = models.IntegerField(null=True,default=0) 
	#solde = models.IntegerField
	def __str__ (self):
		return self.user.username
