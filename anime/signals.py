# les signaux permettent de simplifier notre code
# permet d'integrer les modifications (creation ou changement de profil)

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs): # fonction de reception pour la creation de la photo de profile (faire correspondre la photo a un utilisateur)

    if created:
        Profile.objects.create(user=instance)



@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):    # fonction de reception pour la sauvegarde du profil
    instance.profile.save()







