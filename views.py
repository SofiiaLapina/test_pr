from rest_framework import generics
from django.contrib.auth.models import User
from .models import Question, QuizCategory, Quiz
from .serializers import QuizCategorySerializer
from users.serializers import UserSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from django.conf import settings
import openai
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import json

# Налаштування OpenAI
openai.api_key = settings.OPENAI_API_KEY


# Домашня сторінка
def home(request):
    categories = QuizCategory.objects.all()
    top_users = User.objects.all().order_by('-userprofile__score')[:10]
    return render(request, 'home.html', {
        'categories': categories,
        'top_users': top_users,
    })


# Список категорій вікторин
class CategoryListView(generics.ListAPIView):
    queryset = QuizCategory.objects.all()
    serializer_class = QuizCategorySerializer


# Вибір рівня складності
class DifficultyLevelView(View):
    def get(self, request, category_id):
        category = get_object_or_404(QuizCategory, id=category_id)
        return render(request, 'difficulty.html', {'category': category})


# Список вікторин за категорією та рівнем складності
def quizzes_by_difficulty(request, category_id, difficulty):
    category = get_object_or_404(QuizCategory, id=category_id)
    quizzes = Quiz.objects.filter(category=category, difficulty=difficulty)
    return render(request, 'quizzes_by_difficulty.html', {
        'category': category,
        'difficulty': difficulty,
        'quizzes': quizzes
    })

# Список вікторин
class CategoryListView(View):
    def get(self, request):
        categories = QuizCategory.objects.all()
        return render(request, 'categories.html', {'categories': categories})


# Деталі вікторини
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz_detail.html', {'quiz': quiz})



# Генерація запитань для вікторини
def generate_quiz_question(request):
    category = request.GET.get('category', 'Загальні знання')
    difficulty = request.GET.get('difficulty', 'Легкий')

    prompt = f"""
    Згенеруй 10 питання для вікторини з теми '{category}' та рівнем складності '{difficulty}'.
    Формат:
    {{
        "question": "Текст питання",
        "options": ["Варіант 1", "Варіант 2", "Варіант 3", "Варіант 4"],
        "correct_answer": "Правильна відповідь"
    }}
    """
    try:
        response = openai.Completion.create(
            engine="gpt-neo-1-3b",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        question_data = json.loads(response.choices[0].text.strip())
        return JsonResponse({"question": question_data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Почати вікторину
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Генерація питань
    questions = generate_questions_for_quiz(quiz)

    if not questions:  # Якщо питання не згенеровані
        return JsonResponse({"error": "Не вдалося згенерувати питання. Спробуйте пізніше."}, status=500)

    # Збереження в сесію
    try:
        request.session['quiz'] = {
            'quiz_id': quiz_id,
            'questions': questions,
            'current_question_index': 0,
            'score': 0,
        }
    except Exception as e:
        print(f"Помилка збереження в сесію: {e}")
        return JsonResponse({"error": "Помилка збереження даних у сесію."}, status=500)

    return redirect(f"/api/quizzes/quiz/{quiz_id}/question/0/")

class QuizDetailView(View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        return render(request, 'quiz_detail.html', {'quiz': quiz})


class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz_list.html'
    context_object_name = 'quizzes'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        difficulty = self.kwargs.get('difficulty')
        return Quiz.objects.filter(category_id=category_id, difficulty=difficulty)


# Таблиця лідерів (HTML)
class LeaderboardView(View):
    """
    Відображає топ-10 користувачів за кількістю набраних балів на веб-сторінці.
    """
    def get(self, request):
        top_users = User.objects.all().order_by('-userprofile__score')[:10]
        return render(request, 'leaderboard.html', {'users': top_users})


# Таблиця лідерів (API)
class LeaderboardAPIView(APIView):
    """
    API для отримання топ-10 користувачів за кількістю набраних балів.
    """
    def get(self, request):
        top_users = User.objects.all().order_by('-userprofile__score')[:10]
        serializer = UserSerializer(top_users, many=True)
        return Response(serializer.data)


class QuestionListView(ListView):
    model = Question
    template_name = 'questions.html'
    context_object_name = 'questions'

    def get_queryset(self):
        quiz_id = self.kwargs.get('quiz_id')
        return Question.objects.filter(quiz_id=quiz_id)

def show_results(request, quiz_id):
    quiz_data = request.session.pop('quiz', None)

    if not quiz_data or quiz_data['quiz_id'] != quiz_id:
        return redirect(f"/api/quizzes/quiz/{quiz_id}/start/")

    score = quiz_data['score']
    return render(request, 'results.html', {'score': score})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_answer(request, quiz_id, question_index):
    quiz_data = request.session.get('quiz')

    if not quiz_data or quiz_data['quiz_id'] != quiz_id:
        return redirect(f"/api/quizzes/quiz/{quiz_id}/start/")

    questions = quiz_data['questions']
    current_question = questions[question_index]
    user_answer = request.data.get('answer')
    correct_answer = current_question['correct_answer']

    if user_answer == correct_answer:
        difficulty = Quiz.objects.get(id=quiz_id).difficulty
        points = {1: 4, 2: 7, 3: 10}[difficulty]
        quiz_data['score'] += points

    quiz_data['current_question_index'] += 1
    request.session['quiz'] = quiz_data

    if question_index + 1 >= len(questions):
        return redirect(f"/api/quizzes/quiz/{quiz_id}/results/")

    return redirect(f"/api/quizzes/quiz/{quiz_id}/question/{question_index + 1}/")

def show_question(request, quiz_id, question_index):
    quiz_data = request.session.get('quiz')

    if not quiz_data or quiz_data['quiz_id'] != quiz_id:
        return redirect(f"/api/quizzes/quiz/{quiz_id}/start/")

    questions = quiz_data['questions']
    if question_index >= len(questions):
        return redirect(f"/api/quizzes/quiz/{quiz_id}/results/")

    current_question = questions[question_index]
    return render(request, 'question.html', {
        'question': current_question,
        'quiz_id': quiz_id,
        'question_index': question_index,
        'total_questions': len(questions),
        'time_limit': 30,
    })

# Генерація запитань для вікторини
import json

def generate_questions_for_quiz(quiz):
    questions = []
    for i in range(5):  # Генеруємо 5 питань
        prompt = f"""
        Згенеруй одне питання для вікторини "{quiz.name}".
        Опис: {quiz.description}.
        Категорія: {quiz.category.name}.
        Рівень складності: {quiz.get_difficulty_display()}.
        Формат (JSON):
        {{
            "question": "Текст питання",
            "options": ["Варіант 1", "Варіант 2", "Варіант 3", "Варіант 4"],
            "correct_answer": "Правильна відповідь"
        }}
        """
        try:
            response = openai.Completion.create(
                engine="gpt-neo-1-3b",
                prompt=prompt,
                max_tokens=300,
                temperature=0.7
            )
            response_text = response.choices[0].text.strip()
            question_data = json.loads(response_text)  # Перевірка відповідності JSON
            questions.append(question_data)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e} – відповідь: {response_text}")
        except Exception as e:
            print(f"Помилка генерації питання: {e}")
    return questions if len(questions) == 5 else []

def generate_questions_with_retry(quiz, retries=3):
    for attempt in range(retries):
        questions = generate_questions_for_quiz(quiz)
        if questions:  # Успіх
            return questions
        print(f"Спроба {attempt + 1} не вдалася. Повторюємо...")
    return []  # Якщо після всіх спроб немає результату


