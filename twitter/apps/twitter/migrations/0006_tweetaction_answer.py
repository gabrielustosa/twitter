# Generated by Django 4.0.6 on 2022-08-22 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0005_alter_tweetaction_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetaction',
            name='answer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='twitter.tweet'),
            preserve_default=False,
        ),
    ]
