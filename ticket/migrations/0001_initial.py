# Generated by Django 4.1.6 on 2023-02-16 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Branches",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
            ],
            options={
                "verbose_name_plural": "Branches",
            },
        ),
        migrations.CreateModel(
            name="Expert",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "expert",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Zones",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
            ],
            options={
                "verbose_name_plural": "Zones",
            },
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("issue", models.CharField(max_length=100)),
                ("status", models.BooleanField(default=False)),
                (
                    "date_submitted",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("phone", models.CharField(max_length=12)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="ticket_pics"),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("anydesk", models.CharField(blank=True, max_length=9, null=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Software", "Software"),
                            ("Hardware", "Hardware"),
                            ("Liveware", "Liveware"),
                            ("Server", "Server"),
                        ],
                        default="Software",
                        max_length=100,
                    ),
                ),
                ("verification", models.BooleanField(blank=True, null=True)),
                ("date_closed", models.DateTimeField(blank=True, null=True)),
                ("documentation", models.TextField(blank=True)),
                (
                    "assigned_to",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ticket.expert",
                    ),
                ),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ticket.branches",
                    ),
                ),
                (
                    "submitter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "zone",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ticket.zones"
                    ),
                ),
            ],
        ),
    ]
