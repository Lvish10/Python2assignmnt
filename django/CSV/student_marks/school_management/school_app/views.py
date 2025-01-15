from django.shortcuts import render, redirect
from .utils import read_csv, write_csv, STUDENT_FILE, MARKS_FILE, ATTENDANCE_FILE, MODULES_FILE, QUIZZES_FILE, hash_password, verify_password
from django.shortcuts import render

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
            hashed_password = hash_password(password)  # Use the imported hash_password function
            write_csv(STUDENT_FILE, [student_id, name, age, student_class, address, medical_info, hashed_password, cohort])
            return redirect('view_students')
    return render(request, 'school_app/add_student.html')

def view_students(request):
    students = read_csv(STUDENT_FILE)[1:]  # Skip header
    return render(request, 'school_app/view_students.html', {'students': students})


def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'teacher' and password == 'teacher123':
            # Assuming you have a custom user model or a way to handle teacher login
            return redirect('teacher_dashboard')
        else:
            return render(request, 'school_app/teacher_login.html', {'error': 'Invalid username or password'})
    return render(request, 'school_app/teacher_login.html')

def student_login(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')
        students = read_csv(STUDENT_FILE)
        for student in students[1:]:
            if student[0] == student_id and verify_password(password, student[6]):
                # Assuming you have a custom user model or a way to handle student login
                return redirect('student_dashboard', student_id=student_id)
        return render(request, 'school_app/student_login.html', {'error': 'Invalid Student ID or password'})
    return render(request, 'school_app/student_login.html')

def teacher_dashboard(request):
    return render(request, 'school_app/teacher_dashboard.html')

def student_dashboard(request, student_id):
    students = read_csv(STUDENT_FILE)
    student = next((s for s in students[1:] if s[0] == student_id), None)
    if student:
        return render(request, 'school_app/student_dashboard.html', {'student': student})
    else:
        return redirect('student_login')
    
    

def view_marks(request, student_id):
    marks = read_csv(MARKS_FILE)
    student_marks = [mark for mark in marks[1:] if mark[0] == student_id]
    return render(request, 'school_app/view_marks.html', {'student_marks': student_marks})

def view_attendance(request, student_id):
    attendance = read_csv(ATTENDANCE_FILE)
    student_attendance = [att for att in attendance[1:] if att[0] == student_id]
    return render(request, 'school_app/view_attendance.html', {'student_attendance': student_attendance})

def add_marks(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        subject = request.POST.get('subject')
        marks = request.POST.get('marks')
        comments = request.POST.get('comments')

        if student_id and subject and marks:
            write_csv(MARKS_FILE, [student_id, subject, marks, comments])
            return redirect('teacher_dashboard')
    return render(request, 'school_app/add_marks.html')

def manage_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        subject = request.POST.get('subject')
        attendance = request.POST.get('attendance')

        if student_id and subject and attendance:
            write_csv(ATTENDANCE_FILE, [student_id, subject, attendance])
            return redirect('teacher_dashboard')
    return render(request, 'school_app/manage_attendance.html')

import matplotlib.pyplot as plt
import io
import base64

def teacher_visualizations(request):
    # Generate a bar chart for average marks by subject
    marks = read_csv(MARKS_FILE)[1:]
    subjects = {}
    for mark in marks:
        subject = mark[1]
        score = int(mark[2])
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
    modules = read_csv(MODULES_FILE)
    student_modules = [module for module in modules[1:] if module[0] == student_id]
    return render(request, 'school_app/view_modules.html', {'student_modules': student_modules})

def view_quizzes(request, student_id):
    quizzes = read_csv(QUIZZES_FILE)
    student_quizzes = [quiz for quiz in quizzes[1:]]
    return render(request, 'school_app/view_quizzes.html', {'student_quizzes': student_quizzes})

def generate_report_card(request, student_id):
    students = read_csv(STUDENT_FILE)
    marks = read_csv(MARKS_FILE)
    attendance = read_csv(ATTENDANCE_FILE)

    # Find the student
    student = next((s for s in students[1:] if s[0] == student_id), None)
    if not student:
        return redirect('teacher_dashboard')

    # Get marks for the student
    student_marks = [mark for mark in marks[1:] if mark[0] == student_id]

    # Get attendance for the student
    student_attendance = [att for att in attendance[1:] if att[0] == student_id]

    return render(request, 'school_app/report_card.html', {
        'student': student,
        'marks': student_marks,
        'attendance': student_attendance,
    })