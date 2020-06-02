# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Profile, User


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     print('We are in profile signal')
#     if created:
#         profile = Profile.objects.create(user=instance)
#         profile.name = getattr(instance, '_name', None)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
