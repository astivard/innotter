# Generated by Django 4.0.4 on 2022-06-22 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_alter_page_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='image',
        ),
        migrations.AddField(
            model_name='page',
            name='image_s3_path',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]