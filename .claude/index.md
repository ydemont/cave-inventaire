# index.html — Line Index (5 066 lines total)

## CSS  (lines 1–1930)

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
| 992–1090  | Valeur modal — wine list, price columns; `@media 720px` |
| 1091–1182 | Drinking-window grid (timeline bars), label scanner |
| 1183–1246 | Row entrance stagger, shake, gold shimmer animations |
| 1247–1474 | France SVG map — stage, views, region shapes, drill-down, tooltip; `@media 720px` |
| 1475–1601 | Sidebar — logo, nav items, active state, footer |
| 1602–1694 | Main content, page header; `@media 900px` |
| 1695–1722 | `@media 1200px` (medium screens — stat tiles) + `@media 900px` |
| 1723–1860 | `@media 600px` — full mobile: hide sidebar, mobile chrome, card table, bottom sheets, charts |
| 1861–1930 | `@media prefers-reduced-motion` |

---

## HTML (lines 1930–2820)

| Lines     | Element |
|-----------|---------|
| 1930–1946 | `<body>`, Chart.js `<script>` |
| 1947–1999 | `#intro` — wax seal overlay |
| 2000–2020 | `#passwordScreen` — login form |
| 2018–2096 | `.app-shell` open + sidebar (logo, "Ajouter" CTA, 6 nav buttons) |
| 2100–2170 | `#page-cave` — 6 stat tiles, toolbar (search + 3 filters + export), `#wineTable` |
| 2171–2253 | `#page-queboire` — 3-step wizard + results + Claude prompt section |
| 2254–2264 | `#page-historique` — `#historyContent` |
| 2265–2278 | `#page-valeur` — 2 stat tiles + `#valueContent` |
| 2279–2568 | `#page-analyses` — 6 chart `<canvas>` + `#aTimeline` + France SVG map (France view, Bordeaux detail, tooltip) |
| 2569–2608 | `#page-primeurs` — 2 stat tiles, `#primTable`, `#primMultiVintage` |
| 2609      | `.app-shell` close |
| 2611–2643 | Mobile chrome: `<header class="mobile-header">` + `<nav class="mobile-bottom-nav">` (6 tabs) |
| 2662–2812 | **Add/Edit modal** — domaine, vin, millésime, bouteilles, magnums, prix, livraison, livre, drinkFrom/To, note, type, scan section |
| 2740–2790 | **Drink log modal** — date, format, qty, stars, note, past tastings list |
| 2791–2800 | Overlays: tasting history, que boire, value tracker, analyses |
| 2800–2812 | Confirm-delete dialog |
| 2811–2820 | Toast container |

---

## JavaScript (lines 2815–5066)

### Config & State
| Lines     | Symbol(s) |
|-----------|-----------|
| 2815–2816 | `SEED[]` — 54-wine fallback array |
| 2819–2820 | `SB_URL`, `SB_KEY` |
| 2822–2850 | `sbFetch()` — Supabase REST wrapper (adds `/rest/v1/` prefix + auth header) |
| 2843–2849 | State: `wines[]`, `tastings{}`, `sortCol`, `sortDir`, `editId`, `deleteId`, `nextId` |

### Data Layer
| Lines     | Symbol(s) |
|-----------|-----------|
| 2851–2870 | `rowToWine()`, `wineToRow()` — snake_case ↔ camelCase mappers |
| 2872–2932 | `load()`, `seedDatabase()`, `save()`, `addWineToDb()`, `saveWineToDb()`, `deleteWineFromDb()`, `resetToOriginal()` |

### Stats & Filters
| Lines     | Symbol(s) |
|-----------|-----------|
| 2934–2967 | `updateStats()` — 6 stat tiles |
| 2968–3065 | `getFiltered()`, `getAppellation()`, `getRegion()`, `populateAppellationFilter()`, `populateChateauFilter()`, `populateMillesimeFilter()`, `sortBy()` |
| 2997      | `APPELLATION_MAP[]` — canonical list with `name` + `region` |

### Render & Modal
| Lines     | Symbol(s) |
|-----------|-----------|
| 3066–3144 | `render()` — inventory table rows (`data-label` for mobile cards) |
| 3141      | `esc()` — XSS escape |
| 3145–3293 | `openAdd()`, `openEdit()`, `closeModal()`, `toggleMagnumPrice()`, `clearForm()`, `saveWine()`, `saveWineWithLookup()` (→ Edge Function `drinking-window`), `commitSave()` |

