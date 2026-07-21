from django.shortcuts import render, redirect

from testportal.models import Question
from .forms import QuestionForm

# Create your views here.
def home(request):
    return render(request,'home.html')

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