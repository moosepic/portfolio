# Your Photography Site

A Jekyll site for GitHub Pages: blog, about page, and a portfolio split into
individual galleries with a click-to-enlarge lightbox.

## 1. Get it live

1. Create a new repo on GitHub (e.g. `your-username.github.io` for the root
   domain, or any name if you'll use a custom domain later).
2. Push everything in this folder to that repo.
3. In the repo's **Settings → Pages**, set the source to the `main` branch
   (root). GitHub builds Jekyll sites automatically — no build step to
   configure.
4. Your site is live at `https://your-username.github.io/repo-name/` within
   a minute or two.

When you're ready to add your custom domain: put the domain in a file named
`CNAME` (no extension) at the repo root containing just the domain, e.g.
`www.yourdomain.com`, set `url:` in `_config.yml` to that domain, and point
your DNS at GitHub Pages per [GitHub's custom domain docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

## 2. Adding a blog post

Create a file in `_posts/` named `YYYY-MM-DD-short-title.md`:

```markdown
---
title: "My Title"
tags: [travel, notes]
---
Body text in plain Markdown goes here.
```

Commit and push — it appears on `/blog/` automatically, newest first.

## 3. Adding a new gallery

1. Make a folder: `assets/images/galleries/your-gallery-name/`.
2. Process your source photos first (see step 4 below) so what you commit
   is web-sized and watermarked, not your full-resolution originals.
3. Create `_galleries/your-gallery-name.md`:

```yaml
---
title: "Gallery Title"
description: "One line about this set."
order: 3
cover: /assets/images/galleries/your-gallery-name/01.jpg
images:
  - file: /assets/images/galleries/your-gallery-name/01.jpg
    alt: "Short accessible description"
    caption: "Caption shown in the lightbox"
  - file: /assets/images/galleries/your-gallery-name/02.jpg
    alt: "..."
    caption: "..."
---
```

It appears on `/portfolio/` automatically. `order` controls sort position.

## 4. Preparing images (resize + watermark)

```bash
pip install pillow --break-system-packages
python3 scripts/prepare_images.py ~/Photos/my-shoot assets/images/galleries/your-gallery-name --watermark "Your Name"
```

This resizes to a web-appropriate resolution, strips EXIF/GPS metadata, and
tiles a faint visible watermark into the pixels. It renames files `01.jpg`,
`02.jpg`... in the order it finds them — match those names in the gallery's
front matter. Omit `--watermark` if you don't want a visible mark baked in.

## 5. Previewing locally (optional)

```bash
bundle install
bundle exec jekyll serve
```

Then open `http://localhost:4000`. Not required — pushing to GitHub and
checking the live URL works fine too, just slower to iterate.

---

## About the image-protection measures, honestly

This site includes several layers meant to raise the effort required to
copy or scrape your images:

- **Right-click / drag disabled** on images and the lightbox — removes the
  one-click "Save Image As" path for casual visitors.
- **Lightbox renders via `<canvas>`** with a tiled watermark burned into the
  pixels at display time, so a screenshot of the enlarged view carries the
  mark too.
- **`robots.txt`** disallows known AI-training crawlers (GPTBot, CCBot,
  Google-Extended, ClaudeBot, and others) and the page `<meta>` tag adds the
  emerging `noai` / `noimageai` opt-out signal.
- **Only web-sized, pre-watermarked files are ever uploaded** (via the
  `prepare_images.py` script) — your originals never touch the repo.

**None of this is a real barrier against someone determined.** Browser
devtools can find the image URL regardless of right-click blocking; screen
recording captures anything visible on screen; and `robots.txt` /
`noai` are honor-system signals that only compliant crawlers respect —
plenty don't. Treat this setup as reducing casual copying and *signaling*
non-consent (which matters for takedown requests and, increasingly, for
some legal frameworks around AI training), not as a technical guarantee.
The durable protection is the watermark baked into the file itself and
never publishing your full-resolution originals — that's the part that
survives no matter how the image leaves the page.
