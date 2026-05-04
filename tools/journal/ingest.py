#!/usr/bin/env python3
"""
AMRE Journal Ingestion Script
Usage: python3 ingest.py

Prompts for:
  - LinkedIn article URL (or paste raw HTML)
  - Slug, title, tags, lede, excerpt, metaDesc
  - Related article slugs (3)

Then: processes content, builds HTML, pushes to GitHub, updates blog index.

Can also be called non-interactively:
  python3 ingest.py --slug my-slug --html /path/to/article.html --meta metadata.json
"""
import json, re, sys, base64, urllib.request, urllib.error, argparse
from pathlib import Path
from datetime import datetime

# ── Config ───────────────────────────────────────────────────────────
PAT    = "YOUR_GITHUB_PAT_HERE"
REPO   = "Hilex2030/amre-assets"
BRANCH = "main"
API    = f"https://api.github.com/repos/{REPO}"
WEB_BASE = "/amre-assets/website"
ARTS_JSON = Path('/home/claude/blog/articles.json')  # local cache; update after each ingest

# ── GitHub ────────────────────────────────────────────────────────────
def gh(method, path, body=None):
    url = API + path
    headers = {"Authorization": f"Bearer {PAT}", "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"GH ERROR {e.code}: {e.read().decode()[:400]}")
        raise

def gh_get(path):
    d = gh("GET", f"/contents/{path}?ref={BRANCH}")
    return base64.b64decode(d['content']).decode('utf-8'), d['sha']

# ── HTML Cleaning ─────────────────────────────────────────────────────
def clean_linkedin_html(raw_html):
    """Strip LinkedIn wrapper, series logos, outro sections, external links."""
    # Extract body content
    body_match = re.search(r'<p class="published">[^<]*</p>\s*(<div>.*</div>)\s*</body>', raw_html, re.DOTALL)
    if not body_match:
        body_match = re.search(r'<body>.*?(<div>.*</div>)\s*</body>', raw_html, re.DOTALL)
    if not body_match:
        # Assume user passed body content directly
        body = raw_html.strip()
    else:
        body = body_match.group(1)

    # Strip outro patterns
    body = re.sub(r'<hr>\s*<h3>Let[^<]*Chat[^<]*</h3>.*?</div>\s*$', '</div>', body, flags=re.DOTALL|re.IGNORECASE)
    body = re.sub(r'<h3>Let[^<]*Chat[^<]*</h3>.*?</div>\s*$', '</div>', body, flags=re.DOTALL|re.IGNORECASE)
    body = re.sub(r'<p>Follow us on[^<]*<a[^>]*>[^<]*</a>[^<]*</p>', '', body, flags=re.DOTALL|re.IGNORECASE)
    body = re.sub(r'<p>Feel free to reach out[^<]*</p>', '', body, flags=re.DOTALL|re.IGNORECASE)
    body = re.sub(r'<p>#[^<]*</p>', '', body)

    # Strip external links
    body = re.sub(r'<a[^>]*href="[^"]*linkedin[^"]*"[^>]*>(.*?)</a>', r'\1', body, flags=re.IGNORECASE|re.DOTALL)
    body = re.sub(r'<a[^>]*href="[^"]*compass\.com/agents[^"]*"[^>]*>(.*?)</a>', r'\1', body, flags=re.IGNORECASE|re.DOTALL)
    body = re.sub(r'<a[^>]*target="_blank"[^>]*>(.*?)</a>', r'\1', body, flags=re.DOTALL)
    body = re.sub(r'<a[^>]*href="mailto:[^"]*"[^>]*>(.*?)</a>', r'\1', body, flags=re.DOTALL)

    # Strip linkedin images
    body = re.sub(r'<figure>\s*<img[^>]*licdn[^>]*>.*?</figure>', '', body, flags=re.DOTALL)
    body = re.sub(r'<img[^>]*licdn[^>]*/?>', '', body)

    # Clean empty paragraphs
    body = re.sub(r'<p>\s*</p>', '', body)
    body = re.sub(r'<p>&nbsp;</p>', '', body)
    body = re.sub(r'<hr>\s*</div>\s*$', '</div>', body)
    body = re.sub(r'\s+', ' ', body)
    body = re.sub(r'>\s*<', '><', body)

    # Strip outer div wrapper
    inner = re.match(r'^<div>(.*)</div>$', body, re.DOTALL)
    if inner:
        body = inner.group(1).strip()

    return body.strip()

# ── Article Page Builder ──────────────────────────────────────────────
def calc_read_time(body_text):
    words = len(re.sub(r'<[^>]+>', ' ', body_text).split())
    return f'{max(2, round(words / 230))} min'

def build_article_html(art, body_html, og_url=None):
    """Generate complete article page HTML from metadata + body."""
    import html as html_lib

    if og_url is None:
        og_url = 'https://res.cloudinary.com/luxuryp/videos/f_auto,q_auto/so_0,eo_0/woxa6oigeefrvm3lrso0/11023-fruitland-dr-branded-3.jpg'

    slug      = art['slug']
    title     = art['title']
    canonical = f'https://amre.group/blog/{slug}/'
    read_time = calc_read_time(body_html)

    tags_html = ''.join(
        f'<a href="{WEB_BASE}/blog/?tag={html_lib.escape(t)}" class="article-hero-tag">{html_lib.escape(t)}</a>'
        for t in art['tags']
    )

    # Related cards (3)
    all_arts = {a['slug']: a for a in ARTS}
    related_html = ''
    for r_slug in art.get('related', [])[:3]:
        r = all_arts.get(r_slug)
        if r:
            rtags = ''.join(
                f'<span class="card-tag-pill {"primary" if i==0 else "secondary"}">{html_lib.escape(t)}</span>'
                for i, t in enumerate(r['tags'])
            )
            related_html += f'''<a href="{WEB_BASE}/blog/{r['slug']}/" class="journal-card">
  <div class="journal-card-tags">{rtags}</div>
  <div class="journal-card-body">
    <h2>{html_lib.escape(r['title'])}</h2>
    <p>{html_lib.escape(r['excerpt'])}</p>
    <div class="journal-card-meta"><span>Read article</span><span class="journal-card-arrow">›</span></div>
  </div>
</a>
'''

    # Load template from build.py output of an existing article and swap content
    # Instead of re-importing the full build.py, we read an existing article and do targeted replacements.
    # This is more reliable than re-running the full builder.

    # We fetch a known-good article as template and do surgical replacements
    template_slug = 'power-duplex-ownership-los-angeles'
    template_html, _ = gh_get(f'website/blog/{template_slug}/index.html')

    # Replace canonical
    new_html = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{canonical}">', template_html)
    # Replace OG image
    new_html = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{og_url}">', new_html)
    # Replace og:url
    new_html = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{canonical}">', new_html)
    # Replace titles
    new_html = re.sub(r'<title>[^<]*</title>', f'<title>{html_lib.escape(title + " | The AMRE Journal")}</title>', new_html)
    new_html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html_lib.escape(art["metaDesc"])}">', new_html)
    new_html = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{html_lib.escape(title)}">', new_html)
    new_html = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{html_lib.escape(art["metaDesc"])}">', new_html)
    new_html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html_lib.escape(title)}">', new_html)
    new_html = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html_lib.escape(art["metaDesc"])}">', new_html)

    # Article hero tags
    new_html = re.sub(r'<div class="article-hero-tags">.*?</div>', f'<div class="article-hero-tags">{tags_html}</div>', new_html, flags=re.DOTALL)
    # H1
    new_html = re.sub(r'<h1 itemprop="headline">.*?</h1>', f'<h1 itemprop="headline">{html_lib.escape(title)}</h1>', new_html, flags=re.DOTALL)
    # Lede
    new_html = re.sub(r'<p class="article-lede" itemprop="description">.*?</p>', f'<p class="article-lede" itemprop="description">{html_lib.escape(art["lede"])}</p>', new_html, flags=re.DOTALL)
    # Read time
    new_html = re.sub(r'(<div class="article-byline-time-val">)[^<]*(</div>)', f'\\g<1>{read_time}\\g<2>', new_html)
    # Breadcrumb title
    new_html = re.sub(r'(<span class="current">)[^<]*(</span>)', f'\\g<1>{html_lib.escape(title)}\\g<2>', new_html)
    # Article body
    new_html = re.sub(r'(<div class="article-body" itemprop="articleBody">).*?(</div>\s*</section>)', 
                      f'\\g<1>\n{body_html}\n  \\g<2>', new_html, flags=re.DOTALL, count=1)
    # Related section
    new_html = re.sub(r'<div class="article-related-grid">.*?</div>\s*</section>', 
                      f'<div class="article-related-grid">\n{related_html}\n    </div>\n  </section>', new_html, flags=re.DOTALL)

    return new_html

