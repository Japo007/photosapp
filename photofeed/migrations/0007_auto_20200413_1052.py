# Generated by Django 3.0.1 on 2020-04-13 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photofeed', '0006_auto_20200413_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='originalFile',
            field=models.ImageField(default='download.png', upload_to=''),
        ),
    ]