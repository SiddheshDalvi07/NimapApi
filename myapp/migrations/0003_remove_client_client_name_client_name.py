# Generated by Django 5.1 on 2024-08-31 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_client_name_client_client_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='client_name',
        ),
        migrations.AddField(
            model_name='client',
            name='name',
            field=models.CharField(default=1, max_length=100, verbose_name='client_name'),
            preserve_default=False,
        ),
    ]
