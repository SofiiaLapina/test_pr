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
    if not request.user.is_authenticated:
        login_url = f"{settings.LOGIN_URL}?next={request.path}"
        return redirect(login_url)
    return render(request, 'quiz_detail.html', {'quiz': quiz})


# Генерація запитань для вікторини
def generate_quiz_question(request):
    category = request.GET.get('category', 'Загальні знання')
    difficulty = request.GET.get('difficulty', 'Легкий')

    prompt = f"""
    Згенеруй питання для вікторини з теми '{category}' та рівнем складності '{difficulty}'.
    Формат:
    {{
        "question": "Текст питання",
        "options": ["Варіант 1", "Варіант 2", "Варіант 3", "Варіант 4"],
        "correct_answer": "Правильна відповідь"
    }}
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        question_data = eval(response.choices[0].text.strip())
        return JsonResponse({"question": question_data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Почати вікторину
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Ви повинні увійти до акаунту."}, status=401)

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Згенеруй 15 питань для вікторини '{quiz.name}' із рівнем складності {quiz.get_difficulty_display()}",
            max_tokens=2000,
            temperature=0.7
        )
        questions = eval(response.choices[0].text.strip())
        return JsonResponse({"questions": questions})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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
