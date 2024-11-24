from django.db import models


class QuizCategory(models.Model):
    """
    Модель категорій вікторин.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name="Назва категорії")  # Унікальна назва категорії

    class Meta:
        verbose_name = "Категорія вікторини"
        verbose_name_plural = "Категорії вікторин"
        ordering = ['name']

    def __str__(self):
        return self.name


class Quiz(models.Model):
    """
    Модель вікторини.
    """
    DIFFICULTY_CHOICES = (
        (1, "Легкий"),
        (2, "Середній"),
        (3, "Важкий"),
    )

    name = models.CharField(max_length=255, unique=True, verbose_name="Назва вікторини")  # Унікальна назва вікторини
    category = models.ForeignKey(
        QuizCategory,
        on_delete=models.CASCADE,
        related_name="quizzes",
        verbose_name="Категорія"
    )
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, verbose_name="Рівень складності")

    class Meta:
        verbose_name = "Вікторина"
        verbose_name_plural = "Вікторини"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_difficulty_display()})"


class Question(models.Model):
    """
    Модель питань вікторини.
    """
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Вікторина"
    )
    text = models.TextField(unique=True, verbose_name="Текст питання")  # Унікальний текст питання
    correct_answer = models.CharField(max_length=255, verbose_name="Правильна відповідь")
    options = models.JSONField(help_text="Список варіантів відповідей у форматі JSON", verbose_name="Варіанти відповідей")

    class Meta:
        verbose_name = "Питання"
        verbose_name_plural = "Питання"
        ordering = ['quiz', 'id']

    def __str__(self):
        return f"Питання для вікторини '{self.quiz.name}': {self.text}"
