#!/usr/bin/env python3
"""點入八字門教學站 v2 - build script"""
import json, os, html

def load(name):
    with open(f'/tmp/book_ocr/bazi-door-learn-v2/{name}') as f:
        return json.load(f)

content = load('content.json')
quizzes = {}
for i in range(1, 10):
    quizzes[f'quiz{i}'] = load(f'quiz{i}.json')

css = """
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Noto Serif TC','Noto Sans TC',serif;background:#14121c;color:#e8e0d0;line-height:1.8;min-height:100vh}
.hero{background:linear-gradient(135deg,#2a1f3d 0%,#14121c 50%,#2d1f2f 100%);text-align:center;padding:70px 20px 50px;border-bottom:2px solid #c89b3c;position:relative;overflow:hidden}
.hero::before{content:"";position:absolute;top:-50%;left:-20%;width:140%;height:200%;background:radial-gradient(ellipse at 30% 20%,rgba(200,155,60,0.08),transparent 60%);pointer-events:none}
.hero h1{font-size:3rem;color:#ffd700;text-shadow:0 2px 12px rgba(255,215,0,0.35);margin-bottom:10px;letter-spacing:4px}
.hero .subtitle{font-size:1.15rem;color:#b8a88a;margin-bottom:8px}
.hero .author{font-size:0.9rem;color:#887a6a}
.hero .tag{display:inline-block;margin-top:14px;padding:6px 18px;border:1px solid #c89b3c;border-radius:20px;color:#c89b3c;font-size:0.85rem;letter-spacing:2px}
nav.sticky{position:sticky;top:0;z-index:100;background:rgba(20,18,28,0.95);backdrop-filter:blur(8px);border-bottom:1px solid #3a3040;padding:10px 16px;display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
nav.sticky a{color:#b8a88a;text-decoration:none;padding:6px 14px;border-radius:20px;font-size:0.9rem;transition:all .2s}
nav.sticky a:hover{background:#3d2f50;color:#ffd700}
.container{max-width:960px;margin:0 auto;padding:20px 16px}
.toc{background:#1e1a28;border:1px solid #3a3040;border-radius:12px;padding:24px;margin:24px 0}
.toc h2{color:#c89b3c;font-size:1.3rem;margin-bottom:14px;text-align:center}
.toc table{width:100%;border-collapse:collapse}
.toc td{padding:8px;border-bottom:1px solid #2a2430;color:#d0c8b8}
.toc td a{color:#e8c868;text-decoration:none}
.toc td a:hover{text-decoration:underline}
.toc .lv{font-weight:700;color:#ffd700;width:70px}
.level-tabs{display:flex;gap:8px;margin:28px 0 20px;flex-wrap:wrap;justify-content:center}
.level-tab{padding:12px 24px;border-radius:25px;cursor:pointer;font-weight:700;font-size:1rem;border:2px solid #444;background:#2a2030;color:#b8a88a;transition:all .3s}
.level-tab.active{background:#3d2f50;border-color:#c89b3c;color:#ffd700;box-shadow:0 0 15px rgba(200,155,60,0.2)}
.level-tab:hover{border-color:#c89b3c}
.level-content{display:none}
.level-content.active{display:block}
.lesson-card{background:#1e1a28;border:1px solid #3a3040;border-radius:14px;padding:26px;margin-bottom:26px}
.lesson-header{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.lesson-header h2{color:#c89b3c;font-size:1.5rem;flex:1}
.lesson-badge{background:#c89b3c;color:#14121c;padding:4px 12px;border-radius:20px;font-size:0.8rem;font-weight:700}
.objectives{background:linear-gradient(135deg,#2d3a2d,#1a2a1a);border:1px solid #4a6a3a;border-radius:10px;padding:18px;margin-bottom:18px}
.objectives h3{color:#7cba5a;margin-bottom:10px;font-size:1.05rem}
.objectives li{margin:4px 0 4px 18px;color:#d0c8b8}
.sub-section{margin-bottom:14px}
.sub-section h3{color:#e8c868;font-size:1.1rem;margin-bottom:6px}
.sub-section p{color:#d0c8b8;margin-bottom:8px}
.example-box{background:#2a2438;border-left:4px solid #8a6ad0;border-radius:8px;padding:14px 16px;margin-top:4px}
.example-box strong{color:#b89ae0}
.diagram{background:#1a1625;border:1px solid #3a3040;border-radius:10px;padding:16px;margin:12px 0;text-align:center;overflow-x:auto}
.diagram img{max-width:100%;max-height:280px;border-radius:8px}
.diagram .caption{font-size:0.85rem;color:#887a6a;margin-top:8px}
.quiz-box{background:#201828;border:1px solid #5a3a6a;border-radius:14px;padding:24px;margin-top:20px}
.quiz-box h3{color:#d8a0f0;margin-bottom:16px;font-size:1.2rem}
.quiz-q{margin-bottom:20px}
.quiz-q label{font-weight:600;color:#c8b8a8;display:block;margin-bottom:8px;font-size:1.02rem}
.quiz-opt{display:block;padding:9px 14px;margin:5px 0;border-radius:8px;cursor:pointer;background:#2a2030;border:1px solid #444;color:#b8a88a;transition:all .15s}
.quiz-opt:hover{border-color:#c89b3c;background:#352a40}
.quiz-opt.selected{border-color:#c89b3c;background:#3d2f50;color:#ffd700}
.quiz-opt.correct{border-color:#4a6a3a;background:#2d3a2d;color:#7cba5a}
.quiz-opt.wrong{border-color:#6a3a3a;background:#3a2020;color:#d86060}
.check-btn{margin-top:14px;padding:12px 30px;border:none;border-radius:25px;background:linear-gradient(135deg,#c89b3c,#a07828);color:#14121c;font-weight:700;font-size:1.02rem;cursor:pointer;transition:all .2s}
.check-btn:hover{background:linear-gradient(135deg,#d8ab4c,#b08838);transform:translateY(-1px)}
.explain{margin-top:10px;padding:12px 14px;background:#1a1a2e;border-radius:8px;color:#b8a88a;font-size:0.95rem;display:none;border-left:3px solid #5a3a6a}
.explain.show{display:block}
.score-bar{margin-top:16px;padding:13px 16px;background:#252030;border-radius:10px;color:#c8b8a8;font-weight:600;display:none}
.score-bar.show{display:block}
.back-top{position:fixed;bottom:30px;right:30px;width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#c89b3c,#a07828);color:#14121c;border:none;font-size:1.5rem;cursor:pointer;opacity:0;pointer-events:none;transition:all .3s;z-index:200;box-shadow:0 4px 15px rgba(0,0,0,0.4)}
.back-top.show{opacity:1;pointer-events:auto}
.back-top:hover{transform:translateY(-3px)}
footer{text-align:center;padding:36px 20px;color:#6a5a4a;font-size:0.88rem;border-top:1px solid #2a2430;margin-top:40px}
.drawer{position:fixed;top:0;right:-320px;width:300px;height:100%;background:#1e1a28;z-index:300;transition:right .3s;padding:24px;overflow-y:auto;border-left:1px solid #c89b3c}
.drawer.open{right:0}
.drawer h3{color:#ffd700;margin-bottom:16px}
.drawer a{display:block;color:#d0c8b8;text-decoration:none;padding:8px 0;border-bottom:1px solid #2a2430}
.drawer a:hover{color:#e8c868}
.menu-btn{position:fixed;bottom:30px;left:30px;width:52px;height:52px;border-radius:50%;background:#3d2f50;color:#ffd700;border:1px solid #c89b3c;font-size:1.3rem;cursor:pointer;z-index:200;box-shadow:0 4px 15px rgba(0,0,0,0.4)}
.overlay{position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:250;display:none}
.overlay.show{display:block}
@media(max-width:640px){.hero h1{font-size:2.1rem}.container{padding:14px 10px}}
"""

