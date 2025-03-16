# Generated by Django 5.1.5 on 2025-03-15 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ponde', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidatos',
            name='url_oferta_candidato',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ofertaslaborales',
            name='candidatos_cant',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ofertaslaborales',
            name='titulo_oferta',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
