from django.db import models

# Create your models here.
import re
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

Appointments_state=(('canceld by doctor','canceld by doctor'),('canceld','canceld'),('in processing','in processing'),('missed','missed'),('finished','finished'),('reschedule','reschedule'),('approved','approved'))

# egyptian phone number validation
def validate_egyptian_number(value):
    if not any(re.match(pattern, value) for pattern in [r"011+[0-9]{8}", r"012+[0-9]{8}", r"015+[0-9]{8}",r"010+[0-9]{8}"]):
        raise ValidationError(
            _('%(value)s is not a valid egyptian number'),
            params={'value': value},
        )

def image_upload(instance, imagename):
    extension = imagename.split(".")[1]
    return "users/%s.%s" % (instance.user.id, extension)

# Create your models here.
class Profile(models.Model):
    # connect with auth_user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11,null=True,validators=[validate_egyptian_number],error_messages ={
                    "required":"this is not a valid egyptian number"
                    })
    profile_picture = models.ImageField(upload_to=image_upload,null=True)
    birth_date = models.DateField(null=True,blank=True)
    facebook_profile = models.URLField(null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    # todo: projects

    def __str__(self):
        return str(self.user)
    
    
class Appointments(models.Model):
    user=models.ForeignKey(User, related_name='Appiontment_owner', on_delete=models.CASCADE)
    date=models.DateField(null=False)
    time=models.TimeField(auto_now=False, auto_now_add=False,null=False)
    state=models.CharField(max_length=20 , choices=Appointments_state , null=True)