# ── Blog Index Rebuilder ──────────────────────────────────────────────
def update_blog_index(all_arts):
    """Add the new article to the blog index card grid."""
    # Fetch current index
    index_html, _ = gh_get('website/blog/index.html')

    # Find the journal-grid div and inject the new card at the top
    import html as html_lib

    # Rebuild from scratch would require full build.py; instead insert into existing grid
    # Find the first card in the grid and insert before it
    first_card_match = re.search(r'(<div class="journal-card-wrap")', index_html)
    if not first_card_match:
        print("  ✗ Could not find card grid in index")
        return index_html

    # Build new card for latest article (first in list)
    art = all_arts[0]
    tags_attr = ' '.join(art['tags'])
    tags_html = ''.join(
        f'<span class="card-tag-pill {"primary" if i==0 else "secondary"}">{html_lib.escape(t)}</span>'
        for i, t in enumerate(art['tags'])
    )
    card = f'''<div class="journal-card-wrap" data-tags="{html_lib.escape(tags_attr)}">
<a href="{WEB_BASE}/blog/{art['slug']}/" class="journal-card">
  <div class="journal-card-tags">{tags_html}</div>
  <div class="journal-card-body">
    <h2>{html_lib.escape(art['title'])}</h2>
    <p>{html_lib.escape(art['excerpt'])}</p>
    <div class="journal-card-meta"><span>Read article</span><span class="journal-card-arrow">›</span></div>
  </div>
</a>
</div>
'''
    new_index = index_html[:first_card_match.start()] + card + index_html[first_card_match.start():]

    # Update count
    n = len(all_arts)
    new_index = re.sub(r'\d+ articles in the journal', f'{n} articles in the journal', new_index)
    new_index = re.sub(r"'Browse all \d+ articles", f"'Browse all {n} articles", new_index)
    new_index = re.sub(r'"Browse all \d+ articles', f'"Browse all {n} articles', new_index)

    return new_index

