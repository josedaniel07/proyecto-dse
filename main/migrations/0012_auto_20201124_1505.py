# Generated by Django 3.0.11 on 2020-11-24 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20201124_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='preferencias',
        ),
        migrations.AddField(
            model_name='cliente',
            name='preferencias',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Categoria'),
        ),
    ]
