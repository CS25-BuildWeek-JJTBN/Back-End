# Generated by Django 3.0.3 on 2020-02-05 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0018_room_start'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='items_carrying',
        ),
        migrations.AddField(
            model_name='item',
            name='player',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='adventure.Player'),
        ),
    ]
