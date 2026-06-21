#!/usr/bin/env python3
"""
応用情報技術者試験 過去問 静的サイトジェネレーター
Usage: python build.py
Output: docs/ ディレクトリ (GitHub Pages 用)

依存パッケージ:
    pip install markdown
"""

import os
import re
import shutil
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Error: 'markdown' パッケージが見つかりません。")
    print("以下を実行してください: pip install markdown")
    exit(1)

EXAM_DIR = Path("exam")
DOCS_DIR = Path("docs")

MD_EXTENSIONS = ["tables", "fenced_code", "nl2br"]


# ── パーサー ──────────────────────────────────────────────

def parse_frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip() for v in val[1:-1].split(",")]
        meta[key] = val
    return meta, text[match.end():]


def split_sections(content):
    sections = {}
    current = None
    buf = []
    for line in content.splitlines():
        m = re.match(r"^## (.+)", line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = m.group(1)
            buf = []
        else:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def md_to_html(text):
    return markdown.markdown(text, extensions=MD_EXTENSIONS)


# ── CSS / JS (共通) ──────────────────────────────────────

COMMON_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Hiragino Sans",
               "Noto Sans JP", sans-serif;
  background: #f5f5f5;
  color: #222;
  line-height: 1.7;
}

a { color: #0066cc; text-decoration: none; }
a:hover { text-decoration: underline; }

header {
  background: #1a3a5c;
  color: #fff;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
header h1 { font-size: 1rem; font-weight: 700; flex: 1; }
header a { color: #aed6f1; font-size: 0.85rem; }

.container { max-width: 860px; margin: 0 auto; padding: 16px; }

.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,.1);
  padding: 20px 24px;
  margin-bottom: 16px;
}

/* 問題メタ情報 */
.meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 14px;
  font-size: 0.82rem;
}
.tag {
  background: #e8f0fe;
  color: #1a3a5c;
  border-radius: 4px;
  padding: 2px 8px;
}
.tag.cat { background: #fdebd0; color: #7d4e00; }

h2.section-title {
  font-size: 1rem;
  color: #1a3a5c;
  border-left: 4px solid #1a3a5c;
  padding-left: 8px;
  margin-bottom: 12px;
}

/* Markdown 内コンテンツ */
.md-content p { margin-bottom: 0.8em; }
.md-content ul, .md-content ol { padding-left: 1.4em; margin-bottom: 0.8em; }
.md-content li { margin-bottom: 0.3em; }

.md-content table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  margin-bottom: 1em;
  overflow-x: auto;
  display: block;
}
.md-content th, .md-content td {
  border: 1px solid #ccc;
  padding: 6px 10px;
  text-align: left;
}
.md-content th { background: #f0f4f8; }
.md-content code {
  background: #f0f0f0;
  padding: 1px 5px;
  border-radius: 3px;
  font-size: 0.9em;
}
.md-content pre {
  background: #f6f8fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 12px;
  overflow-x: auto;
  margin-bottom: 1em;
}
.md-content img { max-width: 100%; height: auto; border-radius: 4px; }

/* 解答セクション */
.answer-section { display: none; }
.answer-section.visible { display: block; }

/* ボタン */
.btn {
  display: inline-block;
  padding: 10px 24px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: background .15s;
}
.btn-reveal {
  background: #1a3a5c;
  color: #fff;
  width: 100%;
  margin: 8px 0;
}
.btn-reveal:hover { background: #254d7a; }
.btn-hide {
  background: #e0e0e0;
  color: #555;
  width: 100%;
  margin: 8px 0;
}
.btn-hide:hover { background: #d0d0d0; }

/* ナビゲーション */
.nav-bar {
  display: flex;
  gap: 8px;
  margin-top: 8px;
  flex-wrap: wrap;
}
.nav-btn {
  flex: 1;
  min-width: 120px;
  text-align: center;
  padding: 10px;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #1a3a5c;
}
.nav-btn:hover { background: #e8f0fe; text-decoration: none; }
.nav-btn.disabled { color: #aaa; border-color: #e0e0e0; pointer-events: none; }

/* 一覧ページ */
.exam-group { margin-bottom: 24px; }
.exam-group h2 {
  font-size: 1.1rem;
  padding: 8px 12px;
  background: #1a3a5c;
  color: #fff;
  border-radius: 6px 6px 0 0;
  margin-bottom: 0;
}
.question-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1px;
  background: #ccc;
  border: 1px solid #ccc;
  border-top: none;
  border-radius: 0 0 6px 6px;
  overflow: hidden;
}
.question-item {
  background: #fff;
  padding: 10px 12px;
  font-size: 0.88rem;
  transition: background .1s;
}
.question-item:hover { background: #e8f0fe; }
.question-item a { display: block; color: #222; }
.question-item .q-no { font-weight: 700; color: #1a3a5c; }
.question-item .q-sub { color: #666; font-size: 0.8rem; margin-top: 2px; }

@media (max-width: 600px) {
  .card { padding: 14px 16px; }
  .question-grid { grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); }
}
"""

REVEAL_JS = """
function toggleAnswer(show) {
  document.querySelectorAll('.answer-section').forEach(el => {
    el.classList.toggle('visible', show);
  });
  document.getElementById('btn-reveal').style.display = show ? 'none' : '';
  document.getElementById('btn-hide').style.display  = show ? '' : 'none';
}
"""


# ── 問題ページ生成 ────────────────────────────────────────

def render_question_html(meta, sections, prev_url, next_url):
    q_no = meta.get("question_no", "?")
    season_label = f"{meta.get('year', '')}年{meta.get('season', '')}期"
    category = meta.get("category", "")
    subcategory = meta.get("subcategory", "")
    tags = meta.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]

    mondai_html = md_to_html(sections.get("問題文", "（問題文なし）"))
    image_md = sections.get("参照画像", "")
    image_html = md_to_html(image_md) if image_md and "なし" not in image_md else ""
    seikai_html = md_to_html(sections.get("正解", ""))
    hokan_html = md_to_html(sections.get("選択肢補足", ""))
    tokikata_html = md_to_html(sections.get("解き方", ""))

    tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)

    nav_prev = (f'<a href="{prev_url}" class="nav-btn">← 前の問題</a>'
                if prev_url else '<span class="nav-btn disabled">← 前の問題</span>')
    nav_next = (f'<a href="{next_url}" class="nav-btn">次の問題 →</a>'
                if next_url else '<span class="nav-btn disabled">次の問題 →</span>')

    image_block = f'<div class="card"><h2 class="section-title">参照画像</h2><div class="md-content">{image_html}</div></div>' if image_html else ""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>問{q_no} - {season_label} 応用情報技術者試験</title>
<style>{COMMON_CSS}</style>
</head>
<body>
<header>
  <h1>応用情報技術者試験 {season_label} 問{q_no}</h1>
  <a href="../../index.html">← 一覧に戻る</a>
</header>
<div class="container">

  <div class="card">
    <div class="meta-row">
      <span class="tag cat">{category}</span>
      <span class="tag">{subcategory}</span>
      {tags_html}
    </div>
    <h2 class="section-title">問題文</h2>
    <div class="md-content">{mondai_html}</div>
  </div>

  {image_block}

  <div class="card">
    <button class="btn btn-reveal" id="btn-reveal" onclick="toggleAnswer(true)">答えを見る</button>
    <button class="btn btn-hide"   id="btn-hide"   onclick="toggleAnswer(false)" style="display:none">答えを隠す</button>

    <div class="answer-section">
      <h2 class="section-title" style="margin-top:16px">正解</h2>
      <div class="md-content">{seikai_html}</div>
    </div>

    <div class="answer-section">
      <h2 class="section-title" style="margin-top:16px">選択肢補足</h2>
      <div class="md-content">{hokan_html}</div>
    </div>

    <div class="answer-section">
      <h2 class="section-title" style="margin-top:16px">解き方</h2>
      <div class="md-content">{tokikata_html}</div>
    </div>
  </div>

  <div class="card">
    <div class="nav-bar">
      {nav_prev}
      <a href="../../index.html" class="nav-btn" style="flex:0.5">一覧</a>
      {nav_next}
    </div>
  </div>

</div>
<script>{REVEAL_JS}</script>
</body>
</html>
"""


# ── インデックスページ生成 ────────────────────────────────

EXAM_LABELS = {
    "2025_autumn_am": "2025年秋期 午前",
    "2025_spring_am": "2025年春期 午前",
    "2024_autumn_am": "2024年秋期 午前",
    "2024_spring_am": "2024年春期 午前",
}

def render_index_html(exam_groups):
    groups_html = ""
    for exam_dir, questions in sorted(exam_groups.items(), reverse=True):
        label = EXAM_LABELS.get(exam_dir, exam_dir)
        items_html = ""
        for q in sorted(questions, key=lambda x: x["no"]):
            items_html += f"""
      <div class="question-item">
        <a href="exam/{exam_dir}/q{q['no']:02d}.html">
          <div class="q-no">問{q['no']}</div>
          <div class="q-sub">{q['subcategory']}</div>
        </a>
      </div>"""
        groups_html += f"""
  <div class="exam-group card" style="padding:0">
    <h2>{label}（{len(questions)}問）</h2>
    <div class="question-grid">{items_html}
    </div>
  </div>"""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>応用情報技術者試験 過去問</title>
<style>{COMMON_CSS}
body {{ padding-bottom: 32px; }}
.hero {{
  background: #1a3a5c;
  color: #fff;
  padding: 24px 16px;
  text-align: center;
}}
.hero h1 {{ font-size: 1.4rem; margin-bottom: 4px; }}
.hero p {{ font-size: 0.9rem; color: #aed6f1; }}
</style>
</head>
<body>
<div class="hero">
  <h1>応用情報技術者試験 過去問</h1>
  <p>問題をクリックすると問題文が表示されます。解答は手動で開示できます。</p>
</div>
<div class="container" style="margin-top:16px">
  {groups_html}
</div>
</body>
</html>
"""


# ── メイン処理 ────────────────────────────────────────────

def build():
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir()

    exam_groups = {}

    for exam_folder in sorted(EXAM_DIR.iterdir()):
        if not exam_folder.is_dir():
            continue
        exam_key = exam_folder.name

        md_files = sorted(exam_folder.glob("*.md"),
                          key=lambda p: int(re.search(r"_q(\d+)", p.stem).group(1))
                          if re.search(r"_q(\d+)", p.stem) else 0)
        if not md_files:
            continue

        out_dir = DOCS_DIR / "exam" / exam_key
        out_dir.mkdir(parents=True)

        # 画像をコピー
        for img in exam_folder.glob("*.png"):
            shutil.copy(img, out_dir / img.name)
        for img in exam_folder.glob("*.jpg"):
            shutil.copy(img, out_dir / img.name)

        parsed = []
        for md_path in md_files:
            text = md_path.read_text(encoding="utf-8")
            meta, content = parse_frontmatter(text)
            sections = split_sections(content)
            q_no_str = meta.get("question_no", "0")
            try:
                q_no = int(q_no_str)
            except ValueError:
                q_no = 0
            parsed.append((q_no, meta, sections, md_path))

        parsed.sort(key=lambda x: x[0])

        exam_groups[exam_key] = []
        for i, (q_no, meta, sections, md_path) in enumerate(parsed):
            prev_url = f"q{parsed[i-1][0]:02d}.html" if i > 0 else None
            next_url = f"q{parsed[i+1][0]:02d}.html" if i < len(parsed) - 1 else None

            html = render_question_html(meta, sections, prev_url, next_url)
            out_path = out_dir / f"q{q_no:02d}.html"
            out_path.write_text(html, encoding="utf-8")

            exam_groups[exam_key].append({
                "no": q_no,
                "subcategory": meta.get("subcategory", ""),
            })

        print(f"  [{exam_key}] {len(parsed)} 問 → {out_dir}")

    index_html = render_index_html(exam_groups)
    (DOCS_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"\n完了: {DOCS_DIR / 'index.html'}")


if __name__ == "__main__":
    build()
