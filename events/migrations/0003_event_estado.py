# Generated by Django 5.1.4 on 2024-12-15 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_duracion'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='estado',
            field=models.CharField(choices=[('activo', 'Activo'), ('cancelado', 'Cancelado'), ('finalizado', 'Finalizado')], default='activo', max_length=10),
        ),
    ]