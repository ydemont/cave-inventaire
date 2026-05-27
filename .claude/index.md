# index.html — Line Index (5 100 lines total)

## CSS  (lines 1–1960)

| Lines     | Content |
|-----------|---------|
| 1–12      | `<head>` — meta, fonts (Cormorant Garamond + Inter), Chart.js CDN |
| 13–69     | CSS custom properties — `--ivory`, `--oxblood`, `--gold`, colours + structural vars |
| 70–136    | Reset, base styles, paper texture, noise grain, scrollbar |
| 137–368   | `#intro` wax seal — disk, fluted edge, crest, animation |
| 369–601   | Stat tiles, toolbar, inventory `<table>` rows |
| 602–722   | Empty state, badges (livré/primeur/spot), icon buttons, bottle chip |
| 723–822   | Form fields, autocomplete dropdown, buttons (primary/ghost/danger) |
| 778–936   | Drink/log modal — stars, format picker, tasting rows |
| 823–991   | Que boire wizard — step cards, results; `@media 720px` |
| 952–958   | `@media (max-width: 720px)` — value top-grid collapse + value row 5-col (hide Achat) |
| 992–1035  | **Valeur rows** — `.value-rows-header`, `.wine-value-row` (6-col grid: `1fr 70px 110px 130px 85px 65px`), `.wv-stock`, delta colours |
| 1036–1090 | Analyses page styles — `.analyses-summary`, `.chart-panel`, `.chart-wrap-canvas` |
| 1091–1182 | Drinking-window grid (timeline bars), label scanner |
| 1183–1246 | Row entrance stagger, shake, gold shimmer animations |
| 1247–1474 | France SVG map — stage, views, region shapes, drill-down, tooltip; `@media 720px` |
| 1475–1601 | Sidebar — logo, nav items, active state, footer |
| 1602–1694 | Main content, page header; `@media 900px` (sidebar folds to top nav) |
| 1705–1735 | **Responsive inventory table** breakpoints: |
|           | `@media 1200px` — hide Note(10)+Bu(11), tighten padding |
|           | `@media 900px` — hide Livraison(8), tighten more |
|           | `@media 768px` — hide Fenêtre(9), tightest padding |
| 1744–1752 | `@media 600px` — value rows: Name\|Marché\|% (hide Stock/Achat/+/-) |
| 1755–1895 | `@media 600px` full mobile — sidebar hidden, card table, bottom sheets |
| 1886–1893 | Mobile value rows: same 3-col layout |
| 1895–1897 | `@media prefers-reduced-motion` |
| 1900–1960 | Autocomplete dropdown, Primeurs page styles |

---

## HTML (lines 1960–2860)

| Lines     | Element |
|-----------|---------|
| 1960–1976 | `<body>`, Chart.js `<script>` |
| 1977–1999 | `#intro` — wax seal overlay |
| 2000–2020 | `#passwordScreen` — login form |
| 2018–2096 | `.app-shell` open + sidebar (logo, "Ajouter" CTA, 6 nav buttons) |
| 2100–2170 | `#page-cave` — 6 stat tiles, toolbar (search + 6 filters + export), `#wineTable` (12 cols) |
| 2171–2253 | `#page-queboire` — 3-step wizard + results + Claude prompt section |
| 2254–2264 | `#page-historique` — `#historyContent` |
| 2265–2278 | `#page-valeur` — 2 stat tiles + `#valueContent` |
| 2279–2568 | `#page-analyses` — 6 chart `<canvas>` + `#aTimeline` + France SVG map (France view, Bordeaux detail, tooltip) |
| 2569–2608 | `#page-primeurs` — 2 stat tiles, `#primTable`, `#primMultiVintage` |
| 2609      | `.app-shell` close |
| 2611–2643 | Mobile chrome: `<header class="mobile-header">` + `<nav class="mobile-bottom-nav">` (6 tabs) |
| 2662–2812 | **Add/Edit modal** — all wine fields + scan section |
| 2740–2790 | **Drink log modal** — date, format, qty, stars, note, past tastings list |
| 2791–2812 | Overlays: tasting history, que boire, value tracker, analyses, confirm-delete, toast |

---

## JavaScript (lines 2850–5100)

### Config & State
| Lines     | Symbol(s) |
|-----------|-----------|
| 2850–2851 | `SEED[]` — 54-wine fallback array |
| 2853–2855 | `SB_URL`, `SB_KEY` |
| 2857–2876 | `sbFetch()` — Supabase REST wrapper (adds `/rest/v1/` prefix + auth header) |
| 2877–2884 | State: `wines[]`, `tastings{}`, `sortCol`, `sortDir`, `editId`, `deleteId`, `nextId` |

### Data Layer
| Lines     | Symbol(s) |
|-----------|-----------|
| 2886–2905 | `rowToWine()`, `wineToRow()` — snake_case ↔ camelCase mappers |
| 2907–2966 | `load()`, `seedDatabase()`, `save()`, `addWineToDb()`, `saveWineToDb()`, `deleteWineFromDb()`, `resetToOriginal()` |

### Stats & Filters
| Lines     | Symbol(s) |
|-----------|-----------|
| 2969–3002 | `updateStats()` — 6 stat tiles |
| 3004–3093 | `getFiltered()`, `getAppellation()`, `getRegion()`, `populateAppellationFilter()`, `populateChateauFilter()`, `populateMillesimeFilter()`, `sortBy()` |
| 3032      | `APPELLATION_MAP[]` — canonical list with `name` + `region` |

