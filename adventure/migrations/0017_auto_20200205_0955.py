# Generated by Django 3.0.3 on 2020-02-05 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0016_player_items_carrying'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='color',
            field=models.CharField(default='DEFAULT DESCRIPTION', max_length=50),
        ),
        migrations.AddField(
            model_name='player',
            name='glasses_color',
            field=models.CharField(default='DEFAULT DESCRIPTION', max_length=50),
        ),
        migrations.AddField(
            model_name='player',
            name='glasses_style',
            field=models.CharField(default='DEFAULT DESCRIPTION', max_length=50),
        ),
        migrations.AddField(
            model_name='player',
            name='hoodie_color',
            field=models.CharField(default='DEFAULT DESCRIPTION', max_length=50),
        ),
        migrations.AddField(
            model_name='player',
            name='pants_color',
            field=models.CharField(default='DEFAULT DESCRIPTION', max_length=50),
        ),
        migrations.AddField(
            model_name='player',
            name='pupil_color',
            field=models.CharField(default='DEFAULT DESCRIPTION', max_length=50),
        ),
        migrations.AddField(
            model_name='player',
            name='shoe_color',
            field=models.CharField(default='DEFAULT DESCRIPTION', max_length=50),
        ),
        migrations.AddField(
            model_name='player',
            name='skin_tone',
            field=models.CharField(default='DEFAULT DESCRIPTION', max_length=50),
        ),
    ]
