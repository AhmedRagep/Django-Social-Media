from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # id_user = models.IntegerField(blank=True, null=True)
    bio = models.TextField(blank=True)
    profileimg =  models.ImageField(upload_to='profile_images',default='blank-profile-picture.png')
    location = models.CharField(max_length=50, blank=True)
    

    class Meta:
        verbose_name = ("Profile")
        verbose_name_plural = ("Profiles")

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    

