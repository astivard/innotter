# Generated by Django 4.0.5 on 2022-06-13 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("user", "User"), ("moderator", "Moderator"), ("admin", "Admin")], default="user", max_length=9
            ),
        ),
    ]
