# Generated by Django 3.1.2 on 2020-10-20 10:58

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_QA', '0005_auto_20201018_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='body_text',
            field=ckeditor.fields.RichTextField(default=1),
            preserve_default=False,
        ),
    ]
