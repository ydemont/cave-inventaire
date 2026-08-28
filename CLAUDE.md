# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Session rule:** At the end of every session, update this file to reflect any changes made — new features, architectural decisions, data model changes, Supabase schema updates, or conventions established. Keep it accurate so the next session starts with full context.

## Project Overview

**Cave — Inventaire** is a single-page wine cellar management PWA for a private Bordeaux-focused collection. It is entirely self-contained in one file: `index.html`. There is no build system, no npm, no bundler — just open the file in a browser or serve it statically.

## Second App: Cave — YD (mobile)

There is a **second, separate app** deployed at `wine-app-yd.netlify.app` (Netlify site id `bdc28751-6d21-4eda-9493-d61fb9fba445`), built with Claude Design and preferred by the user on phone for its readability. It has no relation to `index.html` architecturally:

- Source lives at `App/Cave-YD-mobile.html` — a React app loaded via in-browser Babel (`<script type="text/babel">`, CDN React/ReactDOM), not vanilla JS.
- It is a **self-contained "bundler" export**: all JS/CSS/font/image assets are inlined as base64 in a `<script type="__bundler/manifest">` block (UUID → `{mime, compressed, data}`), and a small bootstrap script (`__bundler_loading` / `DOMContentLoaded` handler) unpacks them into `blob:` URLs at runtime and injects real `<script>`/`<link>` tags in dependency order. This is what makes the file work standalone from a single upload — do not "clean up" the manifest/template scripts, they are load-bearing.
- **Important history**: earlier exports (June 9 `Cave-YD-app.html`, and a June 17 manual Netlify drag-and-drop) only contained the shell HTML referencing external blob-UUID asset URLs with no actual asset content — those were broken (404s on every script/font) both locally and once deployed. Always verify a new export actually contains a populated `__bundler/manifest` (not an `ext_resources` list pointing elsewhere) before treating it as deployable.
- **Redeploying**: Netlify's site-level MCP `deploy-site` tool takes no directory/path argument and isn't reliable for this single-file, non-git-linked site (it timed out / 502'd when tried). The verified working method is the raw Netlify API digest-deploy flow, run manually via `curl` with a user-supplied personal access token (`app.netlify.com/user/applications`):
  1. `POST /api/v1/sites/{site_id}/deploys` with `{"files": {"/index.html": "<sha1 of file>"}}`
  2. `PUT /api/v1/deploys/{deploy_id}/files/index.html` with the raw file bytes as body
  3. `POST /api/v1/sites/{site_id}/deploys/{deploy_id}/restore` to publish it live
  The token is only needed for the duration of the deploy; the user can revoke it after.
- The Netlify project `my-cellar-yd` (site id `af0c6c49-008c-4578-a41e-c135b25a7c5b`) is the deployed copy of this repo's `index.html` — the laptop-preferred, more detailed app.

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

1. **CSS** (lines ~13–1930): All styles, including CSS custom properties (`--ivory`, `--oxblood`, `--gold`, etc.) that define the Bordeaux label aesthetic. The design language is Cormorant Garamond (serif headings) + Inter (sans-serif data). Never introduce Bootstrap or Tailwind — the design system is bespoke.

2. **HTML** (lines ~1930–2660): The app shell with a sidebar nav (240px fixed) and main content area. Pages are toggled via CSS classes (`active`), not routing. The seven pages are: `cave` (inventory), `queboire` (what to drink wizard), `historique` (tasting log), `cellier3d` (3D fridge visualization), `valeur` (portfolio value), `analyses` (charts), `primeurs` (current-year primeur campaign tracker). After the app shell closing tag, two mobile-only elements are rendered: `<header class="mobile-header">` and `<nav class="mobile-bottom-nav">` — hidden by default, activated via `@media (max-width: 600px)`.

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
- `shelf` (1–5), `slotCol` (1–7), `slotRow` (1–7) — optional physical position anchor for the Cellier 3D page (see below). Nullable; most records have none.

## Key Features

**Add/Edit wine**: `openAdd()` / `openEdit(id)` → modal form → `saveWine()`. If `drinkFrom`/`drinkTo` are missing, `saveWineWithLookup()` calls the **`drinking-window` Supabase Edge Function** (deployed at `${SB_URL}/functions/v1/drinking-window`), which proxies to `claude-haiku-4-5` server-side. The Edge Function requires `ANTHROPIC_API_KEY` set as a Supabase secret. Do not call the Anthropic API directly from the browser.

The `f_domaine` and `f_vin` fields have custom autocomplete dropdowns (`setupAutocomplete()`). `f_domaine` suggests unique château names already in `wines[]`; `f_vin` suggests names from `APPELLATION_MAP`. Keyboard navigation (↑↓ Enter Escape) is supported. Both are initialised in the `DOMContentLoaded` listener.

**Tasting log**: `openDrink(id)` → log entry with date, rating (1–5 stars), note, format (bouteille/magnum), qty → saved to Supabase `tastings` table. Drunk bottles are subtracted from displayed stock in the inventory. All tastings are now loaded upfront at startup via `loadTastings()` (called inside `load()`), so `getDrunkCount(wineId)` is always accurate on every page.

**"Que boire" wizard**: 3-step questionnaire (occasion, dish, mood) → `generateRecommendations()` scores in-cellar wines using a local algorithm (no API call) that weighs drinking window, appellation, food pairing, and wine age.

**Portfolio value** (`valeur` page): `openValueTracker()` calculates estimated market prices via `estimateMarketPrice(w)`. Prices are looked up via two keys: `dom_firstWordOfVin_vintage` first (disambiguates multi-cuvée domains like Louis Jadot), then `dom_vintage` as fallback; finally appellation/age multipliers applied to purchase price. `dom` = domaine lowercased with the `Château`/`Chateau` prefix stripped — articles like "la", "les", "clos" are **not** stripped (e.g. `'la clef de voûte_2022'`, `'clos floridène_2021'`). Results are saved quarterly to Supabase `value_snapshots` (`VALUE_VERSION = 'v7'`); bump this constant to force recalculation. The table now shows 6 columns: Domaine+Appellation | Stock | Achat | Marché+CHF/btl | +/− | %.

**Analyses page**: 6 Chart.js 4.4.1 charts (canvas elements) + an SVG France map showing bottle counts by wine region. Charts are re-instantiated on each `openAnalyses()` call using the `aCharts` object; always call `chart.destroy()` before recreating.

**Primeurs page** (`openPrimeurs()`): Tracks the current-year primeur buying campaign. Shows:
- Two stat tiles: total CHF spent, total bottles + magnums bought.
- A purchase table listing all wines where `type === 'primeur'` and `date` starts with the current year, sorted by château.
- A multi-vintage tile (Bordeaux wines only, via `getRegion()`) showing châteaux held across 2+ distinct vintages. Châteaux bought this year are highlighted in gold; vintages purchased as this year's primeurs are highlighted in oxblood. Bottle counts reflect actual remaining stock using `getDrunkCount()`.
- "This year" is always `new Date().getFullYear()` — no hardcoded year.

**Cellier 3D** (`openCellier3D()`): A Three.js (CDN, r128, no build step — same pattern as Chart.js) visualization of the physical cellar, a Haier HWS247GGU1 (5 wooden shelves, 247-bottle rated capacity, ~1900×597×714mm). Each shelf is modeled as a 7×7 grid of slots (49 × 5 = 245 ≈ rated capacity — this is an estimate from product research, not the literal manual, easy to retune via `SHELF_COLS`/`SHELF_ROWS`/`SHELF_COUNT`).
- **Position model**: a wine entry stores ONE manually-chosen anchor slot (`shelf`/`slotCol`/`slotRow`), not one coordinate per physical bottle. Its currently-remaining bottles/magnums (via `getDrunkCount`) render sequentially from that anchor, row-major (col 1→7, then next row). If a wine's count overflows the 7×7 grid, the overflow "stacks" visually above the shelf rather than spilling onto another shelf.
- **`computeShelfOccupancy(shelfNum, excludeWineId)`** is the single shared layout algorithm — used by both the edit-modal slot picker AND the 3D renderer, so they can never drift out of sync. Fully-drunk wines are skipped automatically (no manual slot cleanup needed when a bottle is finished).
- **Shelf numbering**: shelf 1 = top ("haut"), shelf 5 = bottom ("bas"). `cellier3DShelfY(shelfNum, shelfGap)` is the single source of truth for this mapping — used by both the shelf meshes and the bottle placement. Don't compute shelf Y positions ad hoc elsewhere.
- **Slot picker**: the edit modal (`openEdit`/`saveWine`) has a "Position dans la cave" field group with a shelf `<select>` and a 7×7 clickable grid (`renderSlotPicker()`) showing free/occupied/selected cells live, scoped to the wine being edited via `excludeWineId`.
- **3D scene** (`initCellier3DScene()`, lazy-initialized on first visit, not torn down/recreated on revisit — only `refreshCellier3DBottles()` re-runs): the cabinet is built from open panels (back/sides/top/bottom + a separate transparent glass front), NOT a closed box — a solid box's opaque front face would hide everything inside. Bottle colors deliberately avoid the shelf's gold-wood tone (`0x7d6024`) so they don't visually blend in.
- **Interaction**: raycasting on pointer move/click against bottle meshes shows a floating popover (`cellier3dEditFromPopover()` etc.) with wine details and a "Modifier" button that calls the real `openEdit(id)`.
- **Unassigned-wines banner**: wines with `shelf == null` (and still-remaining stock) are listed as clickable chips at the top of the page, via `renderCellier3DBanner()`.

**Responsive inventory table**: The cave table progressively hides columns as the viewport narrows — never horizontal-scrolls on common screen sizes:
- `≤ 1200px`: hide Note (col 10) + Bu (col 11); tighten cell padding.
- `≤ 900px`: also hide Livraison (col 8); sidebar folds into a top nav bar.
- `≤ 768px`: also hide Fenêtre (col 9).
- `≤ 600px`: full card view (all fields shown as labelled rows).
Column hiding uses `#wineTable th:nth-child(N), #wineTable td:nth-child(N) { display: none; }` — scoped to `#wineTable` so it only affects the inventory table.

**Mobile layout**: Activated at `≤ 600px` via CSS media query. The sidebar is hidden; a fixed top header (`<header class="mobile-header">`) shows the current page title and a "Ajouter" CTA (visible only on the cave page). A fixed bottom tab bar (`<nav class="mobile-bottom-nav">`) provides navigation with 6 icon+label tabs. The cave inventory table transforms into cards via CSS (`display:block` on `tr`/`td`) using `data-label` attributes on each `<td>` rendered by `renderTable()`. Modals become bottom sheets (full-width, rounded top corners). `showPage()` syncs the mobile header title and bottom nav active state via the `PAGE_TITLES` constant. At `≤ 1200px` (MacBook Air range), stat tile padding and font sizes are reduced so all 6 tiles fit without overflow.

**France map**: SVG-based, using `data-region` attributes on `<g class="region-group">` elements. Regions are coloured by intensity (`intensity-1` through `intensity-5` CSS classes) based on bottle count. Clicking a region with `has-detail` class drills down to a sub-region view.

**Label scanner**: "Coller depuis Claude" — user pastes a JSON string into a textarea and `tryPasteFill()` parses it to pre-fill the add form. Also supports URL parameter `?wine=<JSON>` for direct form pre-fill.

**Authentication**: Uses **Supabase Auth** (`signInWithPassword` via REST, no SDK). The owner email is hardcoded as `OWNER_EMAIL = 'yann.demont@gmail.com'`. On login, the JWT session is stored in `localStorage` under `cave_session` and auto-refreshed before expiry via `getAccessToken()`. `sbFetch()` sends `Authorization: Bearer <jwt>` when a session exists, falling back to the anon key for unauthenticated reads.

**RLS policies**: All four tables (`wines`, `tastings`, `value_snapshots`, `keepalive`) have RLS enabled. SELECT is open to the anon role (data loads at startup without login). INSERT/UPDATE/DELETE require `auth.uid() IS NOT NULL` (authenticated users only). Login is therefore required to add, edit, or delete any record. The `signOut()` function clears the session and returns to the login screen.

## Style Conventions

- UI language is **French** throughout (labels, toasts, button text, error messages)
- Currency is **CHF** (Swiss francs)
- Dates formatted with `fr-CH` locale
- All user-generated HTML is escaped via `esc()` to prevent XSS
- `toast(msg)` for non-blocking feedback; `alert()` only for validation errors that block save

## When Adding Features

- New pages: add a `<section class="page" id="page-XXX">` in the HTML, a `<button class="sidebar-item" data-page="XXX" onclick="showPage('XXX')">` in the sidebar nav, a `<button class="mbn-item" data-page="XXX">` in the `.mobile-bottom-nav`, a title entry in the `PAGE_TITLES` constant, and a handler case in `showPage()`.
- New charts: follow the `aCharts` pattern — destroy before recreate, use `Chart.defaults` already configured for the colour palette.
- Supabase schema changes: update `rowToWine` and `wineToRow` mappers, and the `SEED` array if the new field needs a default for existing records.
- The `estimateMarketPrice` function's `known` dictionary needs manual updating each new vintage year (typically May–June primeur season). Keys must match the generated `dom` value exactly — `dom` strips only the `Château`/`Chateau` prefix, not articles. Always verify key matching by tracing `domaine.toLowerCase().replace(/^ch[âa]teau\s+/i,'')`. For multi-cuvée domains, use the long key format `dom_firstWordOfVin_vintage`.
- New Edge Functions: deploy via the Supabase MCP tool (`deploy_edge_function`, project `xhokwnpplbkjtqhjicrs`). Edge functions live at `${SB_URL}/functions/v1/<name>` — do not use `sbFetch` for them (it adds `/rest/v1/` prefix); call with a plain `fetch` including the `apikey` header.
- New 3D geometry in Cellier 3D: never build an enclosing object as a single closed `BoxGeometry` if the camera needs to see inside it — the opaque front face will completely hide the interior. Build it from individual open panels instead, with a separate transparent material for the side the camera looks through.

## Known Pre-existing Issues (not yet fixed, found incidentally)

- `getAccessToken()` can throw `ReferenceError: Cannot access 'authSession' before initialization` on cold load if `loadTastings()` fires before the `let authSession` declaration further down the script executes (TDZ). Harmless in practice (caught and logged), but worth cleaning up — e.g. hoist `let authSession = null;` near the top of the script.
- The inventory table has no `id="wineTable"` wrapper element, so the `#wineTable th:nth-child(N)...` responsive column-hiding CSS rules (and the `#wineTable` reference in this file) never actually match anything; the table body's real id is `tbody`. The responsive hiding may currently be working by coincidence of other rules, or may not be working at all — needs verification.
- The "Scanner une étiquette" block in the add/edit modal uses inline `style="background:var(--surface-2);border:1px solid var(--rule-strong)..."` — `--surface-2` and `--rule-strong` are not defined anywhere in `:root`, so they silently resolve to nothing. The `.form-grid` "full-width" fields also use a class `form-full` that doesn't match the actual CSS rule `.form-grid .full` — full-width fields in the modal are likely not spanning full width as intended.

## Appellation & Domaine Conventions

All `vin` and `domaine` values in the database follow strict canonical spelling. **Always use these exact forms** when adding or editing records:

- Domaines: full `Château` with accent, capitalised article (`Château Les Gravières`, not `Château les Gravières`)
- Appellations use the `APPELLATION_MAP` array in the JS as the single source of truth. Do not add free-form text, years, classification ranks (Grand Cru Classé, 5ème, etc.), vineyard names, or AOC suffixes to the `vin` field. Examples of correct forms: `Saint-Émilion Grand Cru`, `Pessac-Léognan`, `Moulis-en-Médoc`, `Lalande-de-Pomerol`, `Savigny-lès-Beaune`.
- When adding new appellations, add them to `APPELLATION_MAP` first (with `name` and `region`), then use the `name` value in the database.
