from django.db import models

# Create your models here.

from django.db import models

class Student(models.Model):
    sl_no = models.IntegerField(null=True)
    benf_no = models.CharField(max_length=150, blank=True, null=True)
    aadhar_no = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)  # Increased for long names
    standard = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    scheduled_tribes = models.CharField(max_length=200, blank=True, null=True)
    pvtgs = models.CharField(max_length=200, blank=True, null=True)
    certificate_issued = models.CharField(max_length=20, blank=True, null=True)
    digital_role = models.CharField(max_length=500, blank=True, null=True)  # Sometimes multiple roles
    school_name = models.CharField(max_length=500, blank=True, null=True)   # Ashramshala names can be long
    phase = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

