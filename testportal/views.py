from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from testportal.models import Question, student, Admin
from .forms import QuestionForm

# Create your views here.
def home(request):
    return render(request,'login.html')

def stddashboard(request):
    student_name = request.session.get('student_name')
    if not student_name:
        return redirect('login')
    return render(request, 'student/stddash.html', {'student_name': student_name})

def admindashboard(request):
    admin_name = request.session.get('admin_name')
    if not admin_name:
        return redirect('login')
    total_students = student.objects.count()
    total_questions = Question.objects.count()
    return render(request, 'admin/admindash.html', {
        'admin_name': admin_name,
        'total_students': total_students,
        'total_questions': total_questions,
    })

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
                return redirect('stddashboard')  # Redirect to student dashboard
            return render(request, 'login.html', {'error_message': "Invalid email or password."})
        elif role == 'admin':
            email = request.POST.get('email')
            password = request.POST.get('password')
            if Admin.objects.filter(email=email, password=password).exists():
                name = Admin.objects.get(email = email).name
                request.session['admin_name'] = name  # Store the admin's name in the session
                return redirect('admindashboard')  # Redirect to admin dashboard
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

def testportal(request):
    student_name = request.session.get('student_name')
    if not student_name:
        return redirect('login')
    
    # Get all questions
    questions = list(Question.objects.all())
    total_questions = len(questions)
    
    if total_questions == 0:
        return render(request, 'student/test.html', {
            'error_message': 'No questions available in the database.',
            'student_name': student_name
        })
    
    # Initialize session variables if not present
    if 'test_question_ids' not in request.session or 'answers' not in request.session:
        request.session['test_question_ids'] = [q.id for q in questions]
        request.session['current_index'] = 0
        request.session['answers'] = {}
        request.session.modified = True

    # Get question IDs from session
    question_ids = request.session['test_question_ids']
    current_index = request.session.get('current_index', 0)
    
    # Make sure current_index is within bounds
    if current_index < 0:
        current_index = 0
    elif current_index >= len(question_ids):
        current_index = len(question_ids) - 1
    request.session['current_index'] = current_index

    # Get current question
    current_q_id = question_ids[current_index]
    try:
        current_question = Question.objects.get(id=current_q_id)
    except Question.DoesNotExist:
        # If question was deleted, reset and redirect
        request.session.pop('test_question_ids', None)
        return redirect('testportal')
        
    # Get student's current answers dictionary
    answers = request.session.get('answers', {})
    
    if request.method == 'POST':
        action = request.POST.get('action')
        selected_option = request.POST.get('selected_option', '').strip()
        
        # Save current answer if option is selected or clear if action is 'clear'
        if action == 'clear':
            if str(current_q_id) in answers:
                del answers[str(current_q_id)]
        else:
            if selected_option:
                answers[str(current_q_id)] = selected_option
            elif str(current_q_id) in answers and not selected_option:
                # Keep the previous answer if next was clicked without changes
                pass
        
        request.session['answers'] = answers
        request.session.modified = True
        
        # Process actions
        if action == 'next':
            if current_index < total_questions - 1:
                request.session['current_index'] = current_index + 1
            else:
                return redirect('submit_exam')
        elif action == 'prev':
            if current_index > 0:
                request.session['current_index'] = current_index - 1
        elif action == 'navigate':
            try:
                target_index = int(request.POST.get('target_index', 0))
                if 0 <= target_index < total_questions:
                    request.session['current_index'] = target_index
            except ValueError:
                pass
        elif action == 'submit':
            return redirect('submit_exam')
            
        request.session.modified = True
        return redirect('testportal')
        
    # Render the test page (GET request)
    options = [
        current_question.option1,
        current_question.option2,
        current_question.option3,
        current_question.option4,
    ]
    
    current_answer = answers.get(str(current_q_id), '')
    
    # Construct navigation metadata
    navigator_questions = []
    for idx, q_id in enumerate(question_ids):
        answered = str(q_id) in answers
        navigator_questions.append({
            'index': idx,
            'number': idx + 1,
            'answered': answered,
            'is_current': idx == current_index,
        })
        
    answered_count = len(answers)
    percent_complete = int((answered_count / total_questions) * 100) if total_questions > 0 else 0

    context = {
        'student_name': student_name,
        'current_question': current_question,
        'options': options,
        'current_answer': current_answer,
        'current_index': current_index,
        'question_number': current_index + 1,
        'total_questions': total_questions,
        'navigator_questions': navigator_questions,
        'percent_complete': percent_complete,
    }
    
    return render(request, 'student/test.html', context)

def submit_exam(request):
    student_name = request.session.get('student_name')
    if not student_name:
        return redirect('login')
    
    question_ids = request.session.get('test_question_ids', [])
    answers = request.session.get('answers', {})
    
    if not question_ids:
        return redirect('stddashboard')
        
    # Calculate score
    score = 0
    results = []
    total_questions = len(question_ids)
    
    for q_id in question_ids:
        try:
            q = Question.objects.get(id=q_id)
            user_ans = answers.get(str(q_id), '')
            is_correct = user_ans == q.correct_option
            if is_correct:
                score += 1
            results.append({
                'question': q.question_text,
                'user_answer': user_ans,
                'correct_answer': q.correct_option,
                'is_correct': is_correct,
            })
        except Question.DoesNotExist:
            continue
            
    # Clear the session exam progress so they can retake it
    request.session.pop('test_question_ids', None)
    request.session.pop('current_index', None)
    request.session.pop('answers', None)
    request.session.modified = True
    
    context = {
        'student_name': student_name,
        'score': score,
        'total_questions': total_questions,
        'results': results,
    }
    return render(request, 'student/results.html', context)