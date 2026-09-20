#!/usr/bin/env python3
"""點入八字門教學站 v3 - 完整構建"""
import json, html

BASE = '/tmp/book_ocr/bazi-door-learn-v2'

def load(name):
    with open(f'{BASE}/{name}') as f:
        return json.load(f)

def svg(name):
    with open(f'{BASE}/assets/{name}.svg') as f:
        return f.read()

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

# ===== Quiz JS =====
quiz_lines = []
for i in range(1, 10):
    quiz_lines.append(f'  "quiz{i}": {quiz_json(f"quiz{i}")},')
quiz_js = '{\n' + '\n'.join(quiz_lines) + '\n}'

# ===== SVGs =====
svg_5el = svg('5elements')
svg_pillars = svg('pillars')
svg_10gods = svg('10gods')
svg_zodiac = svg('zodiac')

# ===== Lesson diagrams =====
# Map lesson -> SVG
diagram_map = {
    'lesson1': svg_pillars,
    'lesson2': svg_zodiac,
    'lesson3': svg_pillars,
    'lesson4': svg_5el,
    'lesson5': svg_10gods,
    'lesson6': svg_5el,
    'lesson7': svg_10gods,
    'lesson8': svg_5el,
    'lesson9': svg_10gods,
}

# ===== HTML helpers =====
def esc(s):
    return html.escape(s)

def render_section(sec, idx):
    parts = []
    parts.append(f'<div class="sub-section"><h3>{idx}. {esc(sec["title"])}</h3>')
    parts.append(f'<p>{esc(sec["content"])}</p>')
    if 'example' in sec and sec['example']:
        parts.append(f'<div class="tip"><strong>📌 概念舉例</strong><p>{esc(sec["example"])}</p></div>')
    parts.append('</div>')
    return '\n'.join(parts)

def render_lesson(lv_idx, lesson, lesson_num):
    parts = []
    parts.append(f'<div class="lesson-card" id="{lesson["id"]}">')
    parts.append(f'<div class="lesson-header"><span class="lesson-badge">第{lesson_num}課</span><h2>{esc(lesson["title"])}</h2></div>')
    
    # Objectives
    parts.append('<div class="objectives"><h3>🎯 學習目標</h3><ul>')
    for o in lesson['objectives']:
        parts.append(f'<li>{esc(o)}</li>')
    parts.append('</ul></div>')
    
    # Sections
    for idx, sec in enumerate(lesson['sections'], 1):
        parts.append(render_section(sec, idx))
    
    # Diagram (after first section)
    if lesson['id'] in diagram_map:
        parts.append(f'<div class="diagram-wrap">{diagram_map[lesson["id"]]}<div class="caption">↑ 本課核心概念圖示</div></div>')
    
    # Quiz
    qid = f'quiz{lesson_num}'
    parts.append(f'<div class="quiz-box"><h3>📝 課後練習（{len(quizzes.get(qid, []))} 題）</h3><div id="{qid}"></div></div>')
    parts.append('</div>')
    return '\n'.join(parts)

# ===== Build level HTML =====
levels_html = []
for lv_idx, lv in enumerate(content['levels']):
    cls = "active" if lv_idx == 0 else ""
    inner = []
    for l_idx, lesson in enumerate(lv['lessons']):
        lesson_num = lv_idx * 3 + l_idx + 1
        inner.append(render_lesson(lv_idx, lesson, lesson_num))
    levels_html.append(f'<div id="{lv["id"]}" class="level-content {cls}">' + '\n'.join(inner) + '</div>')

# ===== TOC =====
toc_rows = []
for lv_idx, lv in enumerate(content['levels']):
    for l_idx, lesson in enumerate(lv['lessons']):
        lesson_num = lv_idx * 3 + l_idx + 1
        qn = len(quizzes.get(f'quiz{lesson_num}', []))
        toc_rows.append(f'<tr><td class="lv">{lv["emoji"]} {lv["name"]}</td><td><a href="#{lesson["id"]}">{lesson_num}. {lesson["title"]}</a></td><td style="text-align:right;color:#887a6a">{qn} 題</td></tr>')

toc_html = '<table>' + '\n'.join(toc_rows) + '</table>'

