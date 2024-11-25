from django.urls import path
from .views import (
    home,
    CategoryListView,
    DifficultyLevelView,
    QuizListView,
    QuizDetailView,
    QuestionListView,
    LeaderboardView,
    LeaderboardAPIView,
    quizzes_by_difficulty,
    quiz_detail,
    start_quiz,
    generate_quiz_question,
)

urlpatterns = [
    # Головна сторінка
    path('', home, name='home'),

    # Категорії вікторин
    path('categories/', CategoryListView.as_view(), name='quiz_category_list'),

    # Рівні складності для категорій
    path('categories/<int:category_id>/difficulty/', DifficultyLevelView.as_view(), name='difficulty_list'),

    # Список вікторин за категорією та рівнем складності
    path('categories/<int:category_id>/difficulty/<int:difficulty>/quizzes/',
         quizzes_by_difficulty, name='quizzes_by_difficulty'),

    # Деталі вікторини
    path('quiz/<int:quiz_id>/', quiz_detail, name='quiz_detail'),

    # Почати вікторину
    path('quiz/<int:quiz_id>/start/', start_quiz, name='start_quiz'),

    # Список питань у вікторині
    path('questions/<int:quiz_id>/', QuestionListView.as_view(), name='question_list'),

    # Рейтинг
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('leaderboard/api/', LeaderboardAPIView.as_view(), name='leaderboard_api'),

    # Генерація питання через ШІ
    path('api/generate-question/', generate_quiz_question, name='generate_question'),

]
