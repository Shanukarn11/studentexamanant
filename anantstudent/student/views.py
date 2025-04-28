from django.shortcuts import render

# Create your views here.

# student/views.py

from django.shortcuts import render, redirect
from .models import Student
import csv
from django.contrib import messages

def home(request):
    return render(request, 'html/home.html')

def admin_login(request):
    # Just dummy login page for now
    return render(request, 'html/admin_login.html')

def student_login(request):
    return render(request, 'student_login.html')

def upload_students(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file.')
            return redirect('upload_students')

        # Handle CSV upload carefully for big files
        file_data = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(file_data)
        
        students_to_create = []
        for row in reader:
            student = Student(
                sl_no=row.get('Sl. No.') or None,
                benf_no=row.get('BENF. NO') or '',
                aadhar_no=row.get('Aadhar No.') or '',
                name=row.get('Name of the student') or '',
                standard=row.get('Standard') or '',
                gender=row.get('Gender') or '',
                contact_no=row.get('Contact No.') or '',
                scheduled_tribes=row.get('Scheduled Tribes') or '',
                pvtgs=row.get('PVTGs') or '',
                certificate_issued=row.get('Certificate  Issued : Yes/ No') or '',
                digital_role=row.get('Digital Warrior / Commander') or '',
                school_name=row.get('Ashram School / Hostel Name') or '',
                phase=row.get('Phase 1') or '',
                district=row.get('Dahanu') or '',
            )
            students_to_create.append(student)

        # Bulk create for speed
        Student.objects.bulk_create(students_to_create)
        messages.success(request, "Students uploaded successfully!")
        return redirect('upload_students')

    return render(request, 'upload_students.html')

def view_students(request):
    students = Student.objects.all()
    return render(request, 'view_students.html', {'students': students})

