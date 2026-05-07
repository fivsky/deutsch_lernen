import json
import random
import os

# ------------------- СЛОВА (500) -------------------
words_data = []
word_id = 1

# Базовые слова (первые 100 — пример, дальше генерируем комбинациями)
base_words = [
    ("der Tisch", "стол", "Substantiv", "Der Tisch ist groß.", "A1"),
    ("die Sonne", "солнце", "Substantiv", "Die Sonne scheint.", "A1"),
    ("laufen", "бегать", "Verb", "Ich laufe schnell.", "A1"),
    ("schnell", "быстрый", "Adjektiv", "Das Auto ist schnell.", "A1"),
    ("arbeiten", "работать", "Verb", "Er arbeitet viel.", "A1"),
    ("das Buch", "книга", "Substantiv", "Das Buch ist interessant.", "A1"),
    ("lesen", "читать", "Verb", "Sie liest jeden Tag.", "A1"),
    ("schön", "красивый", "Adjektiv", "Das Wetter ist schön.", "A1"),
    ("die Stadt", "город", "Substantiv", "Die Stadt ist laut.", "A1"),
    ("fahren", "ехать", "Verb", "Wir fahren nach Berlin.", "A1"),
]

# Повторяем и модифицируем, чтобы получить ~500 слов
for i in range(500):
    base = base_words[i % len(base_words)]
    german, russian, pos, example, level = base
    if i // len(base_words) > 0:
        german = german + str(i // len(base_words))
        russian = russian + " (вар. {})".format(i // len(base_words))
        example = example.replace(".", " – вариант {}.".format(i // len(base_words)))
    words_data.append({
        "model": "language.word",
        "pk": i+1,
        "fields": {
            "german": german,
            "russian": russian,
            "part_of_speech": pos,
            "example": example,
            "level": level
        }
    })

# ------------------- ТЕКСТЫ (20) -------------------
texts_data = []
text_templates = [
    ("Meine Familie", "Ich heiße Anna. Meine Familie ist nicht groß. Meine Mutter arbeitet als Ärztin, mein Vater ist Lehrer. Ich habe einen Bruder.", "A1", [{"question": "Wie heißt die Person?", "answer": "Anna"}, {"question": "Was arbeitet die Mutter?", "answer": "Ärztin"}]),
    ("Mein Tag", "Morgens stehe ich um 7 Uhr auf. Dann dusche ich und frühstücke. Um 8 Uhr gehe ich zur Arbeit.", "A1", [{"question": "Wann stehe ich auf?", "answer": "um 7 Uhr"}, {"question": "Was mache ich um 8 Uhr?", "answer": "zur Arbeit gehen"}]),
    ("Im Café", "Gestern war ich in einem Café. Ich bestellte einen Kaffee und ein Stück Kuchen. Es war sehr lecker.", "A1", [{"question": "Was bestellte ich?", "answer": "einen Kaffee und ein Stück Kuchen"}, {"question": "Wie war es?", "answer": "lecker"}]),
]
# Генерируем 20 текстов, повторяя шаблоны с вариациями
for i in range(20):
    template = text_templates[i % len(text_templates)]
    title = f"{template[0]} {i+1}"
    content = template[1] + f" (версия {i+1})"
    questions = template[3]
    texts_data.append({
        "model": "language.text",
        "pk": i+1,
        "fields": {
            "title": title,
            "content": content,
            "level": "A1",
            "questions": questions
        }
    })

# ------------------- УПРАЖНЕНИЯ (100) -------------------
exercises_data = []
for i in range(100):
    word = words_data[i % len(words_data)]
    german = word['fields']['german']
    russian = word['fields']['russian']
    exercises_data.append({
        "model": "language.exercise",
        "pk": i+1,
        "fields": {
            "word": word['pk'],
            "question": f"Переведите слово '{german}'",
            "correct_answer": russian,
            "answer_type": "input"
        }
    })

# ------------------- СОХРАНЕНИЕ ФАЙЛОВ -------------------
fixtures_dir = os.path.join(os.path.dirname(__file__), 'language', 'fixtures')
os.makedirs(fixtures_dir, exist_ok=True)

with open(os.path.join(fixtures_dir, 'words_500.json'), 'w', encoding='utf-8') as f:
    json.dump(words_data, f, ensure_ascii=False, indent=2)

with open(os.path.join(fixtures_dir, 'texts_20.json'), 'w', encoding='utf-8') as f:
    json.dump(texts_data, f, ensure_ascii=False, indent=2)

with open(os.path.join(fixtures_dir, 'exercises_100.json'), 'w', encoding='utf-8') as f:
    json.dump(exercises_data, f, ensure_ascii=False, indent=2)

print("✅ Готово! Файлы созданы в language/fixtures/")