# Build function for lessons HTML
def render_lesson(lv_idx, lesson, lv_id):
    parts = []
    parts.append(f'<div class="lesson-card" id="{lesson["id"]}">')
    parts.append(f'<div class="lesson-header"><span class="lesson-badge">第{lv_idx*3+1+content["levels"][lv_idx]["lessons"].index(lesson)}課</span><h2>{lesson["title"]}</h2></div>')
    # Objectives
    parts.append('<div class="objectives"><h3>🎯 學習目標</h3><ul>')
    for o in lesson['objectives']:
        parts.append(f'<li>{o}</li>')
    parts.append('</ul></div>')
    # Sections
    qn = 1
    for sec in lesson['sections']:
        parts.append(f'<div class="sub-section"><h3>{qn}. {sec["title"]}</h3><p>{sec["content"]}</p>')
        if 'example' in sec and sec['example']:
            parts.append(f'<div class="example-box"><strong>📌 概念舉例：</strong>{sec["example"]}</div>')
        parts.append('</div>')
        qn += 1
    # Quiz
    ln = lv_idx*3 + 1
    qid = f'quiz{ln}'
    parts.append(f'<div class="quiz-box"><h3>📝 課後練習（{len(quizzes[qid])} 題）</h3><div id="{qid}"></div></div>')
    parts.append('</div>')
    return '\n'.join(parts)

