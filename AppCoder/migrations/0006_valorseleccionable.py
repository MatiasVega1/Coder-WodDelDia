# Generated by Django 4.1.5 on 2023-02-03 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0005_task_valuelist'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValorSeleccionable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('valor', models.CharField(max_length=100)),
            ],
        ),
    ]
