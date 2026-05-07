from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Word, Text, Exercise, UserWord, UserProgress

# ========== ОБЩИЙ КОНТЕКСТ ДЛЯ БОКОВОЙ ПАНЕЛИ ==========
def common_context(request):
    ctx = {
        'total_words': Word.objects.count(),
        'total_texts': Text.objects.count(),
        'total_exercises': Exercise.objects.count(),
        'random_word': Word.objects.order_by('?').first(),
    }
    if request.user.is_authenticated:
        progress, _ = UserProgress.objects.get_or_create(user=request.user)
        ctx['user_progress'] = {'points': progress.total_points}
    else:
        ctx['user_progress'] = {'points': 0}
    return ctx

# ========== СЛОВАРЬ (список слов) ==========
def word_list(request):
    ctx = common_context(request)
    ctx['words'] = Word.objects.all()
    return render(request, 'language/word_list.html', ctx)

# ========== ТРЕНАЖЁР (карточки) ==========
@login_required
def trainer(request):
    ctx = common_context(request)
    word = None
    word_id = request.GET.get('word_id')
    if word_id:
        word = get_object_or_404(Word, pk=word_id)
    else:
        # Случайное слово (которое ещё не выучено — опционально)
        user_words = UserWord.objects.filter(user=request.user, known=True).values_list('word_id', flat=True)
        word = Word.objects.exclude(id__in=user_words).order_by('?').first()
        if not word:
            word = Word.objects.order_by('?').first()
    if request.method == 'POST':
        known = request.POST.get('known') == 'true'
        uw, created = UserWord.objects.get_or_create(user=request.user, word=word)
        uw.known = known
        uw.repetition_count += 1
        uw.save()
        progress, _ = UserProgress.objects.get_or_create(user=request.user)
        if known and not created and not uw.known:
            progress.words_learned += 1
        progress.total_points += 1 if known else 0
        progress.save()
        return redirect('language:trainer')
    ctx['word'] = word
    return render(request, 'language/trainer.html', ctx)

# ========== СПИСОК ТЕКСТОВ ==========
def text_list(request):
    ctx = common_context(request)
    ctx['texts'] = Text.objects.all()
    return render(request, 'language/text_list.html', ctx)

# ========== ДЕТАЛЬНАЯ СТРАНИЦА ТЕКСТА С ВОПРОСАМИ ==========
@login_required
def text_detail(request, pk):
    ctx = common_context(request)
    text = get_object_or_404(Text, pk=pk)
    if request.method == 'POST':
        score = 0
        for i, q in enumerate(text.questions):
            user_answer = request.POST.get(f'q{i}', '')
            if user_answer.strip().lower() == q['answer'].lower():
                score += 1
        progress, _ = UserProgress.objects.get_or_create(user=request.user)
        progress.texts_completed += 1
        progress.total_points += score
        progress.save()
        return render(request, 'language/text_result.html', {'score': score, 'total': len(text.questions)})
    ctx['text'] = text
    return render(request, 'language/text_detail.html', ctx)

# ========== СПИСОК УПРАЖНЕНИЙ ==========
def exercise_list(request):
    ctx = common_context(request)
    ctx['exercises'] = Exercise.objects.all()
    return render(request, 'language/exercise_list.html', ctx)

# ========== ДЕТАЛЬНАЯ СТРАНИЦА УПРАЖНЕНИЯ ==========
@login_required
def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    result = None
    if request.method == 'POST':
        answer = request.POST.get('answer', '').strip()
        if answer.lower() == exercise.correct_answer.lower():
            result = True
            # начисляем очки (если нужны)
            if request.user.is_authenticated:
                progress, _ = UserProgress.objects.get_or_create(user=request.user)
                progress.total_points += 5
                progress.save()
        else:
            result = False
    ctx = common_context(request)
    ctx['exercise'] = exercise
    ctx['result'] = result
    return render(request, 'language/exercise_detail.html', ctx)

# ========== ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ ==========
@login_required
def profile(request):
    ctx = common_context(request)
    progress, _ = UserProgress.objects.get_or_create(user=request.user)
    ctx['progress'] = progress
    return render(request, 'language/profile.html', ctx)

# ========== РЕГИСТРАЦИЯ ==========
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('language:word_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

