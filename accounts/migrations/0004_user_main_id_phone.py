# Generated by Django 2.1.3 on 2018-11-20 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_main_id_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='main_id_phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