def quiz_json(qid):
    qs = quizzes.get(qid, [])
    arr = []
    for q in qs:
        opts = '","'.join(q['opts'])
        arr.append(f'{{q:"{q["q"]}",opts:["{opts}"],ans:{q["ans"]},explain:"{q["explain"]}"}}')
    return '[' + ',\n'.join(arr) + ']'

# Build TOC
toc_rows = []
for lv_idx, lv in enumerate(content['levels']):
    for lesson in lv['lessons']:
        lnum = lv_idx*3 + lv['lessons'].index(lesson) + 1
        ln = lv_idx*3 + 1
        lkey = f'quiz{ln}'
        qn = len(quizzes.get(lkey, []))
        toc_rows.append(f'<tr><td class="lv">{lv["emoji"]} {lv["name"]}</td><td><a href="#{lesson["id"]}">{lnum}. {lesson["title"]}</a></td><td style="text-align:right;color:#887a6a">{qn} 題</td></tr>')
toc_html = '\n'.join(toc_rows)

# Build level contents
levels_html = []
for lv_idx, lv in enumerate(content['levels']):
    inner = []
    for lesson in lv['lessons']:
        inner.append(render_lesson(lv_idx, lesson, lv['id']))
    body = f'<div id="{lv["id"]}" class="level-content">' + '\n'.join(inner) + '</div>'
    levels_html.append(body)
levels_body = '\n'.join(levels_html)

# Quiz data JS
quiz_js_lines = []
for i in range(1, 10):
    qid = f'quiz{i}'
    quiz_js_lines.append(f'  "{qid}": {quiz_json(qid)},')
quiz_js = '\n'.join(quiz_js_lines)

