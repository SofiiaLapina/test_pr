from django.contrib import admin
from .models import QuizCategory, Question, Quiz
from django.shortcuts import render, get_object_or_404

# Адмінка для категорій вікторин
@admin.register(QuizCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Відображення ID і назви категорії
    search_fields = ('name',)  # Пошук за назвою категорії

# Адмінка для запитань
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'get_category')  # Додаємо 'get_category' для відображення категорії
    search_fields = ('text',)  # Поля, за якими можна буде шукати

    def get_category(self, obj):
        """Виводимо категорію через пов'язану модель Quiz."""
        return obj.quiz.category.name if obj.quiz and obj.quiz.category else "Без категорії"
    get_category.short_description = 'Категорія'  # Назва стовпця в адмінці

# Адмінка для вікторин
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'difficulty', 'description')  # Додано поле опису
    search_fields = ('name', 'category__name')  # Додаємо пошук за назвою вікторини та категорією
    list_filter = ('category', 'difficulty')  # Додаємо фільтри за категорією та складністю

