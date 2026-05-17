# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Session rule:** At the end of every session, update this file to reflect any changes made — new features, architectural decisions, data model changes, Supabase schema updates, or conventions established. Keep it accurate so the next session starts with full context.

## Project Overview

**Cave — Inventaire** is a single-page wine cellar management PWA for a private Bordeaux-focused collection. It is entirely self-contained in one file: `index.html`. There is no build system, no npm, no bundler — just open the file in a browser or serve it statically.

## Running the App

To develop locally, serve the file with any static HTTP server:

```bash
npx serve .
# or
python3 -m http.server 8080
```

The `.claude/launch.json` configures Claude Code to use a local preview server. There are no tests, no linting, and no compilation steps.

## Architecture

Everything lives in `index.html`, structured as three logical sections:

1. **CSS** (lines ~13–1710): All styles, including CSS custom properties (`--ivory`, `--oxblood`, `--gold`, etc.) that define the Bordeaux label aesthetic. The design language is Cormorant Garamond (serif headings) + Inter (sans-serif data). Never introduce Bootstrap or Tailwind — the design system is bespoke.

2. **HTML** (lines ~1710–2505): The app shell with a sidebar nav (240px fixed) and main content area. Pages are toggled via CSS classes (`active`), not routing. The five pages are: `cave` (inventory), `queboire` (what to drink wizard), `historique` (tasting log), `valeur` (portfolio value), `analyses` (charts).

3. **JavaScript** (lines ~2505–end): Vanilla JS, no framework. Key globals:
   - `wines[]` — in-memory array of all wine objects (source of truth after load)
   - `tastings{}` — map of `wineId → [{date, rating, note, format, qty}]`
   - `valueCache{}` — quarterly snapshot cache to avoid recalculating
   - `sortCol`, `sortDir`, `editId`, `deleteId` — UI state

## Data Layer

**Supabase** is used as the backend (raw REST API, no SDK):
- `SB_URL` and `SB_KEY` are hardcoded constants in the JS section
- Three tables: `wines`, `tastings`, `value_snapshots`
- All DB calls go through `sbFetch(path, options)`, a thin fetch wrapper that adds auth headers
- The app falls back to the hardcoded `SEED` array if Supabase is unreachable

**Data model mapping** (`rowToWine` / `wineToRow`):
- App uses camelCase (`prixBouteille`, `drinkFrom`) — DB uses snake_case (`prix_bouteille`, `drink_from`)
- Wine type: `"primeur"` (futures, bought before delivery) or `"spot"` (already in cellar)
- `livre: true` = physically in cellar; `livre: false` = ordered but not yet delivered

## Key Features

**Add/Edit wine**: `openAdd()` / `openEdit(id)` → modal form → `saveWine()`. If `drinkFrom`/`drinkTo` are missing, `saveWineWithLookup()` calls the **`drinking-window` Supabase Edge Function** (deployed at `${SB_URL}/functions/v1/drinking-window`), which proxies to `claude-haiku-4-5` server-side. The Edge Function requires `ANTHROPIC_API_KEY` set as a Supabase secret. Do not call the Anthropic API directly from the browser.

**Tasting log**: `openDrink(id)` → log entry with date, rating (1–5 stars), note, format (bouteille/magnum), qty → saved to Supabase `tastings` table. Drunk bottles are subtracted from displayed stock in the inventory.

**"Que boire" wizard**: 3-step questionnaire (occasion, dish, mood) → `generateRecommendations()` scores in-cellar wines using a local algorithm (no API call) that weighs drinking window, appellation, food pairing, and wine age.

**Portfolio value** (`valeur` page): `openValueTracker()` calculates estimated market prices via `estimateMarketPrice(w)`. Prices are first looked up in a hardcoded `known` dictionary (château + vintage → CHF), then fall back to appellation/age multipliers applied to purchase price. Results are saved quarterly to Supabase `value_snapshots` and cached in memory.

**Analyses page**: 6 Chart.js 4.4.1 charts (canvas elements) + an SVG France map showing bottle counts by wine region. Charts are re-instantiated on each `openAnalyses()` call using the `aCharts` object; always call `chart.destroy()` before recreating.

**France map**: SVG-based, using `data-region` attributes on `<g class="region-group">` elements. Regions are coloured by intensity (`intensity-1` through `intensity-5` CSS classes) based on bottle count. Clicking a region with `has-detail` class drills down to a sub-region view.

**Label scanner**: "Coller depuis Claude" — user pastes a JSON string into a textarea and `tryPasteFill()` parses it to pre-fill the add form. Also supports URL parameter `?wine=<JSON>` for direct form pre-fill.

**Authentication**: SHA-256 hash of password stored in `localStorage` under `cave_auth`. The correct hash is stored in the `PW_HASH` constant and compared directly — never re-hash the plaintext at runtime. Password is `demont-vins`.

## Style Conventions

- UI language is **French** throughout (labels, toasts, button text, error messages)
- Currency is **CHF** (Swiss francs)
- Dates formatted with `fr-CH` locale
- All user-generated HTML is escaped via `esc()` to prevent XSS
- `toast(msg)` for non-blocking feedback; `alert()` only for validation errors that block save

## When Adding Features

- New pages: add a `<section class="page" id="page-XXX">` in the HTML, a `<button class="sidebar-item" data-page="XXX" onclick="showPage('XXX')">` in the sidebar nav, and a handler case in `showPage()`.
- New charts: follow the `aCharts` pattern — destroy before recreate, use `Chart.defaults` already configured for the colour palette.
- Supabase schema changes: update `rowToWine` and `wineToRow` mappers, and the `SEED` array if the new field needs a default for existing records.
- The `estimateMarketPrice` function's `known` dictionary needs manual updating each new vintage year (typically May–June primeur season).
- New Edge Functions: deploy via the Supabase MCP tool (`deploy_edge_function`, project `xhokwnpplbkjtqhjicrs`). Edge functions live at `${SB_URL}/functions/v1/<name>` — do not use `sbFetch` for them (it adds `/rest/v1/` prefix); call with a plain `fetch` including the `apikey` header.

## Appellation & Domaine Conventions

All `vin` and `domaine` values in the database follow strict canonical spelling. **Always use these exact forms** when adding or editing records:

- Domaines: full `Château` with accent, capitalised article (`Château Les Gravières`, not `Château les Gravières`)
- Appellations use the `APPELLATION_MAP` array in the JS as the single source of truth. Do not add free-form text, years, classification ranks (Grand Cru Classé, 5ème, etc.), vineyard names, or AOC suffixes to the `vin` field. Examples of correct forms: `Saint-Émilion Grand Cru`, `Pessac-Léognan`, `Moulis-en-Médoc`, `Lalande-de-Pomerol`, `Savigny-lès-Beaune`.
- When adding new appellations, add them to `APPELLATION_MAP` first (with `name` and `region`), then use the `name` value in the database.
