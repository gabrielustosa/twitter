# Generated by Django 4.0.6 on 2022-08-20 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0003_alter_tweetaction_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetaction',
            name='action',
            field=models.CharField(choices=[('RT', 'Retweet'), ('LK', 'Like'), ('CM', 'Comment')], max_length=2),
        ),
    ]