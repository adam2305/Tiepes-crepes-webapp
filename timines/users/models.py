from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    chambre = models.TextField(null=True)

class Commande(models.Model):
    TOPPING =(
        ('R','Nature'),
        ('S','sucre'),
        ('N','nutella'),
        ('C','combinaison')
    )
    user = models.TextField(null=False)
    produit = models.PositiveIntegerField(null=False,default=0,validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    topping = models.TextField(null=False,choices=TOPPING)
    adresse = models.TextField(null=False)
    delivered = models.BooleanField(null=False,default=False)
    remarque = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now())
    
    def __unicode__(self):
        return self.name
