# SentinelX design system

**Owner:** Geng Xin · **Tokens:** `app/globals.css` · **CTAs:** `btn-cta` classes in `globals.css`

## Visual language

SentinelX uses a warm, Handhold-inspired enterprise palette with DM Sans (UI) and Source Serif 4 (display). Light and dark themes share semantic CSS variables so marketing and dashboard surfaces stay consistent.

## Color tokens

| Token | Light | Purpose |
|-------|-------|---------|
| `--sx-bg` | `#faf8f5` | Page background |
| `--sx-fg` | `#1a1614` | Primary text |
| `--sx-muted` | `#6b635c` | Secondary text |
| `--sx-accent` | `#e0634f` | Brand accent, links, highlights |
| `--sx-card-solid` | `#ffffff` | Cards and panels |

Intelligence semantics (Tailwind utility classes):

| Meaning | Usage |
|---------|--------|
| Emerald | Success, live connection, low risk |
| Amber / orange | Warning, polling, medium/high risk |
| Red | Critical alerts and risk |
| Purple / cyan | Executive insight, realtime events (marketing) |

## Typography

| Role | Font | Class pattern |
|------|------|----------------|
| Display headings | Source Serif 4 | `font-display` |
| Body UI | DM Sans | `font-sans` (default) |
| Eyebrows / metadata | DM Sans | `text-xs uppercase tracking-[0.2em]` |

## Spacing

- Section rhythm: `space-y-6` on dashboard pages
- Cards: `rounded-[2rem]` or `rounded-3xl`, `p-5`–`p-6`
- Grids: `gap-4` mobile, `xl:grid-cols-*` on wide layouts

## Components

Reusable primitives live under `components/ui/` and `components/dashboard/`. See [components.md](components.md).

## Accessibility

- All interactive controls use `focus-visible:outline` with accent color
- Modals trap focus via Escape to close and `aria-modal`
- Tables support keyboard row activation when `onRowClick` is set
- Color contrast targets WCAG AA for body text on `--sx-bg` / `--sx-card-solid`

## Theme toggle

`ThemeProvider` + `theme-store` persist light/dark preference. Toggle: `components/theme/theme-toggle.tsx`.
