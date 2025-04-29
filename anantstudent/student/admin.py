from django.contrib import admin

from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'sl_no', 'name', 'standard', 'gender', 'contact_no', 
        'school_name', 'district', 'phase', 'certificate_issued'
    )
    search_fields = (
        'name', 'aadhar_no', 'contact_no', 'school_name', 'district'
    )
    list_filter = ('gender', 'standard', 'district', 'phase', 'certificate_issued')
    ordering = ('sl_no',)
    list_per_page = 50  # Show 50 students per page

    # Optional: If you want fields to be grouped nicely when editing
    fieldsets = (
        (None, {
            'fields': ('sl_no', 'benf_no', 'aadhar_no', 'name', 'standard', 'gender', 'contact_no')
        }),
        ('Tribal Details', {
            'fields': ('scheduled_tribes', 'pvtgs')
        }),
        ('School & Phase Info', {
            'fields': ('school_name', 'phase', 'district')
        }),
        ('Certificate Info', {
            'fields': ('certificate_issued', 'digital_role')
        }),
    )
    actions = ['delete_all_students']
    @admin.action(description='Delete all students')
    def delete_all_students(self, request, queryset):
        Student.objects.all().delete()

# Register your models here.
