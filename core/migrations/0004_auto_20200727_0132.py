# Generated by Django 3.0.8 on 2020-07-26 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200727_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Clothing', 'Clothing'), ('Beauty', 'Beauty'), ('Jewellery', 'Jewellery')], max_length=20),
        ),
    ]