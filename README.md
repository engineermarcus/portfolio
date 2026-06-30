# Neiman Marcus — Portfolio

A single-page developer portfolio: infrastructure tooling, client work, and learning references pulled from [github.com/engineermarcus](https://github.com/engineermarcus).

## Live site

Enable GitHub Pages on this repo (Settings → Pages → Deploy from `main` / root) to serve it at:

```
https://engineermarcus.github.io/portfolio
```

## Structure

```
portfolio/
└── index.html   # entire site — markup, styles, and content in one file
```

## Stack

Plain HTML/CSS, no build step. Fonts loaded from Google Fonts (Space Grotesk, JetBrains Mono, Inter).

## Sections

- **Infrastructure & Tools** — self-initiated systems: cloud dev environments, automation, networking, AI tooling
- **Client & Product Work** — shipped projects, including a live e-commerce build
- **Learning & Reference** — public curricula and notes

## Updating

Edit `index.html` directly — each project is a `.repo` block with a name, language tag, description, and stack list. Copy an existing block to add a new project.

## License

MIT
