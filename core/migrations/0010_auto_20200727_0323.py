# Generated by Django 3.0.8 on 2020-07-26 18:23

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200727_0321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, quality=99, size=[700, 600], upload_to='images'),
        ),
    ]
