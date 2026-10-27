from django.db import models
from django.conf import settings
class Importation(models.Model):
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    sha256 = models.CharField(max_length=64,unique=True)
    sheet = models.CharField(max_length=255)
    count = models.PositiveIntegerField()
    start = models.DateField()
    end = models.DateField()
    warnings = models.JSONField(default=list)
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'importación'
    def __str__(self): return self.filename
class Audit(models.Model):
    importation = models.ForeignKey(Importation,on_delete=models.CASCADE,related_name='audits')
    source_id = models.CharField(max_length=255)
    source_row = models.PositiveIntegerField()
    date = models.DateField(db_index=True)
    values = models.JSONField()
    original = models.JSONField()
    turno = models.CharField(max_length=255,blank=True,db_index=True)
    proceso = models.CharField(max_length=255,blank=True)
    linea = models.CharField(max_length=255,blank=True)
    maquina = models.CharField(max_length=255,blank=True)
    operador = models.CharField(max_length=255,blank=True,default='',db_index=True)
    inspector = models.CharField(max_length=255,blank=True)
    parte = models.CharField(max_length=255,blank=True)
    failures = models.PositiveIntegerField(default=0)
    detections = models.PositiveIntegerField(default=0)
    passes = models.PositiveIntegerField(default=0)
    missing = models.PositiveIntegerField(default=0)
    na = models.PositiveIntegerField(default=0)
    inconsistent = models.BooleanField(default=False)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['importation','source_id'],name='unique_id_per_import')]
        ordering = ['-date','-pk']
        verbose_name = 'auditoría'
