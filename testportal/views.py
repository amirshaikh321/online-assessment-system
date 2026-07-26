from django.shortcuts import render, redirect

from testportal.models import Question, student, Admin
from .forms import QuestionForm

# Create your views here.
def home(request):
    return render(request,'login.html')

def stddashboard(request):
    return render(request,'student/stddash.html')

def admindashboard(request):
    return render(request,'admin/admindash.html')

def show_questions(request):
    questions = Question.objects.all()
    return render(request, 'questions/showquestions.html', {'questions': questions})

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_questions')
    else:
        form = QuestionForm()
    return render(request, 'questions/createquestion.html', {'form': form})


def login(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'student':
            email = request.POST.get('email')
            password = request.POST.get('password')
            if student.objects.filter(email=email, password=password).exists():
                name = student.objects.get(email=email).name  # Store the student's name in the session
                request.session['student_name'] = name  # Store the student's name in the session
                return render(request,'student/stddash.html', {'student_name': name})  # Redirect to student dashboard
            return render(request, 'login.html', {'error_message': "Invalid email or password."})
        elif role == 'admin':
            email = request.POST.get('email')
            password = request.POST.get('password')
            if Admin.objects.filter(email=email, password=password).exists():
                return render(request,'admin/admindash.html')  # Redirect to admin dashboard
            return render(request, 'login.html', {'error_message': "Invalid email or password."})
    return render(request, 'login.html')

def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        rollno = request.POST.get('rollno')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if student.objects.filter(email=email).exists():
            return render(request, 'admin/add_student.html', {'error_message': "A student with this email already exists."})

        student_obj = student(name=name, rollno=rollno, email=email, password=password)
        student_obj.save()
        return render(request, 'admin/add_student.html', {'success_message': "Student added successfully."})  # Redirect to student dashboard after successful registration

    return render(request, 'admin/add_student.html')

def logout(request):
    # Clear the session data
    request.session.flush()
    return redirect('login')  # Redirect to the login page after logout