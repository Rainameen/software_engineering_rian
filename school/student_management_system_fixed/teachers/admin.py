from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Department, Teacher, Course, TeacherPermissionLog

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'head_of_department', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'code']
    ordering = ['name']
    
    fieldsets = (
        ('معلومات القسم', {
            'fields': ('name', 'code', 'description')
        }),
        ('الإدارة', {
            'fields': ('head_of_department',)
        }),
    )

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'employee_id', 'department', 'rank', 
        'employment_type', 'is_active', 'hire_date'
    ]
    list_filter = ['department', 'rank', 'employment_type', 'is_active', 'hire_date']
    search_fields = ['user__first_name', 'user__last_name', 'employee_id', 'specialization']
    ordering = ['user__first_name', 'user__last_name']
    readonly_fields = ['date_created', 'date_updated']
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('user', 'employee_id', 'photo')
        }),
        ('معلومات الاتصال', {
            'fields': ('phone', 'office_number')
        }),
        ('المعلومات الأكاديمية', {
            'fields': ('department', 'rank', 'specialization', 'employment_type')
        }),
        ('معلومات التوظيف', {
            'fields': ('hire_date', 'salary', 'years_of_experience')
        }),
        ('الحالة', {
            'fields': ('is_active',)
        }),
        ('معلومات النظام', {
            'fields': ('date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'الاسم الكامل'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'department')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'teacher', 'credit_hours', 'semester', 'year', 'is_active']
    list_filter = ['department', 'teacher', 'semester', 'year', 'is_active']
    search_fields = ['code', 'name', 'teacher__user__first_name', 'teacher__user__last_name']
    ordering = ['code']
    
    fieldsets = (
        ('معلومات المقرر', {
            'fields': ('code', 'name', 'description', 'credit_hours')
        }),
        ('التخصيص', {
            'fields': ('department', 'teacher')
        }),
        ('الفصل الدراسي', {
            'fields': ('semester', 'year', 'is_active')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('department', 'teacher__user')

@admin.register(TeacherPermissionLog)
class TeacherPermissionLogAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'action', 'permission', 'timestamp', 'ip_address']
    list_filter = ['action', 'permission', 'timestamp']
    search_fields = ['teacher__user__first_name', 'teacher__user__last_name', 'action', 'permission']
    ordering = ['-timestamp']
    readonly_fields = ['teacher', 'action', 'permission', 'timestamp', 'ip_address']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('teacher__user')

# تخصيص واجهة المستخدم
admin.site.site_header = "نظام إدارة الطلاب والمعلمين"
admin.site.site_title = "لوحة الإدارة"
admin.site.index_title = "مرحباً بك في لوحة الإدارة"
