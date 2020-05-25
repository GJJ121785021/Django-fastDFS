from django.db import models


class PersonalImage(models.Model):
    name = models.CharField(max_length=50, null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()


