# Generated by Django 2.2.5 on 2019-10-29 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets2text', '0002_auto_20190710_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweettextcompilation',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
