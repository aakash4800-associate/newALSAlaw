# ALSA Law — Astro Landing Page

A navy-and-gold legal-firm landing page built with **Astro 5**, **Tailwind 4**, and **Markdown content collections**, ready to deploy on **Netlify** via **GitHub**.

---

## What's in the project

```
Web1/
├─ astro.config.mjs        # Astro + Tailwind + sitemap config
├─ netlify.toml            # Netlify build settings + security headers
├─ package.json            # Dependencies & scripts
├─ public/                 # Static assets (favicon, robots.txt)
├─ src/
│  ├─ components/          # Hero, PracticeAreas, About, Attorneys, Testimonials, Contact, Nav, Footer
│  ├─ content/             # ← All editable copy lives here as .md files
│  │  ├─ practice-areas/   # 4 markdown files, one per practice
│  │  ├─ attorneys/        # 4 attorney bios
│  │  └─ testimonials/     # 3 client quotes
│  ├─ layouts/Layout.astro
│  ├─ pages/index.astro    # The landing page itself
│  └─ styles/global.css    # Tailwind theme (navy & gold tokens)
└─ tsconfig.json
```

To edit any practice area, attorney bio, or testimonial, **just edit the matching `.md` file** — Astro rebuilds the page automatically.

---

## Step-by-step: get this on a live URL

### 1. Run it locally first (5 minutes)

Open a terminal in this folder and run:

```bash
npm install
npm run dev
```

Open <http://localhost:4321>. The page should look exactly like the production build.

> Need Node.js? Install **Node 20 or newer** from <https://nodejs.org>.

To produce the production build: `npm run build` (output goes to `dist/`).

### 2. Push to GitHub (10 minutes)

1. Go to <https://github.com/new> and create a new **private** (or public) repo named e.g. `alsa-law-site`. **Do not** initialize it with a README, license, or .gitignore — this folder already has them.
2. In the terminal, from inside this folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: ALSA Law landing page"
   git branch -M main
   git remote add origin https://github.com/<your-username>/alsa-law-site.git
   git push -u origin main
   ```
3. Refresh your repo page on GitHub — every file should now be there.

### 3. Deploy on Netlify (5 minutes)

1. Sign in at <https://app.netlify.com>.
2. Click **Add new site → Import an existing project → GitHub**.
3. Authorize Netlify to access your GitHub account if prompted, then pick `alsa-law-site`.
4. Netlify will auto-detect the `netlify.toml` in this repo. The values should already be filled in:
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
   - **Node version:** `20`
5. Click **Deploy site**. The first build takes ~60 seconds. When it's green, click **Open production deploy** to see it live.

You'll get a free `*.netlify.app` URL immediately. To use a custom domain (e.g., `alsa-law.com`):

- Netlify dashboard → **Domain settings → Add a domain you already own** → follow the DNS instructions.
- HTTPS is provisioned automatically by Let's Encrypt.

### 4. Future updates — the workflow

```bash
# edit a markdown file or component
git add .
git commit -m "Update Margaret's bio"
git push
```

Netlify watches the `main` branch and rebuilds + redeploys on every push. Usually live within 90 seconds.

### 5. The contact form just works

The Contact form in `src/components/Contact.astro` uses Netlify Forms — submissions go straight to your Netlify dashboard under **Forms**. No backend or third-party service needed.

To get email notifications: Netlify dashboard → **Forms → Settings → Form notifications → Add notification**.

---

## Editing content

| To change… | Edit this file |
| --- | --- |
| Hero headline / stats | `src/components/Hero.astro` |
| About copy / pull-quote | `src/components/About.astro` |
| A practice area | `src/content/practice-areas/<name>.md` |
| An attorney bio | `src/content/attorneys/<name>.md` |
| A testimonial | `src/content/testimonials/<n>.md` |
| Contact details / address | `src/components/Contact.astro` + `src/components/Footer.astro` |
| Brand colors / fonts | `src/styles/global.css` (the `@theme` block) |
| Site title / SEO meta | `src/layouts/Layout.astro` |

---

## Replacing the placeholder firm

Search-and-replace `ALSA Law` and `alsa-law.example` across the project to drop in your real firm name and domain.
