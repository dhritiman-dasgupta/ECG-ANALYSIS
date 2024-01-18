# healthapp/models.py
from django.db import models

class Patient(models.Model):
    patient_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    device_id = models.CharField(max_length=50, unique=True)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ecgdata(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=50)
    scan_data = models.JSONField()
    EventProcessedUtcTime = models.DateTimeField()

    def __str__(self):
        return f"Scan for {self.patient} ({self.device_id})"

class Device(models.Model):
    device_id = models.CharField(max_length=50, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.device_id
