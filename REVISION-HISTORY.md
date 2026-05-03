# AMRE Website — Revision History & Revert Guide

> **Every change to the website is automatically saved as a git commit.**  
> You can view, compare, and restore any previous version at any time.

---

## 🔗 Quick Links

| Resource | URL |
|---|---|
| **Live website** | https://hilex2030.github.io/amre-assets/website/ |
| **GitHub repository** | https://github.com/Hilex2030/amre-assets |
| **Full commit history** | https://github.com/Hilex2030/amre-assets/commits/main |
| **Website folder** | https://github.com/Hilex2030/amre-assets/tree/main/website |

---

## 📋 How to Revert a Single Page (No Coding Required)

### Method 1 — Via GitHub Web (easiest)

1. Go to **https://github.com/Hilex2030/amre-assets/commits/main**
2. Find the commit you want to go back to (use the table below)
3. Click the commit message to open it
4. Find the file you want to restore (e.g. `website/index.html`)
5. Click **"..."** → **"View file at this point"**
6. Click the pencil ✏️ icon to edit
7. Select all, paste the old content, commit with message like `Revert: homepage to [date]`

### Method 2 — Ask Claude

Simply say:  
> *"Revert the homepage to the version from May 2, 2026"*  
> or  
> *"Roll back the contact page to before the nav change"*

Claude will fetch the old version from git history and push it back.

### Method 3 — GitHub CLI (for developers)

```bash
# Clone the repo
git clone https://github.com/Hilex2030/amre-assets.git
cd amre-assets

# See history
git log --oneline

# Restore a specific file to a specific commit
git checkout <commit-sha> -- website/index.html

# Push the revert
git add website/index.html
git commit -m "Revert: homepage to <commit-sha>"
git push
```

---

## 📁 Website File Structure

```
amre-assets/
├── website/
│   ├── index.html              ← Homepage
│   ├── sellers/index.html      ← Sellers page
│   ├── buyers/index.html       ← Buyers page
│   ├── team/index.html         ← Team page
│   ├── contact/index.html      ← Contact page
│   ├── properties/
│   │   ├── index.html          ← Properties listing page
│   │   └── fruitland-401/
│   │       └── index.html      ← 11023 Fruitland Dr feature page
├── assets/
│   ├── logos/
│   │   ├── amre-white.svg      ← AMRE logo (white)
│   │   ├── amre-black.svg      ← AMRE logo (dark)
│   │   ├── compass-white.png   ← Compass logo (white)
│   │   └── compass-black.png   ← Compass logo (dark)
│   └── photos/
│       ├── amre-michael-stairs-suit.jpg
│       ├── amre-michael-kitchen.jpg
│       ├── amre-michael-sofa-casual.jpg
│       ├── amre-ania-stairs-dress.jpg
│       ├── amre-ania-kitchen.jpg
│       ├── amre-ania-sofa-green.jpg
│       ├── amre-group-sofa-formal.jpg
│       ├── amre-group-stairs-formal.jpg
│       ├── amre-group-exterior-formal.jpg
│       └── amre-group-sofa-conversation.jpg
└── artifacts/
    ├── tracker-4248-lasalle/   ← Active deal tracker
    └── opportunity-11155-tremaine/  ← Seller opportunity dashboard
```

---

## 🕐 Recent Commit History