JS = f"""
// Quiz data
const quizzes = {{
{quiz_js}
}};

// Render quizzes
Object.keys(quizzes).forEach(qid => {{
  const container = document.getElementById(qid);
  if (!container) return;
  const qs = quizzes[qid];
  qs.forEach((q, qi) => {{
    let h = `<div class="quiz-q" data-i="${{qi}}">
      <label>${{qi+1}}. ${{q.q}}</label>`;
    q.opts.forEach((opt, oi) => {{
      h += `<span class="quiz-opt" onclick="selOpt(this,${{qi}},${{oi}},'${{qid}}')">${{String.fromCharCode(65+oi)}}. ${{opt}}</span>`;
    }});
    h += `<div class="explain" id="${{qid}}_e${{qi}}">${{q.explain}}</div></div>`;
    container.innerHTML += h;
  }});
  container.innerHTML += `<button class="check-btn" onclick="chk('${{qid}}')">提交答案</button>
    <div class="score-bar" id="${{qid}}_s"></div>`;
}});

const sel = {{}};
function selOpt(el, qi, oi, qid) {{
  sel[`${{qid}}_${{qi}}`] = oi;
  el.closest('.quiz-q').querySelectorAll('.quiz-opt').forEach(o => o.classList.remove('selected'));
  el.classList.add('selected');
}}
function chk(qid) {{
  const qs = quizzes[qid];
  let c = 0;
  qs.forEach((q, qi) => {{
    const s = sel[`${{qid}}_${{qi}}`];
    document.querySelectorAll(`#${{qid}} .quiz-q[data-i="${{qi}}"] .quiz-opt`).forEach((o, oi) => {{
      o.classList.remove('selected');
      if (oi === q.ans) o.classList.add('correct');
      else if (oi === s) o.classList.add('wrong');
    }});
    if (s === q.ans) c++;
    document.getElementById(`${{qid}}_e${{qi}}`).classList.add('show');
  }});
  const sc = document.getElementById(`${{qid}}_s`);
  const pct = Math.round(c/qs.length*100);
  const msg = pct === 100 ? '🌟 滿分，完美掌握本課！' : pct >= 80 ? '👍 優良成績，再鞏固一下！' : pct >= 60 ? '🙂 合格，請複習重點內容。' : '💪 建議重溫本課再試一次。';
  sc.textContent = `得分：${{c}}/${{qs.length}}（${{pct}}%）— ${{msg}}`;
  sc.classList.add('show');
  sc.scrollIntoView({{behavior:'smooth', block:'nearest'}});
}}
function showLevel(lv, el) {{
  document.querySelectorAll('.level-content').forEach(x => x.classList.remove('active'));
  document.querySelectorAll('.level-tab').forEach(x => x.classList.remove('active'));
  document.getElementById(lv).classList.add('active');
  el.classList.add('active');
}}
window.addEventListener('scroll', () => {{
  document.getElementById('toTop').classList.toggle('show', window.scrollY > 400);
}});
function toTop() {{ window.scrollTo({{top:0,behavior:'smooth'}}); }}
function openMenu() {{ document.getElementById('drawer').classList.add('open'); document.getElementById('ovl').classList.add('show'); }}
function closeMenu() {{ document.getElementById('drawer').classList.remove('open'); document.getElementById('ovl').classList.remove('show'); }}
"""

INDEX_HTML = f"""
<div class="toc" id="index">
<h2>📖 課程索引</h2>
<table>{toc_html}</table>
</div>
"""

# Final HTML
page = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{content['title']} — 教學站</title>
<style>{css}</style>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@700&family=Noto+Sans+TC:wght@400;700&display=swap" rel="stylesheet">
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
{INDEX_HTML}

<div class="level-tabs" id="levels">
<div class="level-tab active" onclick="showLevel('lv1',this)">🌱 初級（第1-3課）</div>
<div class="level-tab" onclick="showLevel('lv2',this)">🔥 中級（第4-6課）</div>
<div class="level-tab" onclick="showLevel('lv3',this)">🧭 高級（第7-9課）</div>
</div>

{levels_body}

