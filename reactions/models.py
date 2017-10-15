from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.conf import  settings


# Create your models here.

class Reaction(models.Model):
	user            = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	product         = models.ForeignKey('shop.Product',null=True,blank=True,related_name='reaction_product')
	table           = models.ForeignKey('shop.Table',null=True,blank=True,related_name='reaction_table')
	collection      = models.ForeignKey('collection.Collection',null=True,blank=True,related_name='reaction_collection')
	created_at      = models.DateTimeField(default=datetime.now, blank=True)
	promote         = models.ForeignKey('promote.Promote',null=True,blank=True,related_name='reaction_collection')

	
	NORMAL      = 'normal'
	SMILE       = 'smile'
	LOVE        = 'love'
	WISH        = 'wish'

	LIKE        = 'like'
	DISLIKE     = 'dislike'

	CHOICES = (
		(NORMAL, NORMAL),
		(SMILE, SMILE),
		(LOVE, LOVE),
		(WISH, WISH),
		(LIKE, LIKE),
		(DISLIKE, DISLIKE),
	)
	reaction_type    = models.CharField(choices = CHOICES,default="Like",max_length=200)
	def __str__(self):
		thing = "x"
		if(self.product):
			thing = str(self.product.name)
		elif(self.table):
			thing = str(self.table.name)
		else:
			thing = str(self.collection.name)

		return str(self.user.username) + " has reacted to " + thing
