# Generated by Django 3.0.3 on 2020-02-05 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0015_auto_20200204_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='items_carrying',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='adventure.Item'),
        ),
    ]