# ===== Drawer links =====
drawer_lines = ['<a href="#index" onclick="closeMenu()">📖 課程索引</a>']
for lv in content['levels']:
    drawer_lines.append(f'<div style="color:#c89b3c;font-weight:700;margin-top:12px">{lv["emoji"]} {lv["name"]}級</div>')
    for l_idx, lesson in enumerate(lv['lessons']):
        drawer_lines.append(f'<a href="#{lesson["id"]}" onclick="closeMenu()">{lesson["title"]}</a>')
drawer_lines.append('<a href="#appendix" onclick="closeMenu()">📄 附錄</a>')

# ===== JS =====
JS = f"""const quizzes = {quiz_js};

Object.keys(quizzes).forEach(qid => {{
  const el = document.getElementById(qid);
  if (!el) return;
  const qs = quizzes[qid];
  qs.forEach((q, qi) => {{
    let h = `<div class="quiz-q" data-i="${{qi}}"><label>${{qi+1}}. ${{q.q}}</label>`;
    q.opts.forEach((opt, oi) => {{
      h += `<span class="quiz-opt" onclick="sel(this,${{qi}},${{oi}},'${{qid}}')">${{String.fromCharCode(65+oi)}}. ${{opt}}</span>`;
    }});
    h += `<div class="explain" id="${{qid}}_e${{qi}}">${{q.explain}}</div></div>`;
    el.innerHTML += h;
  }});
  el.innerHTML += `<button class="check-btn" onclick="chk('${{qid}}')">提交答案</button><div class="score-bar" id="${{qid}}_s"></div>`;
}});

const _s = {{}};
function sel(el, qi, oi, qid) {{
  _s[`${{qid}}_${{qi}}`] = oi;
  el.closest('.quiz-q').querySelectorAll('.quiz-opt').forEach(o => o.classList.remove('selected'));
  el.classList.add('selected');
}}
function chk(qid) {{
  const qs = quizzes[qid], c = qs.reduce((n, q, qi) => {{
    const s = _s[`${{qid}}_${{qi}}`];
    document.querySelectorAll(`#${{qid}} .quiz-q[data-i="${{qi}}"] .quiz-opt`).forEach((o, oi) => {{
      o.classList.remove('selected');
      if (oi === q.ans) o.classList.add('correct');
      else if (oi === s) o.classList.add('wrong');
    }});
    if (s === q.ans) n++;
    document.getElementById(`${{qid}}_e${{qi}}`).classList.add('show');
    return n;
  }}, 0);
  const sc = document.getElementById(`${{qid}}_s`);
  const pct = Math.round(c/qs.length*100);
  const msg = pct === 100 ? '🌟 滿分，完美掌握！' : pct >= 80 ? '👍 優良，再鞏固一下！' : pct >= 60 ? '🙂 合格，請複習重點。' : '💪 建議重溫本課。';
  sc.textContent = `得分：${{c}}/${{qs.length}}（${{pct}}%）— ${{msg}}`;
  sc.classList.add('show');
  sc.scrollIntoView({{behavior:'smooth',block:'nearest'}});
}}
function showLevel(lv, el) {{
  document.querySelectorAll('.level-content').forEach(x => x.classList.remove('active'));
  document.querySelectorAll('.level-tab').forEach(x => x.classList.remove('active'));
  document.getElementById(lv).classList.add('active');
  el.classList.add('active');
  window.scrollTo({{top:document.getElementById('levels').offsetTop - 60,behavior:'smooth'}});
}}
window.addEventListener('scroll',()=>{{document.getElementById('toTop').classList.toggle('show',window.scrollY>400)}});
function toTop(){{window.scrollTo({{top:0,behavior:'smooth'}})}}
function openMenu(){{document.getElementById('drawer').classList.add('open');document.getElementById('ovl').classList.add('show')}}
function closeMenu(){{document.getElementById('drawer').classList.remove('open');document.getElementById('ovl').classList.remove('show')}}
"""

