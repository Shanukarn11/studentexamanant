from django.shortcuts import render
from django.http import HttpResponse
from .models import BaselineResult
from django.core.paginator import Paginator


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


def upload_baseline(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            messages.error(request, "No file uploaded.")
            return redirect('upload_baseline')

        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(uploaded_file)
            else:
                messages.error(request, "Please upload a CSV or Excel file.")
                return redirect('upload_baseline')

            df = df.where(pd.notnull(df), None)

            baseline_entries = []
            for _, row in df.iterrows():
                baseline_entries.append(BaselineResult(
                    name=row.get('Name of the student'),
                    standard=row.get('Standard'),
                    q1=row.get('Q.1'),
                    q2=row.get('Q.2'),
                    q3=row.get('Q.3'),
                    q4=row.get('Q.4'),
                    q5=row.get('Q.5'),
                    q6=row.get('Q.6'),
                    q7=row.get('Q.7'),
                    q8=row.get('Q.8'),
                    q9=row.get('Q.9'),
                    q10=row.get('Q.10'),
                    q11=row.get('Q.11'),
                    q12=row.get('Q.12'),
                    q13=row.get('Q.13'),
                    q14=row.get('Q.14'),
                    q15=row.get('Q.15'),
                    q16=row.get('Q.16'),
                    q17=row.get('Q.17'),
                    q18=row.get('Q.18'),
                    q19=row.get('Q.19'),
                    q20=row.get('Q.20'),
                    q21=row.get('Q.21'),
                    q22=row.get('Q.22'),
                    q23=row.get('Q.23'),
                    q24=row.get('Q.24'),
                    q25=row.get('Q.25'),
                    q26=row.get('Q.26'),
                    q27=row.get('Q.27'),
                    q28=row.get('Q.28'),
                    q29=row.get('Q.29'),
                    q30=row.get('Q.30'),
                    total_marks=row.get('Total Marks'),
                    phase=row.get('Phase'),
                ))

            BaselineResult.objects.bulk_create(baseline_entries)

            messages.success(request, "Baseline results uploaded successfully!")

        except Exception as e:
            messages.error(request, f"Error processing file: {e}")

        return redirect('upload_baseline')

    # This is the response when method is GET
    return render(request, 'html/upload_baseline.html')


def view_baseline(request):
    standard = request.GET.get('standard')
    phase = request.GET.get('phase')

    results = BaselineResult.objects.all().order_by('-total_marks')

    if standard:
        results = results.filter(standard=standard)
    if phase:
        results = results.filter(phase=phase)
    questions=['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15',
 'q16', 'q17', 'q18', 'q19', 'q20', 'q21', 'q22', 'q23', 'q24', 'q25', 'q26', 'q27', 'q28', 'q29', 'q30']
    # Get distinct values for filters
    standards = BaselineResult.objects.values_list('standard', flat=True).distinct()
    phases = BaselineResult.objects.values_list('phase', flat=True).distinct()

    paginator = Paginator(results, 100)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'standards': standards,
        'phases': phases,
        'selected_standard': standard,
        'selected_phase': phase,
        'questions':questions,
        'students':results
    }
    return render(request, 'html/view_baseline.html', context)