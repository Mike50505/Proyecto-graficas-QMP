from django.db import migrations


def backfill_operator(apps, schema_editor):
    Audit=apps.get_model('audits','Audit')
    alias=schema_editor.connection.alias
    pending=[]
    for audit in Audit.objects.using(alias).all().iterator(chunk_size=1000):
        value=audit.values.get('Nómina Operador','')
        audit.operador=str(value).strip() if value is not None else ''
        pending.append(audit)
        if len(pending)>=1000:
            Audit.objects.using(alias).bulk_update(pending,['operador'],batch_size=1000)
            pending=[]
    if pending:Audit.objects.using(alias).bulk_update(pending,['operador'],batch_size=1000)


class Migration(migrations.Migration):
    dependencies=[('audits','0002_audit_operador')]
    operations=[migrations.RunPython(backfill_operator,migrations.RunPython.noop)]
