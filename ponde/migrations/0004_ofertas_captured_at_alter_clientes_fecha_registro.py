# Generated by Django 5.1.5 on 2025-01-27 11:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visual', '0003_ofertas_page_alter_clientes_fecha_registro'),
    ]

    operations = [
        migrations.AddField(
            model_name='ofertas',
            name='captured_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='fecha_registro',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2025, 1, 27, 11, 19, 50, 154691)),
        ),
    ]
