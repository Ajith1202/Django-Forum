# Generated by Django 3.1 on 2020-08-29 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20200820_1640'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CommentVote',
        ),
    ]