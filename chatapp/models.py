"""from django.db import models
from django.contrib.auth.models import User
Create your models here.
class userh(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    
class Messages(models.Model):
    message = models.CharField(max_length = 500)
    user    = models.ForeignKey(User,on_delete=models.CASCADE)    """
    
# models.py

from django.db import models

class ChatMessage(models.Model):
    username = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.message}"
    
         
