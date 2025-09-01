
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Teacher, Course
from students.models import Student, Grade
from django.contrib import messages
from django.forms import inlineformset_factory
from students.forms import GradeForm

@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = Course.objects.filter(teacher=teacher)
    context = {
        'teacher': teacher,
        'courses': courses,
    }
    return render(request, 'teachers/dashboard.html', context)

@login_required
def teacher_course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher__user=request.user)
    students_in_course = Student.objects.filter(courses=course)
    context = {
        'course': course,
        'students_in_course': students_in_course,
    }
    return render(request, 'teachers/course_detail.html', context)

@login_required
def edit_student_grade(request, student_id, course_id):
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id, teacher__user=request.user)
    grade, created = Grade.objects.get_or_create(student=student, course=course)

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث درجة الطالب بنجاح.')
            return redirect('teacher_course_detail', course_id=course.id)
    else:
        form = GradeForm(instance=grade)

    context = {
        'student': student,
        'course': course,
        'form': form,
    }
    return render(request, 'teachers/edit_grade.html', context)




