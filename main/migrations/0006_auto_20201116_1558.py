# Generated by Django 3.0.11 on 2020-11-16 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_pedido_tipo_comprobante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='tipo_comprobante',
            field=models.CharField(blank=True, choices=[('Boleta', 'Boleta'), ('Factura', 'Factura')], max_length=7, null=True),
        ),
    ]