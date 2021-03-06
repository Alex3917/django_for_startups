# Generated by Django 3.1.6 on 2021-02-09 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210208_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailaddress',
            name='user_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='nfc_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='nfkc_name',
            field=models.CharField(blank=True, db_index=True, max_length=20),
        ),
    ]
