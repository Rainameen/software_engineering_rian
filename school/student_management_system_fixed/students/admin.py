from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'age', 'year', 'gpa', 'is_active', 'date_enrolled']
    list_filter = ['year', 'gender', 'is_active', 'date_enrolled']
    search_fields = ['first_name', 'last_name', 'email', 'student_id']
    list_editable = ['is_active']
    ordering = ['first_name', 'last_name']
    readonly_fields = ['date_enrolled']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'age', 'gender', 'photo')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Academic Information', {
            'fields': ('student_id', 'year', 'gpa')
        }),
        ('System Information', {
            'fields': ('is_active', 'date_enrolled'),
            'classes': ('collapse',)
        }),
    )
