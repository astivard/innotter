# Generated by Django 4.0.5 on 2022-06-16 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_role"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="image_s3_path",
        ),
        migrations.AddField(
            model_name="user",
            name="image",
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to="users/%Y/%m/%d/"),
        ),
    ]
