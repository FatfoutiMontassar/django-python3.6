from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
def rename(instance,name):
	return 'profile_picture/'+instance.user.username + '/'+str(instance.created_at)+name


class Profile(models.Model):
    user = models.OneToOneField(User,default=1)
    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField(null=True,upload_to=rename)
    created_at = models.DateTimeField(default=datetime.now, blank=True)


    def __str__(self):
        return self.user.username
