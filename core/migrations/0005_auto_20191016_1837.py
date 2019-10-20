# Generated by Django 2.2.5 on 2019-10-16 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20191016_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='nasabah',
            name='balance',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]