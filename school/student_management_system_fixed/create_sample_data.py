#!/usr/bin/env python
"""
Sample data creation script for Student Management System
Run this script to populate the database with sample students
"""

import os
import sys
import django
from django.core.management.base import BaseCommand

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from students.models import Student
from django.utils import timezone
import random

def create_sample_students():
    """Create sample student data"""
    
    # Sample data
    first_names = [
        'Ahmed', 'Fatima', 'Mohammed', 'Aisha', 'Omar', 'Khadija', 'Ali', 'Zainab',
        'Hassan', 'Mariam', 'Yusuf', 'Layla', 'Ibrahim', 'Nour', 'Khalid', 'Sara',
        'Abdullah', 'Amina', 'Malek', 'Huda', 'Tariq', 'Yasmin', 'Rashid', 'Dina'
    ]
    
    last_names = [
        'Al-Rashid', 'Al-Zahra', 'Al-Mansouri', 'Al-Hashimi', 'Al-Qasimi', 'Al-Maktoum',
        'Al-Sabah', 'Al-Thani', 'Al-Khalifa', 'Al-Saud', 'Al-Nahyan', 'Al-Sharqi',
        'Al-Nuaimi', 'Al-Otaibi', 'Al-Dosari', 'Al-Ghamdi', 'Al-Harbi', 'Al-Shehri',
        'Al-Qahtani', 'Al-Mutairi', 'Al-Subai', 'Al-Enezi', 'Al-Rashidi', 'Almosanif'
    ]
    
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'university.edu']
    
    # Clear existing data
    Student.objects.all().delete()
    print("Cleared existing student data...")
    
    students_created = 0
    
    for i in range(50):  # Create 50 sample students
        try:
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            # Generate unique student ID
            year = random.choice(['2020', '2021', '2022', '2023', '2024'])
            student_id = f"{year}{first_name[:2].upper()}{last_name[:2].upper()}{random.randint(100, 999)}"
            
            # Check if student ID already exists
            while Student.objects.filter(student_id=student_id).exists():
                student_id = f"{year}{first_name[:2].upper()}{last_name[:2].upper()}{random.randint(100, 999)}"
            
            # Generate email
            email = f"{first_name.lower()}.{last_name.lower().replace('-', '')}@{random.choice(domains)}"
            
            # Check if email already exists
            counter = 1
            original_email = email
            while Student.objects.filter(email=email).exists():
                email = f"{original_email.split('@')[0]}{counter}@{original_email.split('@')[1]}"
                counter += 1
            
            # Generate other data
            age = random.randint(18, 28)
            gender = random.choice(['M', 'F'])
            year_level = random.choice(['1', '2', '3', '4'])
            gpa = round(random.uniform(2.0, 4.0), 2)
            phone = f"+966{random.randint(500000000, 599999999)}"
            is_active = random.choice([True, True, True, False])  # 75% active
            
            # Create student
            student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                age=age,
                gender=gender,
                student_id=student_id,
                year=year_level,
                gpa=gpa,
                address=f"Street {random.randint(1, 100)}, District {random.randint(1, 20)}, City",
                is_active=is_active
            )
            
            students_created += 1
            print(f"Created student {students_created}: {student.full_name} ({student.student_id})")
            
        except Exception as e:
            print(f"Error creating student {i+1}: {e}")
            continue
    
    print(f"\n✅ Successfully created {students_created} sample students!")
    
    # Print some statistics
    total_students = Student.objects.count()
    active_students = Student.objects.filter(is_active=True).count()
    male_students = Student.objects.filter(gender='M').count()
    female_students = Student.objects.filter(gender='F').count()
    
    print(f"\n📊 Database Statistics:")
    print(f"Total Students: {total_students}")
    print(f"Active Students: {active_students}")
    print(f"Inactive Students: {total_students - active_students}")
    print(f"Male Students: {male_students}")
    print(f"Female Students: {female_students}")
    
    # Year distribution
    for year in ['1', '2', '3', '4']:
        count = Student.objects.filter(year=year).count()
        year_name = dict(Student.YEAR_CHOICES)[year]
        print(f"{year_name}: {count}")
    
    print(f"\n🎯 Sample students with 'Malek' in name: {Student.objects.filter(first_name__icontains='Malek').count()}")
    print(f"🎯 Students under 23: {Student.objects.filter(age__lt=23).count()}")
    print(f"🎯 Students in first 3 years: {Student.objects.filter(year__in=['1', '2', '3']).count()}")

if __name__ == '__main__':
    print("🚀 Creating sample student data...")
    create_sample_students()
    print("✨ Sample data creation completed!")

