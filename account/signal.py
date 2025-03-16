
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import UserAccount, UserProfile

#according to django documentation says we should handle signal in separate file
@receiver(post_save, sender=UserAccount)#decorator to connect to the sender
def  post_save_create_profile_receiver(sender, instance, created, **kwargs):# the created will return true when the profile is created false we

    if created:
        UserProfile.objects.create(user=instance)
     
    else:
        try:

            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)
           
# post_save.connect(post_save_create_profile_receiver, sender=User)
#------------------this is about the post_save signal---------------------------  ;
@receiver(pre_save, sender=UserAccount)#decorator to connect to the sender
def pre_save(sender, instance, **kwargs):
    pass #pre save doe