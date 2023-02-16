from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')

    def __str__(self) -> str:
        return f"{self.user.username}'s Account"
    
    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)

        image = Image.open(self.image.path)
        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)