import json

words = []
for i in range(1, 101):
    words.append({
        "model": "language.word",
        "pk": i,
        "fields": {
            "german": f"Wort{i}",
            "russian": f"Слово{i}",
            "part_of_speech": "noun",
            "example": f"Beispiel für Wort{i}.",
            "level": "A1"
        }
    })

texts = []
for i in range(1, 11):
    texts.append({
        "model": "language.text",
        "pk": i,
        "fields": {
            "title": f"Text {i}",
            "content": f"Inhalt von Text {i}. Das ist ein einfacher Text für A1.",
            "level": "A1",
            "questions": [{"question": f"Frage zu Text {i}?", "answer": "Antwort"}]
        }
    })

exercises = []
for i in range(1, 51):
    exercises.append({
        "model": "language.exercise",
        "pk": i,
        "fields": {
            "word": i % 100 + 1,
            "question": f"Übersetze 'Wort{i}'",
            "correct_answer": f"Слово{i}",
            "answer_type": "input"
        }
    })

full = words + texts + exercises
with open('full_data.json', 'w', encoding='utf-8') as f:
    json.dump(full, f, ensure_ascii=False, indent=2)

print("✅ full_data.json создан, содержит", len(words), "слов,", len(texts), "текстов,", len(exercises), "упражнений.")