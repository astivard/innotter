# Generated by Django 4.0.5 on 2022-06-06 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Page",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80)),
                ("uuid", models.CharField(max_length=30, unique=True)),
                ("description", models.TextField()),
                ("image", models.URLField(blank=True, null=True)),
                ("is_private", models.BooleanField(default=False)),
                ("unblock_date", models.DateTimeField(blank=True, null=True)),
                ("is_blocked", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=30, unique=True)),
            ],
        ),
    ]
