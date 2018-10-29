# Generated by Django 2.1.2 on 2018-10-29 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dicom', '0005_auto_20181029_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMBFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=500)),
                ('is_archived', models.BooleanField(default=False)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='file_set', to='dicom.SMBDirectory')),
            ],
            options={
                'verbose_name_plural': 'SMB Files',
            },
        ),
    ]
