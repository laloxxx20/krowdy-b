# Generated by Django 2.1.3 on 2018-11-20 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20181120_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='main_id_email',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]