<div id="appendix" class="lesson-card">
<div class="lesson-header"><span class="lesson-badge">附錄</span><h2>📄 附錄：全書章節溫習</h2></div>
<div class="sub-section">
<h3>附錄一：重要口訣一覽</h3>
<ul style="margin:8px 0 8px 20px;color:#d0c8b8">
<li><strong>五虎遁年起月</strong>：甲己之年丙作首，乙庚之歲戊為頭，丙辛歲首尋庚起，丁壬壬位順行流，戊癸何方發，甲寅之上好追求。</li>
<li><strong>五鼠遁日起時</strong>：甲己還加甲，乙庚丙子初，丙辛從戊起，丁壬庚子居，戊癸何方發，壬子是真途。</li>
<li><strong>天干五合</strong>：甲己合化土，乙庚合化金，丙辛合化水，丁壬合化木，戊癸合化火。</li>
<li><strong>地支六合</strong>：子丑合土，寅亥合木，卯戌合火，辰酉合金，巳申合水，午未合火土。</li>
<li><strong>地支六沖</strong>：子午沖、丑未沖、寅申沖、卯酉沖、辰戌沖、巳亥沖。</li>
<li><strong>五行相生</strong>：木生火、火生土、土生金、金生水、水生木。</li>
<li><strong>五行相剋</strong>：金剋木、木剋土、土剋水、水剋火、火剋金。</li>
<li><strong>斷事金句</strong>：現象從天干看，實力從地支尋；喜神為輔弼，忌神輾轉攻。</li>
</ul>
</div>
<div class="sub-section">
<h3>附錄二：十天干十二地支五行陰陽速查</h3>
<p>天干：甲乙（木）、丙丁（火）、戊己（土）、庚辛（金）、壬癸（水）。<br>
陽干：甲丙戊庚壬；陰干：乙丁己辛癸。<br>
地支：亥子（水）、寅卯（木）、巳午（火）、申酉（金）、辰戌丑未（土）。<br>
陽支：子寅辰午申戌；陰支：丑卯巳未酉亥。</p>
</div>
<div class="sub-section">
<h3>附錄三：四柱排盤步驟</h3>
<ol style="margin:8px 0 8px 20px;color:#d0c8b8">
<li>查年柱：以立春為界，查萬年曆。</li>
<li>查日柱：查萬年曆得日柱干支。</li>
<li>起月柱：看出生日是否已過節，用五虎遁推天干。</li>
<li>起時柱：將生時化為時辰，用五鼠遁推天干。</li>
<li>排大運：陽男陰女順排，陰男陽女逆排。</li>
<li>配十神：以日干對照各柱干支推十神。</li>
<li>定旺弱：三審（令、地、勢）+ 五原則。</li>
<li>分喜忌：定用神，觀合化，斷吉凶。</li>
</ol>
</div>
<div class="sub-section">
<h3>附錄四：OCR 原文備份</h3>
<p>本站內容皆由全書 128 頁掃描件深度 OCR 提取製作。原文共提取約 51,000 字，點擊下方按鈕可瀏覽附錄頁。</p>
</div>
</div>
</div>

<button class="menu-btn" onclick="openMenu()">☰</button>
<button class="back-top" id="toTop" onclick="toTop()">↑</button>
<div class="overlay" id="ovl" onclick="closeMenu()"></div>
<div class="drawer" id="drawer">
<h3>📖 快速導航</h3>
DRAWER_PLACEHOLDER
</div>

<footer>
<p>本站內容節選自 {content['author']}《{content['title']}》（{content['publisher']}），僅作教育學習參考用途。</p>
<p>深度 OCR 製作 · 教學站 v2 · 2026</p>
</footer>

<script>
{JS}
</script>
</body>
</html>"""

# Fix the drawer template (Python for-loop inside f-string won't work - build separately)
drawer_links = ['<a href="#index" onclick="closeMenu()">課程索引</a>']
for lv in content['levels']:
    drawer_links.append(f'<div style="color:#c89b3c;font-weight:700;margin-top:12px">{lv["emoji"]} {lv["name"]}級</div>')
    for lesson in lv['lessons']:
        drawer_links.append(f'<a href="#{lesson["id"]}" onclick="closeMenu()">{lesson["title"]}</a>')
drawer_links.append('<a href="#appendix" onclick="closeMenu()">📄 附錄</a>')

page = page.replace(f'''<div class="drawer" id="drawer">
<h3>📖 快速導航</h3>
DRAWER_PLACEHOLDER
</div>''', '<div class="drawer" id="drawer">\n<h3>📖 快速導航</h3>\n' + '\n'.join(drawer_links) + '\n</div>')

with open('/tmp/book_ocr/bazi-door-learn-v2/index.html', 'w') as f:
    f.write(page)
print(f"Built: {len(page)} bytes")
