# Generated by Django 2.2.6 on 2019-11-24 17:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_auto_20191124_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.UUID('df42f71e-75fa-4d0b-952a-6efa3d8ed016'), editable=False, primary_key=True, serialize=False),
        ),
    ]
