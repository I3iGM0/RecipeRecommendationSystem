from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

#Creates user models
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    date_of_birth = models.DateField(blank=False, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=True)
    steps = models.DecimalField(decimal_places=0, max_digits=20)
    calories = models.DecimalField(decimal_places=0, max_digits=20)
    deep = models.DecimalField(decimal_places=0, max_digits=20)
    light = models.DecimalField(decimal_places=0, max_digits=20)
    REM = models.DecimalField(decimal_places=0, max_digits=20)
    Wake = models.DecimalField(decimal_places=0, max_digits=20)
    Totaltime = models.DecimalField(decimal_places=0, max_digits=20)

    def __str__(self):
        return f'{self.user.username} Health Data'

    class Meta:
       ordering = ('-date',)
