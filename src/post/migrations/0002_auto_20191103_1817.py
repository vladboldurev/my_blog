# Generated by Django 2.2.6 on 2019-11-03 18:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.UUID('9490b797-2d51-424b-8f48-b4d60e50049d'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['id'], name='id_index'),
        ),
    ]
