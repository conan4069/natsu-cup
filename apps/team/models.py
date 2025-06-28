from django.db import models

# Create your models here.

class Player (models.Model):
  name = models.CharField(max_length=64, blank=False, null=False)
  last_name = models.CharField(max_length=120)
  img = models.ImageField(upload_to='player/', null=True)

  def __str__(self):
    return f'{self.name} {self.last_name}'

class Team (models.Model):
  name = models.CharField(max_length=100, blank=False, null=False, unique=True)
  img = models.ImageField(upload_to='teams/', null=True)

  def __str__(self):
    return f'{self.name}'