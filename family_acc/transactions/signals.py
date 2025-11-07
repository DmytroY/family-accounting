from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Transaction

@receiver(post_save, sender=Transaction)
def transaction_created(sender, instance, created, **kwargs):
    if(created):
        print(f"--DY-- new transaction created by {instance.created_by}")
        if instance.created_by and hasattr(instance.created_by, "profile"):
            instance.family = instance.created_by.profile.family
            instance.save(update_fields=["family"])  # ! treat of recurtion 