from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    student_class = models.CharField(max_length=50)
    address = models.TextField()
    medical_info = models.TextField()
    password = models.CharField(max_length=128)  # Store hashed passwords
    cohort = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.name} - {self.subject}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    subject = models.CharField(max_length=100)
    attendance = models.IntegerField()  # Percentage

    def __str__(self):
        return f"{self.student.name} - {self.subject}"

class Module(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='modules')
    module_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.student.name} - {self.module_name}"

class Quiz(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='quizzes')
    quiz_name = models.CharField(max_length=100)
    answer = models.TextField()

    def __str__(self):
        return f"{self.module.module_name} - {self.quiz_name}"