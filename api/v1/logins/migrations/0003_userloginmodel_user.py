# Generated by Django 4.0.6 on 2022-09-30 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('logins', '0002_alter_userloginmodel_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userloginmodel',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]