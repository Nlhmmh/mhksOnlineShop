# Generated by Django 3.0.8 on 2020-07-26 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200726_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('both', 'Both')], default='both', max_length=20),
        ),
    ]
