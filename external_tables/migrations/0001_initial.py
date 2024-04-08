# Generated by Django 3.2.6 on 2022-05-06 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_column', models.CharField(default='ID', max_length=128)),
                ('id_field', models.CharField(default='id', max_length=128)),
                ('key', models.CharField(max_length=255)),
                ('sheet_name', models.CharField(max_length=255)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]