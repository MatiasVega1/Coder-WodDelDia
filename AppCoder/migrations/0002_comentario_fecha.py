# Generated by Django 4.1.7 on 2023-02-20 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='fecha',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]
