# Generated by Django 3.0.3 on 2020-02-05 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0014_auto_20200204_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='room',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='adventure.Room'),
        ),
    ]
