from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



category_list = (
    ('Software', 'Software'),
    ('Hardware', 'Hardware'),
    ('Liveware', 'Liveware'),
    ('Server', 'Server'),
)

class Zones(models.Model):
    class Meta:
        verbose_name_plural = "Zones"
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name


class Branches(models.Model):
    class Meta:
        verbose_name_plural = "Branches"
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name

class Expert(models.Model):
    expert = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.expert.username

class Ticket(models.Model):

    zone = models.ForeignKey(Zones, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE)
    issue = models.CharField(max_length=100, blank=False, null=False)
    status = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(default=timezone.now)
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, blank=False, null=False)
    image = models.ImageField(
        upload_to='ticket_pics', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    anydesk = models.CharField(max_length=9, blank=True, null=True)
    assigned_to = models.ForeignKey(Expert, on_delete=models.CASCADE, null=True)
    category = models.CharField(
        max_length=100, choices=category_list, default=category_list[0][0])  # admin
    verification = models.BooleanField(blank=True, null=True)  # admin
    date_closed = models.DateTimeField(null=True, blank=True)  # admin
    documentation = models.TextField(blank=True)

    def __str__(self):
        return self.issue
    
    def get_absolute_url(self):
        return reverse('my_tickets', kwargs={'username': self.submitter.username})
