# Generated by Django 3.2.5 on 2021-07-14 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_question_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(default='', max_length=50),
        ),
    ]