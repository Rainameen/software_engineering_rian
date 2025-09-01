#!/usr/bin/env python
"""
إنشاء بيانات تجريبية للمعلمين والأقسام
"""

import os
import sys
import django
from django.core.management.base import BaseCommand

# إعداد بيئة Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from teachers.models import Department, Teacher, Course
from django.contrib.auth.models import User
from django.utils import timezone
import random
from datetime import date, timedelta

def create_sample_data():
    """إنشاء بيانات تجريبية للمعلمين والأقسام"""
    
    print("🚀 إنشاء بيانات تجريبية للمعلمين والأقسام...")
    
    # إنشاء الأقسام
    departments_data = [
        {'name': 'قسم علوم الحاسوب', 'code': 'CS', 'description': 'قسم علوم الحاسوب وتقنية المعلومات'},
        {'name': 'قسم الهندسة', 'code': 'ENG', 'description': 'قسم الهندسة بجميع تخصصاتها'},
        {'name': 'قسم إدارة الأعمال', 'code': 'BA', 'description': 'قسم إدارة الأعمال والاقتصاد'},
        {'name': 'قسم الطب', 'code': 'MED', 'description': 'قسم الطب والعلوم الصحية'},
        {'name': 'قسم الآداب', 'code': 'ART', 'description': 'قسم الآداب واللغات'},
    ]
    
    departments = []
    for dept_data in departments_data:
        dept, created = Department.objects.get_or_create(
            code=dept_data['code'],
            defaults={
                'name': dept_data['name'],
                'description': dept_data['description']
            }
        )
        departments.append(dept)
        if created:
            print(f"✅ تم إنشاء القسم: {dept.name}")
    
    # بيانات المعلمين
    teachers_data = [
        {'first_name': 'أحمد', 'last_name': 'المحمد', 'rank': 'professor', 'specialization': 'هندسة البرمجيات'},
        {'first_name': 'فاطمة', 'last_name': 'العلي', 'rank': 'associate_professor', 'specialization': 'قواعد البيانات'},
        {'first_name': 'محمد', 'last_name': 'الأحمد', 'rank': 'assistant_professor', 'specialization': 'الذكاء الاصطناعي'},
        {'first_name': 'عائشة', 'last_name': 'السالم', 'rank': 'lecturer', 'specialization': 'شبكات الحاسوب'},
        {'first_name': 'عمر', 'last_name': 'الخالد', 'rank': 'professor', 'specialization': 'الهندسة المدنية'},
        {'first_name': 'خديجة', 'last_name': 'الزهراء', 'rank': 'associate_professor', 'specialization': 'إدارة المشاريع'},
        {'first_name': 'علي', 'last_name': 'الحسن', 'rank': 'assistant_professor', 'specialization': 'الطب الباطني'},
        {'first_name': 'زينب', 'last_name': 'الفاطمي', 'rank': 'lecturer', 'specialization': 'الأدب العربي'},
    ]
    
    # حذف المعلمين الموجودين
    Teacher.objects.all().delete()
    User.objects.filter(is_staff=False, is_superuser=False).delete()
    
    teachers_created = 0
    
    for i, teacher_data in enumerate(teachers_data):
        try:
            # إنشاء حساب المستخدم
            username = f"{teacher_data['first_name'].lower()}.{teacher_data['last_name'].lower()}"
            email = f"{username}@university.edu.sa"
            
            # التأكد من عدم وجود المستخدم
            if User.objects.filter(username=username).exists():
                username = f"{username}{i+1}"
                email = f"{username}@university.edu.sa"
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=teacher_data['first_name'],
                last_name=teacher_data['last_name'],
                password='teacher123'  # كلمة مرور افتراضية
            )
            
            # إنشاء المعلم
            department = random.choice(departments)
            hire_date = date.today() - timedelta(days=random.randint(365, 3650))  # من سنة إلى 10 سنوات
            
            teacher = Teacher.objects.create(
                user=user,
                employee_id=f"T{2020 + i:04d}",
                phone=f"+966{random.randint(500000000, 599999999)}",
                office_number=f"{random.randint(100, 999)}",
                department=department,
                rank=teacher_data['rank'],
                employment_type=random.choice(['full_time', 'part_time', 'contract']),
                specialization=teacher_data['specialization'],
                hire_date=hire_date,
                salary=random.randint(8000, 25000),
                years_of_experience=random.randint(1, 20),
                is_active=random.choice([True, True, True, False])  # 75% نشط
            )
            
            teachers_created += 1
            print(f"✅ تم إنشاء المعلم {teachers_created}: {teacher.full_name} - {teacher.get_rank_display()}")
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء المعلم {i+1}: {e}")
            continue
    
    # تعيين رؤساء الأقسام
    for department in departments:
        professors = Teacher.objects.filter(department=department, rank='professor', is_active=True)
        if professors.exists():
            department.head_of_department = professors.first()
            department.save()
            print(f"✅ تم تعيين {department.head_of_department.full_name} رئيساً لقسم {department.name}")
    
    # إنشاء بعض المقررات
    courses_data = [
        {'code': 'CS101', 'name': 'مقدمة في البرمجة', 'credit_hours': 3},
        {'code': 'CS201', 'name': 'هياكل البيانات', 'credit_hours': 3},
        {'code': 'ENG101', 'name': 'الرياضيات الهندسية', 'credit_hours': 4},
        {'code': 'BA101', 'name': 'مبادئ الإدارة', 'credit_hours': 3},
        {'code': 'MED101', 'name': 'التشريح', 'credit_hours': 5},
    ]
    
    Course.objects.all().delete()
    courses_created = 0
    
    for course_data in courses_data:
        try:
            # اختيار قسم مناسب حسب رمز المقرر
            if course_data['code'].startswith('CS'):
                dept = Department.objects.get(code='CS')
            elif course_data['code'].startswith('ENG'):
                dept = Department.objects.get(code='ENG')
            elif course_data['code'].startswith('BA'):
                dept = Department.objects.get(code='BA')
            elif course_data['code'].startswith('MED'):
                dept = Department.objects.get(code='MED')
            else:
                dept = random.choice(departments)
            
            # اختيار معلم من نفس القسم
            teachers_in_dept = Teacher.objects.filter(department=dept, is_active=True)
            if teachers_in_dept.exists():
                teacher = random.choice(teachers_in_dept)
                
                course = Course.objects.create(
                    code=course_data['code'],
                    name=course_data['name'],
                    credit_hours=course_data['credit_hours'],
                    department=dept,
                    teacher=teacher,
                    semester='الفصل الأول',
                    year=2024,
                    is_active=True
                )
                
                courses_created += 1
                print(f"✅ تم إنشاء المقرر: {course.code} - {course.name}")
        
        except Exception as e:
            print(f"❌ خطأ في إنشاء المقرر {course_data['code']}: {e}")
    
    print(f"\n📊 ملخص البيانات المنشأة:")
    print(f"الأقسام: {Department.objects.count()}")
    print(f"المعلمون: {Teacher.objects.count()}")
    print(f"المقررات: {Course.objects.count()}")
    
    # إحصائيات المعلمين
    print(f"\n📈 إحصائيات المعلمين:")
    for rank_code, rank_name in Teacher.RANK_CHOICES:
        count = Teacher.objects.filter(rank=rank_code).count()
        print(f"{rank_name}: {count}")
    
    print(f"\n✨ تم إنشاء البيانات التجريبية بنجاح!")
    print(f"يمكنك الآن تسجيل الدخول بأي من المعلمين باستخدام:")
    print(f"اسم المستخدم: ahmed.almohammad (مثال)")
    print(f"كلمة المرور: teacher123")

if __name__ == '__main__':
    create_sample_data()

