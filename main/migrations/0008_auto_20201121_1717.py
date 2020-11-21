# Generated by Django 3.0.11 on 2020-11-21 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20201116_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborador',
            name='numero',
            field=models.CharField(max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='estado',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fecha_nacimiento',
            field=models.DateField(blank=True),
        ),
    ]
