# Generated by Django 2.2.5 on 2019-10-16 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='nasabah',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
