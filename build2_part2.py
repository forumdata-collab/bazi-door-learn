#!/usr/bin/env python3
"""Part 2: Generate quiz JS and HTML structure"""
import json, re

BASE = '/tmp/book_ocr/bazi-door-learn-v2'

def load(name):
    with open(f'{BASE}/{name}') as f:
        return json.load(f)

content = load('content.json')
quizzes = {}
for i in range(1, 10):
    quizzes[f'quiz{i}'] = load(f'quiz{i}.json')

def quiz_json(qid):
    qs = quizzes.get(qid, [])
    arr = []
    for q in qs:
        opts = '","'.join(q['opts'])
        q_safe = q['q'].replace('"', '\\"')
        e_safe = q['explain'].replace('"', '\\"').replace('\n', ' ')
        arr.append(f'{{q:"{q_safe}",opts:["{opts}"],ans:{q["ans"]},explain:"{e_safe}"}}')
    return '[' + ','.join(arr) + ']'

# Build quiz JS
quiz_js_lines = []
for i in range(1, 10):
    qid = f'quiz{i}'
    quiz_js_lines.append(f'  "{qid}": {quiz_json(qid)},')
quiz_js = '\n'.join(quiz_js_lines)

print(f"Quiz JS: {len(quiz_js)} chars, keys: {len(quiz_js_lines)}")

# Verify each quiz has 20 questions
for i in range(1, 10):
    print(f"  quiz{i}: {len(quizzes[f'quiz{i}'])} questions")