# ===== Full HTML =====
CSS = """
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}body{font-family:'LXGW WenKai','Noto Sans TC',sans-serif;background:#14121c;color:#e8e0d0;line-height:1.9;min-height:100vh}.hero{background:linear-gradient(135deg,#2a1f3d 0%,#14121c 50%,#2d1f2f 100%);text-align:center;padding:70px 20px 50px;border-bottom:2px solid #c89b3c;position:relative;overflow:hidden}.hero::before{content:"";position:absolute;top:-50%;left:-20%;width:140%;height:200%;background:radial-gradient(ellipse at 30% 20%,rgba(200,155,60,0.08),transparent 60%);pointer-events:none}.hero h1{font-size:3rem;color:#ffd700;text-shadow:0 2px 12px rgba(255,215,0,0.35);margin-bottom:10px;letter-spacing:4px}.hero .subtitle{font-size:1.15rem;color:#b8a88a;margin-bottom:8px}.hero .author{font-size:0.9rem;color:#887a6a}.hero .tag{display:inline-block;margin-top:14px;padding:6px 18px;border:1px solid #c89b3c;border-radius:20px;color:#c89b3c;font-size:0.85rem;letter-spacing:2px}nav.sticky{position:sticky;top:0;z-index:100;background:rgba(20,18,28,0.95);backdrop-filter:blur(8px);border-bottom:1px solid #3a3040;padding:10px 16px;display:flex;gap:8px;flex-wrap:wrap;justify-content:center}nav.sticky a{color:#b8a88a;text-decoration:none;padding:6px 14px;border-radius:20px;font-size:0.9rem;transition:all .2s}nav.sticky a:hover{background:#3d2f50;color:#ffd700}.container{max-width:960px;margin:0 auto;padding:20px 16px}.toc{background:#1e1a28;border:1px solid #3a3040;border-radius:12px;padding:24px;margin:24px 0}.toc h2{color:#c89b3c;font-size:1.3rem;margin-bottom:14px;text-align:center}.toc table{width:100%;border-collapse:collapse}.toc td{padding:8px;border-bottom:1px solid #2a2430;color:#d0c8b8}.toc td a{color:#e8c868;text-decoration:none}.toc td a:hover{text-decoration:underline}.toc .lv{font-weight:700;color:#ffd700;width:70px}.level-tabs{display:flex;gap:8px;margin:28px 0 20px;flex-wrap:wrap;justify-content:center}.level-tab{padding:12px 24px;border-radius:25px;cursor:pointer;font-weight:700;font-size:1rem;border:2px solid #444;background:#2a2030;color:#b8a88a;transition:all .3s}.level-tab.active{background:#3d2f50;border-color:#c89b3c;color:#ffd700;box-shadow:0 0 15px rgba(200,155,60,0.2)}.level-tab:hover{border-color:#c89b3c}.level-content{display:none}.level-content.active{display:block;animation:fadeIn .4s ease}@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}.lesson-card{background:#1e1a28;border:1px solid #3a3040;border-radius:14px;padding:26px;margin-bottom:26px;scroll-margin-top:70px}.lesson-header{display:flex;align-items:center;gap:12px;margin-bottom:16px}.lesson-header h2{color:#c89b3c;font-size:1.5rem;flex:1}.lesson-badge{background:#c89b3c;color:#14121c;padding:4px 12px;border-radius:20px;font-size:0.8rem;font-weight:700}.objectives{background:linear-gradient(135deg,#2d3a2d,#1a2a1a);border:1px solid #4a6a3a;border-radius:10px;padding:18px;margin-bottom:22px}.objectives h3{color:#7cba5a;margin-bottom:10px;font-size:1.05rem}.objectives li{margin:6px 0 6px 18px;color:#d0c8b8}.sub-section{background:#221d2e;border-radius:10px;padding:18px 20px;margin-bottom:14px;border-left:3px solid #3a3040;transition:border-color .2s}.sub-section:hover{border-left-color:#c89b3c}.sub-section h3{color:#e8c868;font-size:1.1rem;margin-bottom:10px}.sub-section p{color:#d0c8b8;margin-bottom:10px;line-height:2}.sub-section p:last-child{margin-bottom:0}.tip{background:#2a2438;border-left:4px solid #8a6ad0;border-radius:8px;padding:14px 18px;margin:14px 0 4px}.tip strong{color:#b89ae0;display:block;margin-bottom:6px}.tip p{color:#c8b8d8;margin:0}.diagram-wrap{background:#1a1625;border:1px solid #3a3040;border-radius:10px;padding:16px;margin:18px 0;text-align:center;overflow-x:auto}.diagram-wrap svg{max-width:100%;max-height:340px}.diagram-wrap .caption{font-size:0.85rem;color:#887a6a;margin-top:8px}.quiz-box{background:#201828;border:1px solid #5a3a6a;border-radius:14px;padding:24px;margin-top:24px}.quiz-box h3{color:#d8a0f0;margin-bottom:16px;font-size:1.2rem}.quiz-q{margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid #2a2430}.quiz-q:last-of-type{border-bottom:none}.quiz-q label{font-weight:600;color:#c8b8a8;display:block;margin-bottom:8px;font-size:1.02rem}.quiz-opt{display:block;padding:9px 14px;margin:5px 0;border-radius:8px;cursor:pointer;background:#2a2030;border:1px solid #444;color:#b8a88a;transition:all .15s}.quiz-opt:hover{border-color:#c89b3c;background:#352a40}.quiz-opt.selected{border-color:#c89b3c;background:#3d2f50;color:#ffd700}.quiz-opt.correct{border-color:#4a6a3a;background:#2d3a2d;color:#7cba5a;animation:pulse .4s}.quiz-opt.wrong{border-color:#6a3a3a;background:#3a2020;color:#d86060}@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.03)}100%{transform:scale(1)}}.check-btn{margin-top:14px;padding:12px 30px;border:none;border-radius:25px;background:linear-gradient(135deg,#c89b3c,#a07828);color:#14121c;font-weight:700;font-size:1.02rem;cursor:pointer;transition:all .2s}.check-btn:hover{background:linear-gradient(135deg,#d8ab4c,#b08838);transform:translateY(-1px)}.explain{margin-top:10px;padding:12px 14px;background:#1a1a2e;border-radius:8px;color:#b8a88a;font-size:0.95rem;display:none;border-left:3px solid #5a3a6a}.explain.show{display:block;animation:fadeIn .3s}.score-bar{margin-top:16px;padding:13px 16px;background:#252030;border-radius:10px;color:#c8b8a8;font-weight:600;display:none}.score-bar.show{display:block;animation:fadeIn .3s}.back-top{position:fixed;bottom:30px;right:30px;width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#c89b3c,#a07828);color:#14121c;border:none;font-size:1.5rem;cursor:pointer;opacity:0;pointer-events:none;transition:all .3s;z-index:200;box-shadow:0 4px 15px rgba(0,0,0,0.4)}.back-top.show{opacity:1;pointer-events:auto}.back-top:hover{transform:translateY(-3px)}footer{text-align:center;padding:36px 20px;color:#6a5a4a;font-size:0.88rem;border-top:1px solid #2a2430;margin-top:40px}.drawer{position:fixed;top:0;right:-320px;width:300px;height:100%;background:#1e1a28;z-index:300;transition:right .3s;padding:24px;overflow-y:auto;border-left:1px solid #c89b3c}.drawer.open{right:0}.drawer h3{color:#ffd700;margin-bottom:16px}.drawer a{display:block;color:#d0c8b8;text-decoration:none;padding:8px 0;border-bottom:1px solid #2a2430}.drawer a:hover{color:#e8c868}.menu-btn{position:fixed;bottom:30px;left:30px;width:52px;height:52px;border-radius:50%;background:#3d2f50;color:#ffd700;border:1px solid #c89b3c;font-size:1.3rem;cursor:pointer;z-index:200;box-shadow:0 4px 15px rgba(0,0,0,0.4)}.overlay{position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:250;display:none}.overlay.show{display:block}.flow-arrow{animation:flowing 2.5s ease-in-out infinite}@keyframes flowing{0%,100%{opacity:0.4}50%{opacity:1}}.flow-arrow2{animation:flowing 3s ease-in-out infinite 0.5s}@media(max-width:640px){.hero h1{font-size:2.1rem}.container{padding:14px 10px}}
"""

page = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{content['title']} — 教學站</title>
<style>{CSS}</style>
<link href="https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@400;700&family=Noto+Sans+TC:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
<div class="hero">
<h1>{content['title']}</h1>
<div class="subtitle">{content['subtitle']} — 三級九課循序漸進</div>
<span class="tag">📚 全書九課 · 180 題課後練習 · 深度 OCR 製作</span>
<div class="author" style="margin-top:10px">原著：{content['author']} ／ {content['publisher']}</div>
</div>
<nav class="sticky">
<a href="#index">📖 課程索引</a>
<a href="#lv1">🌱 初級</a>
<a href="#lv2">🔥 中級</a>
<a href="#lv3">🧭 高級</a>
<a href="#appendix">📄 附錄</a>
</nav>
<div class="container">
<div class="toc" id="index"><h2>📖 課程索引</h2>{toc_html}</div>
<div class="level-tabs" id="levels">
<div class="level-tab active" onclick="showLevel('lv1',this)">🌱 初級（第1-3課）</div>
<div class="level-tab" onclick="showLevel('lv2',this)">🔥 中級（第4-6課）</div>
<div class="level-tab" onclick="showLevel('lv3',this)">🧭 高級（第7-9課）</div>
</div>
{"".join(levels_html)}
<div id="appendix" class="lesson-card">
<div class="lesson-header"><span class="lesson-badge">附錄</span><h2>📄 附錄：全書章節溫習</h2></div>
<div class="sub-section"><h3>附錄一：重要口訣一覽</h3>
<p><strong>五虎遁年起月</strong>：甲己之年丙作首，乙庚之歲戊為頭，丙辛歲首尋庚起，丁壬壬位順行流，戊癸何方發，甲寅之上好追求。</p>
<p><strong>五鼠遁日起時</strong>：甲己還加甲，乙庚丙子初，丙辛從戊起，丁壬庚子居，戊癸何方發，壬子是真途。</p>
<p><strong>天干五合</strong>：甲己合化土，乙庚合化金，丙辛合化水，丁壬合化木，戊癸合化火。</p>
<p><strong>地支六合</strong>：子丑合土，寅亥合木，卯戌合火，辰酉合金，巳申合水，午未合火土。</p>
<p><strong>五行相生</strong>：木生火、火生土、土生金、金生水、水生木。</p>
<p><strong>五行相剋</strong>：金剋木、木剋土、土剋水、水剋火、火剋金。</p>
<p><strong>斷事金句</strong>：現象從天干看，實力從地支尋；喜神為輔弼，忌神輾轉攻。</p>
</div>
<div class="sub-section"><h3>附錄二：十天干十二地支速查</h3>
<p>天干：甲乙（木）、丙丁（火）、戊己（土）、庚辛（金）、壬癸（水）。陽干：甲丙戊庚壬；陰干：乙丁己辛癸。</p>
<p>地支：亥子（水）、寅卯（木）、巳午（火）、申酉（金）、辰戌丑未（土）。陽支：子寅辰午申戌；陰支：丑卯巳未酉亥。</p>
</div>
<div class="sub-section"><h3>附錄三：排盤步驟</h3>
<p>1. 查年柱（立春為界）→ 2. 查日柱（萬年曆）→ 3. 起月柱（五虎遁）→ 4. 起時柱（五鼠遁）→ 5. 排大運 → 6. 配十神 → 7. 定旺弱（三審法）→ 8. 分喜忌（用神）。</p>
</div>
<div class="sub-section"><h3>附錄四：OCR 原文備份</h3>
<p>本站內容皆由全書 128 頁掃描件深度 OCR 提取製作，原文共提取約 51,000 字。</p>
<p><a href="appendix.html" style="display:inline-block;margin-top:10px;padding:10px 24px;background:linear-gradient(135deg,#c89b3c,#a07828);color:#14121c;border-radius:25px;text-decoration:none;font-weight:700">📄 查看全書 OCR 原文附錄</a></p>
</div>
</div>
</div>
<button class="menu-btn" onclick="openMenu()">☰</button>
<button class="back-top" id="toTop" onclick="toTop()">↑</button>
<div class="overlay" id="ovl" onclick="closeMenu()"></div>
<div class="drawer" id="drawer">
<h3>📖 快速導航</h3>
{"".join(drawer_lines)}
</div>
<footer>
<p>本站內容節選自 {content['author']}《{content['title']}》（{content['publisher']}），僅作教育學習參考。</p>
<p>深度 OCR 製作 · 教學站 v3 · 2026</p>
</footer>
<script>{JS}</script>
</body>
</html>"""

with open(f'{BASE}/index.html', 'w') as f:
    f.write(page)
print(f"Built v3: {len(page)} bytes")
