# Generated by Django 4.1.7 on 2023-02-20 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0002_comentario_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wod',
            name='cantidad2',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='wod',
            name='cantidad3',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='wod',
            name='movimiento2',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movimientos2', to='AppCoder.movimiento'),
        ),
    ]
