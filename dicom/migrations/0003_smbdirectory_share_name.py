# Generated by Django 2.1.2 on 2018-10-28 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dicom', '0002_smbdirectory'),
    ]

    operations = [
        migrations.AddField(
            model_name='smbdirectory',
            name='share_name',
            field=models.CharField(default=None, max_length=64),
            preserve_default=False,
        ),
    ]
