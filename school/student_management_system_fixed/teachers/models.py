from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class Department(models.Model):
    """قسم أكاديمي"""
    name = models.CharField(max_length=100, verbose_name="اسم القسم")
    code = models.CharField(max_length=10, unique=True, verbose_name="رمز القسم")
    description = models.TextField(blank=True, verbose_name="وصف القسم")
    head_of_department = models.ForeignKey(
        'Teacher', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='headed_department',
        verbose_name="رئيس القسم"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "قسم"
        verbose_name_plural = "الأقسام"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Teacher(models.Model):
    """نموذج المعلم مع الصلاحيات"""
    
    RANK_CHOICES = [
        ('lecturer', 'محاضر'),
        ('assistant_professor', 'أستاذ مساعد'),
        ('associate_professor', 'أستاذ مشارك'),
        ('professor', 'أستاذ'),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'دوام كامل'),
        ('part_time', 'دوام جزئي'),
        ('contract', 'متعاقد'),
        ('visiting', 'زائر'),
    ]
    
    # ربط بحساب المستخدم
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="حساب المستخدم")
    
    # المعلومات الشخصية
    employee_id = models.CharField(max_length=20, unique=True, verbose_name="الرقم الوظيفي")
    phone = models.CharField(max_length=15, blank=True, verbose_name="رقم الهاتف")
    office_number = models.CharField(max_length=20, blank=True, verbose_name="رقم المكتب")
    photo = models.ImageField(upload_to='teacher_photos/', blank=True, null=True, verbose_name="الصورة")
    
    # المعلومات الأكاديمية
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="القسم")
    rank = models.CharField(max_length=20, choices=RANK_CHOICES, verbose_name="الدرجة العلمية")
    employment_type = models.CharField(max_length=15, choices=EMPLOYMENT_TYPE_CHOICES, verbose_name="نوع التوظيف")
    specialization = models.CharField(max_length=100, verbose_name="التخصص")
    
    # معلومات التوظيف
    hire_date = models.DateField(verbose_name="تاريخ التوظيف")
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="الراتب")
    years_of_experience = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        default=0,
        verbose_name="سنوات الخبرة"
    )
    
    # الحالة
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "معلم"
        verbose_name_plural = "المعلمون"
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ("can_view_all_students", "يمكن عرض جميع الطلاب"),
            ("can_edit_student_grades", "يمكن تعديل درجات الطلاب"),
            ("can_generate_reports", "يمكن إنشاء التقارير"),
            ("can_manage_department", "يمكن إدارة القسم"),
            ("can_view_teacher_salaries", "يمكن عرض رواتب المعلمين"),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_rank_display()}"
    
    def get_absolute_url(self):
        return reverse('teacher_detail', kwargs={'pk': self.pk})
    
    @property
    def full_name(self):
        return self.user.get_full_name()
    
    @property
    def email(self):
        return self.user.email
    
    def save(self, *args, **kwargs):
        # إنشاء المجموعات والصلاحيات تلقائياً
        super().save(*args, **kwargs)
        self.assign_permissions()
    
    def assign_permissions(self):
        """تعيين الصلاحيات حسب الدرجة العلمية"""
        # إزالة جميع المجموعات السابقة
        self.user.groups.clear()
        
        # تعيين الصلاحيات حسب الدرجة العلمية
        if self.rank == 'professor':
            # الأساتذة لديهم جميع الصلاحيات
            group, created = Group.objects.get_or_create(name='أساتذة')
            permissions = [
                'can_view_all_students',
                'can_edit_student_grades', 
                'can_generate_reports',
                'can_manage_department',
                'can_view_teacher_salaries',
            ]
            self._add_permissions_to_group(group, permissions)
            self.user.groups.add(group)
            
        elif self.rank == 'associate_professor':
            # الأساتذة المشاركون
            group, created = Group.objects.get_or_create(name='أساتذة مشاركون')
            permissions = [
                'can_view_all_students',
                'can_edit_student_grades',
                'can_generate_reports',
                'can_manage_department',
            ]
            self._add_permissions_to_group(group, permissions)
            self.user.groups.add(group)
            
        elif self.rank == 'assistant_professor':
            # الأساتذة المساعدون
            group, created = Group.objects.get_or_create(name='أساتذة مساعدون')
            permissions = [
                'can_view_all_students',
                'can_edit_student_grades',
                'can_generate_reports',
            ]
            self._add_permissions_to_group(group, permissions)
            self.user.groups.add(group)
            
        else:  # lecturer
            # المحاضرون
            group, created = Group.objects.get_or_create(name='محاضرون')
            permissions = [
                'can_view_all_students',
                'can_edit_student_grades',
            ]
            self._add_permissions_to_group(group, permissions)
            self.user.groups.add(group)
    
    def _add_permissions_to_group(self, group, permission_codenames):
        """إضافة صلاحيات إلى المجموعة"""
        for codename in permission_codenames:
            try:
                permission = Permission.objects.get(codename=codename)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                pass

class Course(models.Model):
    """مقرر دراسي"""
    code = models.CharField(max_length=10, unique=True, verbose_name="رمز المقرر")
    name = models.CharField(max_length=100, verbose_name="اسم المقرر")
    description = models.TextField(blank=True, verbose_name="وصف المقرر")
    credit_hours = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name="الساعات المعتمدة"
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="القسم")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="المدرس")
    semester = models.CharField(max_length=20, verbose_name="الفصل الدراسي")
    year = models.IntegerField(verbose_name="السنة الدراسية")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    
    class Meta:
        verbose_name = "مقرر"
        verbose_name_plural = "المقررات"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class TeacherPermissionLog(models.Model):
    """سجل صلاحيات المعلمين"""
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="المعلم")
    action = models.CharField(max_length=100, verbose_name="الإجراء")
    permission = models.CharField(max_length=100, verbose_name="الصلاحية")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="الوقت")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="عنوان IP")
    
    class Meta:
        verbose_name = "سجل صلاحية"
        verbose_name_plural = "سجلات الصلاحيات"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.teacher.full_name} - {self.action} - {self.timestamp}"
