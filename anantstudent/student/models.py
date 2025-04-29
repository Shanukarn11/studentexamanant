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

class BaselineResult(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    standard = models.CharField(max_length=20,blank=True, null=True)

    # Questions Q1 to Q30
    q1 = models.IntegerField( blank=True, null=True)
    q2 = models.IntegerField( blank=True, null=True)
    q3 = models.IntegerField( blank=True, null=True)
    q4 = models.IntegerField( blank=True, null=True)
    q5 = models.IntegerField( blank=True, null=True)
    q6 = models.IntegerField( blank=True, null=True)
    q7 = models.IntegerField( blank=True, null=True)
    q8 = models.IntegerField( blank=True, null=True)
    q9 = models.IntegerField( blank=True, null=True)
    q10 = models.IntegerField( blank=True, null=True)
    q11 = models.IntegerField( blank=True, null=True)
    q12 = models.IntegerField( blank=True, null=True)
    q13 = models.IntegerField( blank=True, null=True)
    q14 = models.IntegerField( blank=True, null=True)
    q15 = models.IntegerField( blank=True, null=True)
    q16 = models.IntegerField( blank=True, null=True)
    q17 = models.IntegerField( blank=True, null=True)
    q18 = models.IntegerField( blank=True, null=True)
    q19 = models.IntegerField( blank=True, null=True)
    q20 = models.IntegerField( blank=True, null=True)
    q21 = models.IntegerField( blank=True, null=True)
    q22 = models.IntegerField( blank=True, null=True)
    q23 = models.IntegerField( blank=True, null=True)
    q24 = models.IntegerField( blank=True, null=True)
    q25 = models.IntegerField( blank=True, null=True)
    q26 = models.IntegerField( blank=True, null=True)
    q27 = models.IntegerField( blank=True, null=True)
    q28 = models.IntegerField( blank=True, null=True)
    q29 = models.IntegerField( blank=True, null=True)
    q30 = models.IntegerField( blank=True, null=True)

    total_marks = models.IntegerField(blank=True, null=True)
    phase = models.CharField(max_length=100,blank=True, null=True)