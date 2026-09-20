#!/usr/bin/env python3
"""點入八字門教學站 v3 - 加入圖示動畫+淺白說明"""
import json, html

BASE = '/tmp/book_ocr/bazi-door-learn-v2'

def load(name):
    with open(f'{BASE}/{name}') as f:
        return json.load(f)

content = load('content.json')
quizzes = {}
for i in range(1, 10):
    quizzes[f'quiz{i}'] = load(f'quiz{i}.json')

def svg(name):
    with open(f'{BASE}/assets/{name}.svg') as f:
        return f.read()

SVG_5EL = svg('5elements')
SVG_PILLARS = svg('pillars')
SVG_10GODS = svg('10gods')
SVG_ZODIAC = svg('zodiac')

# ============ CSS ============
css = '''
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Noto Serif TC','Noto Sans TC',serif;background:#14121c;color:#e8e0d0;line-height:1.9;min-height:100vh}
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
.level-content.active{display:block;animation:fadeIn .4s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.lesson-card{background:#1e1a28;border:1px solid #3a3040;border-radius:14px;padding:26px;margin-bottom:26px;scroll-margin-top:70px}
.lesson-header{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.lesson-header h2{color:#c89b3c;font-size:1.5rem;flex:1}
.lesson-badge{background:#c89b3c;color:#14121c;padding:4px 12px;border-radius:20px;font-size:0.8rem;font-weight:700}
.objectives{background:linear-gradient(135deg,#2d3a2d,#1a2a1a);border:1px solid #4a6a3a;border-radius:10px;padding:18px;margin-bottom:22px}
.objectives h3{color:#7cba5a;margin-bottom:10px;font-size:1.05rem}
.objectives li{margin:6px 0 6px 18px;color:#d0c8b8}
.sub-section{background:#221d2e;border-radius:10px;padding:18px 20px;margin-bottom:16px;border-left:3px solid #3a3040}
.sub-section:hover{border-left-color:#c89b3c}
.sub-section h3{color:#e8c868;font-size:1.1rem;margin-bottom:10px}
.sub-section p{color:#d0c8b8;margin-bottom:10px;line-height:2}
.sub-section p:last-child{margin-bottom:0}
.tip{background:#2a2438;border-left:4px solid #8a6ad0;border-radius:8px;padding:14px 18px;margin:14px 0 4px}
.tip strong{color:#b89ae0;display:block;margin-bottom:6px}
.tip p{color:#c8b8d8;margin:0}
.diagram-wrap{background:#1a1625;border:1px solid #3a3040;border-radius:10px;padding:16px;margin:18px 0;text-align:center;overflow-x:auto}
.diagram-wrap svg{max-width:100%;max-height:340px}
.diagram-wrap .caption{font-size:0.85rem;color:#887a6a;margin-top:8px}
.quiz-box{background:#201828;border:1px solid #5a3a6a;border-radius:14px;padding:24px;margin-top:24px}
.quiz-box h3{color:#d8a0f0;margin-bottom:16px;font-size:1.2rem}
.quiz-q{margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid #2a2430}
.quiz-q:last-of-type{border-bottom:none}
.quiz-q label{font-weight:600;color:#c8b8a8;display:block;margin-bottom:8px;font-size:1.02rem}
.quiz-opt{display:block;padding:9px 14px;margin:5px 0;border-radius:8px;cursor:pointer;background:#2a2030;border:1px solid #444;color:#b8a88a;transition:all .15s}
.quiz-opt:hover{border-color:#c89b3c;background:#352a40}
.quiz-opt.selected{border-color:#c89b3c;background:#3d2f50;color:#ffd700}
.quiz-opt.correct{border-color:#4a6a3a;background:#2d3a2d;color:#7cba5a;animation:pulse .4s}
.quiz-opt.wrong{border-color:#6a3a3a;background:#3a2020;color:#d86060}
@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.03)}100%{transform:scale(1)}}
.check-btn{margin-top:14px;padding:12px 30px;border:none;border-radius:25px;background:linear-gradient(135deg,#c89b3c,#a07828);color:#14121c;font-weight:700;font-size:1.02rem;cursor:pointer;transition:all .2s}
.check-btn:hover{background:linear-gradient(135deg,#d8ab4c,#b08838);transform:translateY(-1px)}
.explain{margin-top:10px;padding:12px 14px;background:#1a1a2e;border-radius:8px;color:#b8a88a;font-size:0.95rem;display:none;border-left:3px solid #5a3a6a}
.explain.show{display:block;animation:fadeIn .3s}
.score-bar{margin-top:16px;padding:13px 16px;background:#252030;border-radius:10px;color:#c8b8a8;font-weight:600;display:none}
.score-bar.show{display:block;animation:fadeIn .3s}
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
/* SVG animation: flow arrows for 5elements */
.flow-arrow{animation:flowing 2.5s ease-in-out infinite}
@keyframes flowing{0%,100%{opacity:0.4}50%{opacity:1}}
.svg-pulse{animation:svgPulse 2.2s ease-in-out infinite;transform-origin:center}
@keyframes svgPulse{0%,100%{opacity:1}50%{opacity:0.55}}
@media(max-width:640px){.hero h1{font-size:2.1rem}.container{padding:14px 10px}}
'''
print(f"CSS part 1 done: {len(css)} chars")
