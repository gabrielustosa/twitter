# Generated by Django 4.0.6 on 2022-08-23 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_created_user_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(default='Presente professor camisa 13'),
            preserve_default=False,
        ),
    ]