from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'ذكر'),
        ('F', 'أنثى'),
    ]
    
    YEAR_CHOICES = [
        ('1', 'السنة الأولى'),
        ('2', 'السنة الثانية'), 
        ('3', 'السنة الثالثة'),
        ('4', 'السنة الرابعة'),
    ]
    
    first_name = models.CharField(max_length=50, verbose_name="الاسم الأول")
    last_name = models.CharField(max_length=50, verbose_name="اسم العائلة")
    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=15, blank=True, verbose_name="رقم الهاتف")
    age = models.IntegerField(
        validators=[MinValueValidator(16), MaxValueValidator(100)],
        verbose_name="العمر"
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="الجنس")
    student_id = models.CharField(max_length=20, unique=True, verbose_name="رقم الطالب")
    year = models.CharField(max_length=1, choices=YEAR_CHOICES, verbose_name="السنة الدراسية")
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, verbose_name="المعدل التراكمي")
    address = models.TextField(blank=True, verbose_name="العنوان")
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True, verbose_name="الصورة الشخصية")
    date_enrolled = models.DateField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    is_active = models.BooleanField(default=True, verbose_name="حالة النشاط")
    
    class Meta:
        verbose_name = "طالب"
        verbose_name_plural = "الطلاب"
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def get_year_display_full(self):
        return dict(self.YEAR_CHOICES)[self.year]


from teachers.models import Course

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="الطالب")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="المقرر")
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="الدرجة")
    date_recorded = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    
    class Meta:
        verbose_name = "درجة"
        verbose_name_plural = "الدرجات"
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.course.name}: {self.score}"