### CRUD & Utilities
| Lines     | Symbol(s) |
|-----------|-----------|
| 3294–3319 | `confirmDelete()`, `closeConfirm()`, `doDelete()` |
| 3320–3336 | `exportCSV()` |
| 3337–3344 | `toast()` |
| 3345–3384 | `showPage()`, `PAGE_TITLES{}` |

### Tasting Log
| Lines     | Symbol(s) |
|-----------|-----------|
| 3385–3615 | `loadTastings()`, `saveTasting()`, `deleteTastingFromDb()`, `getDrunkCount()`, `openDrink()`, `updateDrinkQtyLabel()`, `updateStockInfo()`, `updateStars()`, `saveDrink()`, `deleteTasting()`, `starsHtml()`, `renderDrinkLog()`, `showHistory()` |
| 3387–3389 | State: `tastings{}`, `drinkWineId`, `drinkRating` |

### Label Scanner
| Lines     | Symbol(s) |
|-----------|-----------|
| 3616–3668 | `triggerCamera()`, `tryPasteFill()`, `fillFormFromWine()`, `checkUrlParams()` |

### Que Boire Wizard
| Lines     | Symbol(s) |
|-----------|-----------|
| 3669–3965 | `openWhatToDrink()`, `wtdReset()`, `closeWtd()`, `generateClaudePrompt()`, `copyPrompt()`, `wtdSelect()`, `wtdAdvance()`, `wtdBack()`, `updateWtdDots()`, `generateRecommendations()` |
| 3670–3672 | State: `wtdAnswers{}`, `wtdCurrentStep`, `WTD_STEPS = 3` |

### Value Tracker
| Lines     | Symbol(s) |
|-----------|-----------|
| 3966–4059 | `getQuarterLabel()`, `loadValueCache()`, `needsRefresh()`, `loadSnapshotFromDb()`, `saveSnapshotToDb()`, `openValueTracker()`, `forceRefreshValues()` |
| 3967–3968 | `VALUE_VERSION = 'v6'`, `valueCache{}` |
| 4060–4286 | `estimateMarketPrice()` — `known{}` dict (line 4069) + appellation/age fallback (line 4111) |
| 4159–4254 | `renderValueTable()` |

### Analyses
| Lines     | Symbol(s) |
|-----------|-----------|
| 4287–4650 | `openAnalyses()`, `renderAnalyses()` |
| 4288      | `aCharts{}` — chart instance registry (always `destroy()` before recreating) |
| 4310–4342 | Summary stats block |
| 4343–4379 | Chart 1 — Spending + avg price per millésime (bar) |
| 4380–4402 | Chart 2 — Bottles by appellation (donut) |
| 4403–4428 | Chart 3 — Top châteaux (horizontal bar) |
| 4429–4445 | Chart 4 — Avg price line |
| 4446–4541 | Chart 5 — France wine map |
| 4502–4541 | Chart 6 — Bottles to drink per year |
| 4542–4568 | Chart 6b — Primeurs vs Spot donut |
| 4569–4650 | Chart 7 — Drinking window timeline |
| 4600–4650 | `filterTimeline()`, state: `_timelineWines[]`, `_timelineYears[]` |

### France Map
| Lines     | Symbol(s) |
|-----------|-----------|
| 4651–4786 | `renderFranceMap()`, `paintMapView()`, `switchMapView()`, `getTotalDrunk()` |
| 4653      | `_mapData{}` — `{regionMap, regionChateaux, subMap, subChateaux}` |

### Auth
| Lines     | Symbol(s) |
|-----------|-----------|
| 4787–4897 | `loadStoredSession()`, `refreshSession()`, `getAccessToken()`, `checkPassword()`, `signOut()`, `runIntro()`, `initAuth()`, `togglePwVisibility()` |
| 4788–4789 | `OWNER_EMAIL = 'yann.demont@gmail.com'`, `authSession` |

### Autocomplete & Init
| Lines     | Symbol(s) |
|-----------|-----------|
| 4898–4958 | `setupAutocomplete()` — keyboard nav (↑↓ Enter Esc) for `f_domaine` + `f_vin` |
| ~5050     | `DOMContentLoaded` — wires autocomplete, calls `initAuth()` |

### Primeurs Page
| Lines     | Symbol(s) |
|-----------|-----------|
| 4959–5066 | `openPrimeurs()` |
| 4980–5002 | Purchase table (wines where `type==='primeur'` and `date` starts with current year) |
| 5003–5066 | Multi-vintage châteaux tile (Bordeaux only, 2+ vintages, gold/oxblood highlights) |
