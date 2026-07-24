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

# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             student = student.objects.get(email=email, password=password)
#             return redirect('stddashboard')  # Redirect to student dashboard
#         except student.DoesNotExist:
#             try:
#                 admin = Admin.objects.get(email=email, password=password)
#                 return redirect('admindashboard')  # Redirect to admin dashboard
#             except Admin.DoesNotExist:
#                 error_message = "Invalid email or password."
#                 return render(request, 'login.html', {'error_message': error_message})

#     return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'student':
            email = request.POST.get('email')
            password = request.POST.get('password')
            if student.objects.filter(email=email, password=password).exists():
                return render(request,'student/stddash.html')  # Redirect to student dashboard
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
        return render(request, 'admin/add_student.html')  # Redirect to student dashboard after successful registration

    return render(request, 'admin/add_student.html')