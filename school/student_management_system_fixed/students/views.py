from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Student
from .forms import StudentForm, StudentSearchForm
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Dashboard View
def dashboard(request):
    """Dashboard with statistics and charts"""
    total_students = Student.objects.count()
    active_students = Student.objects.filter(is_active=True).count()
    inactive_students = total_students - active_students
    
    # Year distribution
    year_stats = Student.objects.values('year').annotate(count=Count('year')).order_by('year')
    
    # Gender distribution
    gender_stats = Student.objects.values('gender').annotate(count=Count('gender'))
    
    # Average GPA
    avg_gpa = Student.objects.aggregate(avg_gpa=Avg('gpa'))['avg_gpa'] or 0
    
    context = {
        'total_students': total_students,
        'active_students': active_students,
        'inactive_students': inactive_students,
        'year_stats': year_stats,
        'gender_stats': gender_stats,
        'avg_gpa': round(avg_gpa, 2),
    }
    return render(request, 'students/dashboard.html', context)

# List all students with search and filters
def student_list(request):
    """Display all students with search and filtering capabilities"""
    students = Student.objects.all()
    search_form = StudentSearchForm(request.GET)
    
    # Apply search filters
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        year = search_form.cleaned_data.get('year')
        gender = search_form.cleaned_data.get('gender')
        is_active = search_form.cleaned_data.get('is_active')
        
        if search_query:
            students = students.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(student_id__icontains=search_query)
            )
        
        if year:
            students = students.filter(year=year)
            
        if gender:
            students = students.filter(gender=gender)
            
        if is_active:
            students = students.filter(is_active=is_active == 'True')
    
    # Ordering (from QuerySet examples)
    order_by = request.GET.get('order_by', 'first_name')
    if order_by.startswith('-'):
        students = students.order_by(order_by)
    else:
        students = students.order_by(order_by)
    
    # Pagination
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'current_order': order_by,
    }
    return render(request, 'students/student_list.html', context)

# Student detail view
def student_detail(request, pk):
    """Display single student details"""
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})

# Create new student
def student_create(request):
    """Create new student"""
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.full_name} has been created successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    
    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Add New Student'
    })

# Update student
def student_update(request, pk):
    """Update existing student"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.full_name} has been updated successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'students/student_form.html', {
        'form': form,
        'student': student,
        'title': f'Update {student.full_name}'
    })

# Delete student
def student_delete(request, pk):
    """Delete student"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student_name = student.full_name
        student.delete()
        messages.success(request, f'Student {student_name} has been deleted successfully!')
        return redirect('student_list')
    
    return render(request, 'students/student_confirm_delete.html', {'student': student})

# Advanced QuerySet examples
def advanced_queries(request):
    """Demonstrate advanced QuerySet operations from the presentation"""
    
    # Order by (ascending and descending)
    students_asc = Student.objects.order_by('first_name')
    students_desc = Student.objects.order_by('-first_name')
    
    # Contains search
    name_contains = Student.objects.filter(first_name__contains='a')
    
    # In query (multiple values)
    years_in = Student.objects.filter(year__in=['1', '2', '3'])
    
    # Range query
    age_range = Student.objects.filter(age__range=[18, 25])
    
    # Exact match
    exact_year = Student.objects.filter(year__exact='1')
    
    # Exclude
    exclude_inactive = Student.objects.exclude(is_active=False)
    
    # Complex query with Q objects
    complex_query = Student.objects.filter(
        Q(first_name__icontains='Malek') | Q(age__lt=23)
    )
    
    context = {
        'students_asc': students_asc[:5],
        'students_desc': students_desc[:5],
        'name_contains': name_contains[:5],
        'years_in': years_in[:5],
        'age_range': age_range[:5],
        'exact_year': exact_year[:5],
        'exclude_inactive': exclude_inactive[:5],
        'complex_query': complex_query[:5],
    }
    
    return render(request, 'students/advanced_queries.html', context)

# Export to CSV
def export_csv(request):
    """Export students data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Student ID', 'First Name', 'Last Name', 'Email', 'Phone',
        'Age', 'Gender', 'Year', 'GPA', 'Date Enrolled', 'Active'
    ])
    
    students = Student.objects.all()
    for student in students:
        writer.writerow([
            student.student_id,
            student.first_name,
            student.last_name,
            student.email,
            student.phone,
            student.age,
            student.get_gender_display(),
            student.get_year_display(),
            student.gpa,
            student.date_enrolled,
            'Yes' if student.is_active else 'No'
        ])
    
    return response

# Export to PDF
def export_pdf(request):
    """Export students data to PDF"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    # Title
    styles = getSampleStyleSheet()
    title = Paragraph("Students Report", styles['Title'])
    elements.append(title)
    
    # Table data
    data = [['ID', 'Name', 'Email', 'Year', 'GPA', 'Status']]
    students = Student.objects.all()
    
    for student in students:
        data.append([
            student.student_id,
            student.full_name,
            student.email,
            student.get_year_display(),
            str(student.gpa),
            'Active' if student.is_active else 'Inactive'
        ])
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    return response

# AJAX views for dynamic content
def get_student_stats(request):
    """Return student statistics as JSON for charts"""
    year_stats = list(Student.objects.values('year').annotate(count=Count('year')))
    gender_stats = list(Student.objects.values('gender').annotate(count=Count('gender')))
    
    return JsonResponse({
        'year_stats': year_stats,
        'gender_stats': gender_stats
    })
