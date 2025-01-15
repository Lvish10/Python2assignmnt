from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Marks, Attendance, Module, Quiz
from django.contrib.auth.hashers import make_password, check_password  # For password hashing and verification

def home(request):
    return render(request, 'school_app/home.html')

def add_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        age = request.POST.get('age')
        student_class = request.POST.get('class')
        address = request.POST.get('address')
        medical_info = request.POST.get('medical_info')
        password = request.POST.get('password')
        cohort = request.POST.get('cohort')

        if student_id and name and age and student_class and address and medical_info and password and cohort:
            # Hash the password before saving
            hashed_password = make_password(password)
            Student.objects.create(
                student_id=student_id,
                name=name,
                age=age,
                student_class=student_class,
                address=address,
                medical_info=medical_info,
                password=hashed_password,
                cohort=cohort
            )
            return redirect('view_students')
    return render(request, 'school_app/add_student.html')

def view_students(request):
    students = Student.objects.all()
    return render(request, 'school_app/view_students.html', {'students': students})

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'teacher' and password == 'teacher123':
            return redirect('teacher_dashboard')
        else:
            return render(request, 'school_app/teacher_login.html', {'error': 'Invalid username or password'})
    return render(request, 'school_app/teacher_login.html')

def student_login(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')
        try:
            student = Student.objects.get(student_id=student_id)
            if check_password(password, student.password):  # Verify the password
                return redirect('student_dashboard', student_id=student_id)
            else:
                return render(request, 'school_app/student_login.html', {'error': 'Invalid password'})
        except Student.DoesNotExist:
            return render(request, 'school_app/student_login.html', {'error': 'Student ID not found'})
    return render(request, 'school_app/student_login.html')

def teacher_dashboard(request):
    return render(request, 'school_app/teacher_dashboard.html')

def student_dashboard(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'school_app/student_dashboard.html', {'student': student})

def view_marks(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    marks = Marks.objects.filter(student=student)
    return render(request, 'school_app/view_marks.html', {'student_marks': marks})

def view_attendance(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    attendance = Attendance.objects.filter(student=student)
    return render(request, 'school_app/view_attendance.html', {'student_attendance': attendance})

def add_marks(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        subject = request.POST.get('subject')
        marks = request.POST.get('marks')
        comments = request.POST.get('comments')

        if student_id and subject and marks:
            student = get_object_or_404(Student, student_id=student_id)
            Marks.objects.create(
                student=student,
                subject=subject,
                marks=marks,
                comments=comments
            )
            return redirect('teacher_dashboard')
    return render(request, 'school_app/add_marks.html')

def manage_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        subject = request.POST.get('subject')
        attendance = request.POST.get('attendance')

        if student_id and subject and attendance:
            student = get_object_or_404(Student, student_id=student_id)
            Attendance.objects.create(
                student=student,
                subject=subject,
                attendance=attendance
            )
            return redirect('teacher_dashboard')
    return render(request, 'school_app/manage_attendance.html')

import matplotlib.pyplot as plt
import io
import base64

def teacher_visualizations(request):
    # Generate a bar chart for average marks by subject
    marks = Marks.objects.all()
    subjects = {}
    for mark in marks:
        subject = mark.subject
        score = mark.marks
        if subject in subjects:
            subjects[subject].append(score)
        else:
            subjects[subject] = [score]

    avg_marks = {subject: sum(scores) / len(scores) for subject, scores in subjects.items()}

    plt.figure(figsize=(10, 5))
    plt.bar(avg_marks.keys(), avg_marks.values(), color='skyblue')
    plt.xlabel('Subject')
    plt.ylabel('Average Marks')
    plt.title('Average Marks by Subject')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render(request, 'school_app/teacher_visualizations.html', {'image': image_base64})

def view_modules(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    modules = Module.objects.filter(student=student)
    return render(request, 'school_app/view_modules.html', {'student_modules': modules})

def view_quizzes(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    quizzes = Quiz.objects.filter(module__student=student)
    return render(request, 'school_app/view_quizzes.html', {'student_quizzes': quizzes})

def generate_report_card(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    marks = Marks.objects.filter(student=student)
    attendance = Attendance.objects.filter(student=student)

    return render(request, 'school_app/report_card.html', {
        'student': student,
        'marks': marks,
        'attendance': attendance,
    })