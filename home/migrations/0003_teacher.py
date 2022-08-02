# Generated by Django 4.0.6 on 2022-08-01 23:15

import django.contrib.auth.models
from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_student"),
    ]

    operations = [
        migrations.CreateModel(
            name="Teacher",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("home.user",),
            managers=[
                ("teacher", django.db.models.manager.Manager()),
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
