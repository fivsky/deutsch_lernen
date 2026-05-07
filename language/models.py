from django.db import models
from django.contrib.auth.models import User

class Word(models.Model):
    german = models.CharField(max_length=100, unique=True)
    russian = models.CharField(max_length=200)
    part_of_speech = models.CharField(max_length=50, blank=True)
    example = models.TextField(blank=True)
    level = models.CharField(max_length=10, default='A1')

    def __str__(self):
        return f"{self.german} – {self.russian}"

class Text(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    level = models.CharField(max_length=10, default='A1')
    questions = models.JSONField(default=list)  # [{"question": "...", "answer": "..."}]

    def __str__(self):
        return self.title

class Exercise(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=200)
    answer_type = models.CharField(max_length=10, choices=[('choice', 'Выбор'), ('input', 'Ввод')], default='input')

    def __str__(self):
        return self.question[:50]

class UserWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    known = models.BooleanField(default=False)
    repetition_count = models.IntegerField(default=0)
    last_shown = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'word')

class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    words_learned = models.IntegerField(default=0)
    texts_completed = models.IntegerField(default=0)