from django.contrib import admin
from .models import QuizCategory, Question, Quiz
from .models import Quiz, QuizCategory
from django.shortcuts import render, get_object_or_404

@admin.register(QuizCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'get_category')  # Додаємо 'get_category' для відображення категорії
    search_fields = ('text',)  # Поля, за якими можна буде шукати

    def get_category(self, obj):
        """Виводимо категорію через пов'язану модель Quiz."""
        return obj.quiz.category.name if obj.quiz and obj.quiz.category else "Без категорії"
    get_category.short_description = 'Категорія'  # Назва стовпця в адмінці

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'difficulty')
    search_fields = ('name', 'description')

def quizzes_by_difficulty(request, category_id, difficulty):
    category = get_object_or_404(QuizCategory, id=category_id)
    quizzes = Quiz.objects.filter(category=category, difficulty=difficulty)
    return render(request, 'quizzes_by_difficulty.html', {'category': category, 'quizzes': quizzes})

