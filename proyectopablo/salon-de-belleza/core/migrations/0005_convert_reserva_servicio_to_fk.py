"""Convertir Reserva.servicio (CharField choices) a ForeignKey a Servicio.

Este migration hace los pasos seguros en SQLite:
1) Añade un campo temporal `servicio_fk` (FK nullable).
2) Mapea los valores antiguos de `servicio` (strings) a instancias de
   `Servicio` (busca por nombre o crea si hace falta) y guarda en `servicio_fk`.
3) Elimina el antiguo campo `servicio` (CharField).
4) Renombra `servicio_fk` a `servicio`.

NOTA: Esta migración preserva los datos existentes y deja `turno` como
campo nullable (se puede enlazar manualmente si se desea).
"""
from django.db import migrations, models


def forwards(apps, schema_editor):
    Reserva = apps.get_model('core', 'Reserva')
    Servicio = apps.get_model('core', 'Servicio')
    db_alias = schema_editor.connection.alias

    # Map values from choices to readable labels we expect en Servicio.nombre
    mapping = {
        'Unas': 'Uñas',
        'Corte_Pelo': 'Corte de Pelo',
        'Tintura': 'Tintura',
    }

    for reserva in Reserva.objects.using(db_alias).all():
        old = getattr(reserva, 'servicio', None)
        if not old:
            continue
        label = mapping.get(old, old)

        # Buscar un Servicio existente que coincida por nombre (case-insensitive)
        servicio_obj = Servicio.objects.using(db_alias).filter(nombre__iexact=label).first()
        if not servicio_obj:
            servicio_obj = Servicio.objects.using(db_alias).create(nombre=label)

        reserva.servicio_fk = servicio_obj
        reserva.save()


def backwards(apps, schema_editor):
    # No intentamos revertir automáticamente el mapeo; dejamos el campo char
    # tal como estaba (reversión manual si es necesario).
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_contacto'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='servicio_fk',
            field=models.ForeignKey(to='core.servicio', null=True, blank=True, on_delete=models.SET_NULL),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name='reserva',
            name='servicio',
        ),
        migrations.RenameField(
            model_name='reserva',
            old_name='servicio_fk',
            new_name='servicio',
        ),
    ]
