# Generated by Django 3.0.3 on 2020-04-19 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_message_chat_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instantreply',
            name='imessage',
        ),
        migrations.RemoveField(
            model_name='instantreply',
            name='user',
        ),
        migrations.RemoveField(
            model_name='usermsg',
            name='unread_message',
        ),
        migrations.DeleteModel(
            name='InstantMessage',
        ),
        migrations.DeleteModel(
            name='InstantReply',
        ),
        migrations.DeleteModel(
            name='Usermsg',
        ),
    ]
