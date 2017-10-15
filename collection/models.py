from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.conf import  settings

# Create your models here.
def renameC(instance,name):
	return instance.user.username.replace('@','_')+'/collections/'+instance.name+'/'+str(instance.created_at)+name

class Collection(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    name         = models.CharField(max_length=200)
    description  = models.TextField()
    image        = models.ImageField(null=True,upload_to=renameC)
    created_at   = models.DateTimeField(default=datetime.now, blank=True)
    products     = models.ManyToManyField('shop.Product',blank=True,related_name='collecstions_products')
    activationChoices = (
	    (None, "I do not know now"),
	    (True, "Yes I acknowledge this"),
	    (False, "No, I do not like this") )
    isActive     = models.NullBooleanField(choices = activationChoices,default=True)

    def __str__(self):
        return self.name
