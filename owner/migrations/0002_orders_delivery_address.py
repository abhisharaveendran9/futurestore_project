# Generated by Django 3.2.15 on 2022-09-28 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='delivery_address',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
