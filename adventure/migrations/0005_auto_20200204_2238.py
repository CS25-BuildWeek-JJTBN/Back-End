# Generated by Django 3.0.3 on 2020-02-04 22:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0004_player_visited_rooms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='DEFAULT DESCRIPTION', max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='items_carrying',
            field=models.ManyToManyField(to='adventure.Item'),
        ),
        migrations.AddField(
            model_name='room',
            name='items',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='adventure.Item'),
            preserve_default=False,
        ),
    ]