# ── Main Ingest Flow ──────────────────────────────────────────────────
def ingest(art_meta, raw_html):
    """Full ingest: clean HTML, build page, push to GitHub."""
    print(f"\n→ Ingesting: {art_meta['slug']}")

    # Clean HTML
    body_html = clean_linkedin_html(raw_html)
    print(f"  Body: {len(body_html)} chars")

    # Build article HTML
    article_html = build_article_html(art_meta, body_html)
    print(f"  Article page: {len(article_html)} chars")

    # Load and update articles.json
    if ARTS_JSON.exists():
        all_data = json.loads(ARTS_JSON.read_text())
        # Prepend new article (newest first)
        all_data['articles'] = [art_meta] + [a for a in all_data['articles'] if a['slug'] != art_meta['slug']]
        ARTS_JSON.write_text(json.dumps(all_data, indent=2))
        all_arts = all_data['articles']
    else:
        all_arts = [art_meta]

    # Update blog index
    new_index_html = update_blog_index(all_arts)

    # Atomic commit
    ref = gh("GET", f"/git/ref/heads/{BRANCH}")
    parent_sha = ref["object"]["sha"]
    parent_commit = gh("GET", f"/git/commits/{parent_sha}")
    base_tree_sha = parent_commit["tree"]["sha"]

    slug = art_meta['slug']
    blobs = [
        (f"website/blog/{slug}/index.html", article_html, "utf-8"),
        ("website/blog/index.html", new_index_html, "utf-8"),
    ]

    tree_entries = []
    for path, content, enc in blobs:
        blob = gh("POST", "/git/blobs", {"content": content, "encoding": enc})
        tree_entries.append({"path": path, "mode": "100644", "type": "blob", "sha": blob["sha"]})
        print(f"  blob {path}")

    new_tree = gh("POST", "/git/trees", {"base_tree": base_tree_sha, "tree": tree_entries})
    new_commit = gh("POST", "/git/commits", {
        "message": f"Add journal article: {art_meta['title'][:60]}",
        "tree": new_tree["sha"],
        "parents": [parent_sha]
    })
    gh("PATCH", f"/git/refs/heads/{BRANCH}", {"sha": new_commit["sha"], "force": False})

    live_url = f"https://hilex2030.github.io/amre-assets/website/blog/{slug}/"
    print(f"\n✓ Published: {live_url}")
    print(f"  Commit: https://github.com/{REPO}/commit/{new_commit['sha']}")
    return live_url

# ── CLI ───────────────────────────────────────────────────────────────
ARTS = json.loads(ARTS_JSON.read_text())['articles'] if ARTS_JSON.exists() else []

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest a new journal article')
    parser.add_argument('--html',  help='Path to raw LinkedIn-exported HTML file')
    parser.add_argument('--meta',  help='Path to JSON file with article metadata')
    parser.add_argument('--slug',  help='Article slug (overrides meta file)')
    args = parser.parse_args()

    if args.meta:
        art_meta = json.loads(Path(args.meta).read_text())
    else:
        # Interactive mode
        print("\n─── AMRE Journal Ingest ───────────────────────────────")
        art_meta = {
            'slug':     input("Slug (e.g. my-new-article): ").strip(),
            'title':    input("Title: ").strip(),
            'tags':     [t.strip() for t in input("Tags (comma-sep, e.g. Investing, LA Market): ").split(',')],
            'lede':     input("Lede (1-2 sentences, italic opener): ").strip(),
            'excerpt':  input("Excerpt (card preview, 1 sentence): ").strip(),
            'metaDesc': input("Meta description (SEO, ~150 chars): ").strip(),
            'related':  [s.strip() for s in input("3 related slugs (comma-sep): ").split(',')],
        }

    if args.slug:
        art_meta['slug'] = args.slug

    if args.html:
        raw_html = Path(args.html).read_text(encoding='utf-8', errors='replace')
    else:
        print("\nPaste the raw article HTML below, then press Ctrl+D (Unix) or Ctrl+Z+Enter (Windows):")
        raw_html = sys.stdin.read()

    ingest(art_meta, raw_html)
