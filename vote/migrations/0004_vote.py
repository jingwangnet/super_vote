# Generated by Django 3.2.5 on 2021-07-14 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_alter_question_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='')),
            ],
        ),
    ]