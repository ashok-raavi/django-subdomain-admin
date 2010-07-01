
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from subdomains.models import Subdomain

class SubModel(models.Model):
    subdomain = models.ForeignKey(Subdomain,blank=True,null=True)
    
    class Meta:
        abstract = True

def set_permissions(sender, instance, created, **kwargs):
    '''For every permission added to the models inherited from SubModel, 
    grant the same permission to the group 'SubUser' ''' 
    if created:
        content_type = instance.content_type
        model = models.get_model(content_type.app_label, content_type.model)
        group = Group.objects.get_or_create(name='SubUser')[0]
        if model.__base__ == SubModel:
            group.permissions.add(instance)
            
models.signals.post_save.connect(set_permissions, sender=Permission)