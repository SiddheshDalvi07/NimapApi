# Generated by Django 5.1 on 2024-08-31 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='name',
        ),
        migrations.AddField(
            model_name='client',
            name='client_name',
            field=models.CharField(default='', max_length=100, verbose_name='client_name'),
        ),
    ]