### Render & Modal
| Lines     | Symbol(s) |
|-----------|-----------|
| 3102–3175 | `render()` — inventory table rows (`data-label` for mobile cards) |
| 3176      | `esc()` — XSS escape |
| 3181–3328 | `openAdd()`, `openEdit()`, `closeModal()`, `toggleMagnumPrice()`, `clearForm()`, `saveWine()`, `saveWineWithLookup()` (→ Edge Function `drinking-window`), `commitSave()` |

### CRUD & Utilities
| Lines     | Symbol(s) |
|-----------|-----------|
| 3330–3354 | `confirmDelete()`, `closeConfirm()`, `doDelete()` |
| 3356–3371 | `exportCSV()` |
| 3373–3379 | `toast()` |
| 3381–3427 | `showPage()`, `PAGE_TITLES{}` |

### Tasting Log
| Lines     | Symbol(s) |
|-----------|-----------|
| 3420–3650 | `loadTastings()`, `saveTasting()`, `deleteTastingFromDb()`, `getDrunkCount()`, `openDrink()`, `updateDrinkQtyLabel()`, `updateStockInfo()`, `updateStars()`, `saveDrink()`, `deleteTasting()`, `starsHtml()`, `renderDrinkLog()`, `showHistory()` |

### Label Scanner
| Lines     | Symbol(s) |
|-----------|-----------|
| 3652–3702 | `triggerCamera()`, `tryPasteFill()`, `fillFormFromWine()`, `checkUrlParams()` |

### Que Boire Wizard
| Lines     | Symbol(s) |
|-----------|-----------|
| 3704–4000 | `openWhatToDrink()`, `wtdReset()`, `closeWtd()`, `generateClaudePrompt()`, `copyPrompt()`, `wtdSelect()`, `wtdAdvance()`, `wtdBack()`, `updateWtdDots()`, `generateRecommendations()` |

### Value Tracker
| Lines     | Symbol(s) |
|-----------|-----------|
| 4001–4094 | `getQuarterLabel()`, `loadValueCache()`, `needsRefresh()`, `loadSnapshotFromDb()`, `saveSnapshotToDb()`, `openValueTracker()` |
| 4002      | `VALUE_VERSION = 'v7'` — bump to force snapshot recalculation |
| 4095–4226 | **`estimateMarketPrice()`** — two-key lookup: `dom_vinPart_vintage` then `dom_vintage`, then appellation/age fallback |
|           | `known{}` dict at line 4101 — 2021/2022/2023/2024 primeurs + 2026 spot wines |
|           | Key rule: `dom` = domaine lowercased, `Château` prefix stripped only — articles ("la", "les", "clos") kept |
| 4227–4335 | **`renderValueTable()`** — 6-col layout: Domaine+Appellation \| Stock \| Achat \| Marché+CHF/btl \| +/− \| % |
| 4336–4341 | `forceRefreshValues()` |

### Analyses
| Lines     | Symbol(s) |
|-----------|-----------|
| 4368–4730 | `openAnalyses()`, `renderAnalyses()` |
| 4369      | `aCharts{}` — chart instance registry (always `destroy()` before recreating) |
| 4376+     | Chart 1 Spending, Chart 2 Appellation donut, Chart 3 Top châteaux, Chart 4 Avg price, Chart 5 France map, Chart 6 Bottles/year, Chart 6b Primeurs/Spot, Chart 7 Drinking window timeline |
| 4683      | `filterTimeline()` |

### France Map
| Lines     | Symbol(s) |
|-----------|-----------|
| 4732–4862 | `renderFranceMap()`, `paintMapView()`, `switchMapView()`, `getTotalDrunk()` |

### Auth
| Lines     | Symbol(s) |
|-----------|-----------|
| 4868–4977 | `loadStoredSession()`, `refreshSession()`, `getAccessToken()`, `checkPassword()`, `signOut()`, `runIntro()`, `initAuth()`, `togglePwVisibility()` |
| 4869      | `OWNER_EMAIL = 'yann.demont@gmail.com'` |

### Autocomplete & Init
| Lines     | Symbol(s) |
|-----------|-----------|
| 4980–5039 | `setupAutocomplete()` — keyboard nav (↑↓ Enter Esc) for `f_domaine` + `f_vin` |
| ~5085     | `DOMContentLoaded` — wires autocomplete, calls `initAuth()` |

### Primeurs Page
| Lines     | Symbol(s) |
|-----------|-----------|
| 5041–5100 | `openPrimeurs()` |
| ~5061     | Purchase table (type=primeur, current year) |
| ~5078     | Multi-vintage châteaux tile (Bordeaux only, 2+ vintages, gold/oxblood highlights) |

---

## Responsive Inventory Table — Column Hide Map

| Breakpoint | Columns hidden | Selector used |
|------------|---------------|---------------|
| ≤ 1200px   | Note (10), Bu (11) | `#wineTable th/td:nth-child(10/11)` |
| ≤ 900px    | + Livraison (8) | `#wineTable th/td:nth-child(8)` |
| ≤ 768px    | + Fenêtre (9) | `#wineTable th/td:nth-child(9)` |
| ≤ 600px    | Card view (all cols as rows) | `display:block` on `tr`/`td` |

## Valeur Table — Responsive Column Hide Map

| Breakpoint | Columns shown | Grid |
|------------|--------------|------|
| > 720px    | All 6 | `1fr 70px 110px 130px 85px 65px` |
| ≤ 720px    | Name \| Stock \| Marché \| +/− \| % (hide Achat) | `1fr 65px 130px 85px 65px` |
| ≤ 600px    | Name \| Marché \| % (hide Stock, Achat, +/−) | `1fr 120px 65px` |
