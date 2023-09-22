# Generated by Django 4.2.5 on 2023-09-22 19:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_rename_name_record_title_alter_category_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 22, 14, 14, 21, 692146)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='color',
            field=models.CharField(default='#ff69b4', max_length=7),
        ),
    ]