| Commit | Date | Description | Link |
|---|---|---|---|
| `e21273b4` | 2026-05-03 | Update dashboard — La Salle post-inspection sweep May 2 | [View](https://github.com/Hilex2030/amre-assets/commit/e21273b4d39bcb2446c8166a32844667e6b62d17) |
| `402fda9a` | 2026-05-03 | Update: consistent nav/footer, stats, social links, dark text — website/ | [View](https://github.com/Hilex2030/amre-assets/commit/402fda9a98304597eff145aa714000d02aabe4ab) |
| `12647703` | 2026-05-03 | Update: consistent nav/footer, stats, social links, dark text — contact | [View](https://github.com/Hilex2030/amre-assets/commit/126477038cd97eda9530a8b270b76b2c41f34203) |
| `7cc0ee28` | 2026-05-03 | Update: consistent nav/footer, stats, social links, dark text — team | [View](https://github.com/Hilex2030/amre-assets/commit/7cc0ee28033ee6ff0f19f16bea6252dde46e9bd2) |
| `f1a0d02b` | 2026-05-03 | Update: consistent nav/footer, stats, social links, dark text — buyers | [View](https://github.com/Hilex2030/amre-assets/commit/f1a0d02b88a74848e14ead5e15d10598ac8830bc) |
| `32533138` | 2026-05-03 | Update: consistent nav/footer, stats, social links, dark text — sellers | [View](https://github.com/Hilex2030/amre-assets/commit/32533138565362a0b53e257029326b4b7a620fc0) |
| `41f658d6` | 2026-05-03 | Rebuild homepage: stacked team, real photos, updated stats, featured pro | [View](https://github.com/Hilex2030/amre-assets/commit/41f658d619c818a290f19d13665e5c65f4527373) |
| `6ac91f59` | 2026-05-03 | Add Fruitland property page — 11023 Fruitland Dr Unit 401 | [View](https://github.com/Hilex2030/amre-assets/commit/6ac91f59e6b1c5c15767edf9024a69be6d892396) |
| `d02298d1` | 2026-05-03 | Rebuild homepage: stacked team, real photos, updated stats, featured pro | [View](https://github.com/Hilex2030/amre-assets/commit/d02298d10e11e1b62c65b8a6c4a7d7e7ca6612b5) |
| `51603ea8` | 2026-05-03 | Rebuild homepage: stacked team, real photos, updated stats, featured pro | [View](https://github.com/Hilex2030/amre-assets/commit/51603ea86a4394b2cacfaab25d3da39bfb82f289) |
| `0461420d` | 2026-05-03 | Fix: comprehensive mobile layout — properties | [View](https://github.com/Hilex2030/amre-assets/commit/0461420ddff9db86a835ee9e119f431665b24b5e) |
| `dcee6e49` | 2026-05-03 | Fix: comprehensive mobile layout — contact | [View](https://github.com/Hilex2030/amre-assets/commit/dcee6e49b8c4f36b9d47d4238a786af0387ce0af) |
| `986f6132` | 2026-05-03 | Fix: comprehensive mobile layout — team | [View](https://github.com/Hilex2030/amre-assets/commit/986f613279e0c201c2f67224587fbe70ca6f2c9f) |
| `46a7ba7c` | 2026-05-03 | Fix: comprehensive mobile layout — buyers | [View](https://github.com/Hilex2030/amre-assets/commit/46a7ba7ce1249fd6d9ce15084f772f93c4631dbc) |
| `56294e76` | 2026-05-03 | Fix: comprehensive mobile layout — sellers | [View](https://github.com/Hilex2030/amre-assets/commit/56294e7615c5130fbe6093844c0adc9494b4c3dd) |
| `75bab4a2` | 2026-05-03 | Fix: comprehensive mobile layout — website | [View](https://github.com/Hilex2030/amre-assets/commit/75bab4a29942c3d92760d295795a640f8ea27373) |
| `bc9d76d8` | 2026-05-03 | Fix: contact page — agents above form, working intent chips, mobile stac | [View](https://github.com/Hilex2030/amre-assets/commit/bc9d76d830ad00366a80d6eb264e8882a9ce66d3) |
| `51fba272` | 2026-05-03 | Fix: Playfair as primary header font — properties | [View](https://github.com/Hilex2030/amre-assets/commit/51fba272a39ee11982a0bc799b98cafd6c58e09c) |
| `c0d253d6` | 2026-05-03 | Fix: Playfair as primary header font — contact | [View](https://github.com/Hilex2030/amre-assets/commit/c0d253d683dddde05840f14604055f75d6bb9f6a) |
| `798da7ea` | 2026-05-03 | Fix: Playfair as primary header font — team | [View](https://github.com/Hilex2030/amre-assets/commit/798da7ea1ecac9e85cc27a5c8cda318651c88ffa) |
| `653ead45` | 2026-05-03 | Fix: Playfair as primary header font — buyers | [View](https://github.com/Hilex2030/amre-assets/commit/653ead45f0576af6d4f1758338a1ff5dcf08b173) |
| `25112f4a` | 2026-05-03 | Fix: Playfair as primary header font — sellers | [View](https://github.com/Hilex2030/amre-assets/commit/25112f4accb0207faae5f0791042562fd71b66dd) |
| `196d7358` | 2026-05-03 | Fix: Playfair as primary header font — website | [View](https://github.com/Hilex2030/amre-assets/commit/196d73587f5bfd74b264ddc7d464283f43bb7dca) |
| `49849376` | 2026-05-02 | Buyers: high-specificity overrides for sans-serif headlines | [View](https://github.com/Hilex2030/amre-assets/commit/49849376d11058fd307b5bc7999492a48832fbc2) |
| `e6fcc0e7` | 2026-05-02 | <!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta nam | [View](https://github.com/Hilex2030/amre-assets/commit/e6fcc0e7755c0eed40f244a0bf7ad5b0f9310403) |
| `3604821d` | 2026-05-02 | Contact: drop amre.group/contact-us canonical and og:url | [View](https://github.com/Hilex2030/amre-assets/commit/3604821d25e96772d5e7eb6b12bd1eeb0094999e) |
| `c4c0efe0` | 2026-05-02 | Properties: drop all amre.group property links, fix canonical/og:url | [View](https://github.com/Hilex2030/amre-assets/commit/c4c0efe02a3495278bb9e4fc7308e50a1b75ed2b) |
| `df88500e` | 2026-05-02 | Team: actually swap agent-photo-col bg images to Q1 2026 photoshoot phot | [View](https://github.com/Hilex2030/amre-assets/commit/df88500ef41f1c4444c757b4c91788519ce34786) |
| `aeb7cb73` | 2026-05-02 | Contact: sans headlines, larger paragraph type, lighter footer, unify na | [View](https://github.com/Hilex2030/amre-assets/commit/aeb7cb737a256b5280bfce199060e3f9d83d509d) |
| `238a76b0` | 2026-05-02 | Team: swap to Q1 2026 photoshoot photos, sans headlines, larger paragrap | [View](https://github.com/Hilex2030/amre-assets/commit/238a76b0151c3a6276a4f74c56bfd9fb325956b1) |


---

## 🎨 Brand Reference

| Token | Value | Use |
|---|---|---|
| `--forest` | `#1c3d31` | Hunter green — primary dark sections |
| `--navy` | `#070B33` | Deep navy — nav, footer |
| `--brass` | `#ffc13c` | Gold — accents, CTAs, eyebrows |
| `--blue` | `#0064e5` | Compass blue — links, badges |
| `--offwhite` | `#f7edf0` | Light background sections |
| Serif | Playfair Display | All headlines (h1–h4) |
| Sans | Montserrat | Body, nav, labels, buttons |

---

## 📞 Support

**To request changes**, start a new Claude conversation in the AMRE project and describe:
- Which page
- What section
- What to change (screenshot preferred)

**Tally form ID:** `aQZxXX`  
**GitHub PAT expires:** ~July 2026

---

*Last updated: May 2, 2026 · Maintained by AMRE Real Estate Group*
