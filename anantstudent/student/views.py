from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# student/views.py

from django.shortcuts import render, redirect
from .models import Student
import csv
import pandas as pd
from io import TextIOWrapper
from django.contrib import messages

def home(request):
    return render(request, 'html/home.html')

def admin_login(request):
    # Just dummy login page for now
    return render(request, 'html/admin_login.html')

def student_login(request):
    return render(request, 'html/student_login.html')

# def upload_students(request):
#     if request.method == 'POST':
#         csv_file = request.FILES['csv_file']

#         if not csv_file.name.endswith('.csv'):
#             messages.error(request, 'This is not a CSV file.')
#             return redirect('upload_students')
#                 # Decode with UTF-8 to support Marathi and Unicode


#         # Handle CSV upload carefully for big files
#         file_data = csv_file.read().decode("utf-8").splitlines()
#         reader = csv.DictReader(file_data)
        
#         students_to_create = []
#         for row in reader:
#             student = Student(
#                 sl_no=row.get('Sl. No.') or None,
#                 benf_no=row.get('BENF. NO') or '',
#                 aadhar_no=row.get('Aadhar No.') or '',
#                 name=row.get('Name of the student') or '',
#                 standard=row.get('Standard') or '',
#                 gender=row.get('Gender') or '',
#                 contact_no=row.get('Contact No.') or '',
#                 scheduled_tribes=row.get('Scheduled Tribes') or '',
#                 pvtgs=row.get('PVTGs') or '',
#                 certificate_issued=row.get('Certificate  Issued : Yes/ No') or '',
#                 digital_role=row.get('Digital Warrior / Commander') or '',
#                 school_name=row.get('Ashram School / Hostel Name') or '',
#                 phase=row.get('Phase 1') or '',
#                 district=row.get('Dahanu') or '',
#             )
#             students_to_create.append(student)

#         # Bulk create for speed
#         Student.objects.bulk_create(students_to_create)
#         messages.success(request, "Students uploaded successfully!")
#         return redirect('upload_students')

#     return render(request, 'html/upload_students.html')

def upload_students(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            messages.error(request, "Please upload a file.")
            return redirect('upload_students')

        file_name = uploaded_file.name.lower()

        students_to_create = []

        try:
            if file_name.endswith('.csv'):
                decoded_file = TextIOWrapper(uploaded_file.file, encoding='utf-8')
                reader = csv.DictReader(decoded_file)
            elif file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                reader = df.to_dict(orient='records')
            else:
                messages.error(request, "Unsupported file type. Upload CSV or Excel.")
                return redirect('upload_students')

            for row in reader:
                students_to_create.append(Student(
                    sl_no=None if pd.isna(row.get('Sl. No.')) else int(row.get('Sl. No.')),
                    benf_no=row.get('BENF. NO', ''),
                    aadhar_no=row.get('Aadhar No.', ''),
                    name=row.get('Name of the student', ''),
                    standard=row.get('Standard', ''),
                    gender=row.get('Gender', ''),
                    contact_no=row.get('Contact No.', ''),
                    scheduled_tribes=row.get('Scheduled Tribes', ''),
                    pvtgs=row.get('PVTGs', ''),
                    certificate_issued=row.get('Certificate  Issued : Yes/ No', ''),
                    digital_role=row.get('Digital Warrior / Commander', ''),
                    school_name=row.get('Ashram School / Hostel Name', ''),
                    phase=row.get('Phase', ''),
                    district=row.get('District', ''),
                ))

            Student.objects.bulk_create(students_to_create)
            messages.success(request, "Students uploaded successfully.")
            return redirect('upload_students')

        except Exception as e:
            messages.error(request, f"Error uploading file: {str(e)}")
            return redirect('upload_students')

    return render(request, 'html/upload_students.html')  # Your upload page template

def view_students(request):
    students = Student.objects.all()

    # Filters
    school_name = request.GET.get('school_name')
    standard = request.GET.get('standard')
    district = request.GET.get('district')

    if school_name:
        students = students.filter(school_name=school_name)
    if standard:
        students = students.filter(standard=standard)
    if district:
        students = students.filter(district=district)

    # Unique values for dropdowns
    school_names = Student.objects.values_list('school_name', flat=True).distinct()
    standards = Student.objects.values_list('standard', flat=True).distinct()
    districts = Student.objects.values_list('district', flat=True).distinct()

    return render(request, 'html/view_students.html', {
        'students': students,
        'school_names': school_names,
        'standards': standards,
        'districts': districts,
    })

def download_students(request):
    students = Student.objects.all()

    name = request.GET.get('name')
    standard = request.GET.get('standard')
    district = request.GET.get('district')

    if name:
        students = students.filter(name=name)
    if standard:
        students = students.filter(standard=standard)
    if district:
        students = students.filter(district=district)

    df = pd.DataFrame(list(students.values()))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=students.xlsx'

    df.to_excel(response, index=False)
    return response

