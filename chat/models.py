from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=200 , blank=False)
    
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL  , null=True)
    room = models.ForeignKey(Room , null=True , on_delete=models.CASCADE )
    body = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body
    
    

    class Meta:
        ordering = ['created']    
