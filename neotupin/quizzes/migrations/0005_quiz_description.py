# Generated by Django 5.1.3 on 2024-11-24 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizzes", "0004_quiz_delete_category_alter_question_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="description",
            field=models.TextField(
                blank=True, null=True, verbose_name="Опис вікторини"
            ),
        ),
    ]