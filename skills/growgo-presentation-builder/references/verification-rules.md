# Verification Rules (Growgo variant)

Static + dynamic checks after writing the HTML file. **Inherits parent checks except font check**, plus Growgo-specific additions.

## Static checks (always run)

### 1. No em-dashes
```bash
grep -c '—' presentations/<slug>.html
```
Must return `0`.

### 2. Font check (Growgo-specific - Roboto allowed, others forbidden)
```bash
grep -iE "font-family[^;]*(\bInter\b|\bRoboto\b)" presentations/<slug>.html
```
Roboto MUST appear. Inter MUST NOT.

Then check no forbidden fonts as primary:
```bash
grep -iE "font-family:[ ]*['\"]?(Helvetica|Times New Roman|system-ui)" presentations/<slug>.html
```
Must return empty.

### 3. Background check
```bash
grep -E "background[:-][^;]*#[Ff][Ff][Ff][Ff][Ff][Ff]" presentations/<slug>.html | grep -v "transparent"
```
Must return empty. No `#FFFFFF` as bg (cards on dark sections may use white text but bg must be `#EFEFEF` or `#1E1E1E` or dark cards).

### 4. Yellow highlight present on hook
```bash
grep -c 'class="hl"' presentations/<slug>.html
```
Must return ≥ 1.

### 5. Logo embedded
```bash
grep -c 'class="brand-mark"' presentations/<slug>.html
```
Must return ≥ 2 (hook + cta).

### 6. Banned ekspercka phrases (PL)
```bash
grep -iE "Rekomendujemy|Zalecamy|Musicie|Trzeba|Konieczne jest|Myślę że|Widzę że|Dla mnie" presentations/<slug>.html
```
Must return empty.

### 7. Banned ekspercka phrases (EN)
```bash
grep -iE "we recommend|you should|you must|it's necessary|I think|I see that" presentations/<slug>.html
```
Must return empty.

### 8. Banned universal Growgo phrases
```bash
grep -iE "Mieliśmy ogromną przyjemność|Z przyjemnością podzielimy|Pragniemy zaprezentować|Mechanizm funkcjonowania polega na|niezwykle ważny|w zakresie" presentations/<slug>.html
```
Must return empty.

### 9. No emoji
```bash
grep -P '[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}\x{2700}-\x{27BF}]' presentations/<slug>.html
```
Must return empty.

### 10. Brand spelling
```bash
grep -E "GrowGo|GROWGO|growgo" presentations/<slug>.html | grep -v "growgo-presentation-builder\|growgo.io\|@growgo"
```
Must return empty. Only "Growgo" allowed in copy (lowercase only in URLs/handles).

### 11. Scroll-snap present
```bash
grep -c "scroll-snap-type" presentations/<slug>.html
```
Must return ≥ 1.

### 12. Required section types
```bash
grep -oE 'data-section-type="[^"]+"' presentations/<slug>.html | sort | uniq -c
```
Must have: 1 hook, 1 cta, ≥1 each of quote, metric, steps, before-after. Total 8-14.

### 13. Yellow `#FEBF2D` not used as text color on light bg
Hard to automate fully. Visual inspection step - check the screenshot via dynamic check below.

## Dynamic checks (Claude_in_Chrome)

Same as parent. Open the file, screenshot hook + mid + CTA sections.

Visual scan:
- Logo aspect ratio not distorted
- Yellow highlight visible on hook headline
- Card shadows present on light bg
- No card shadows on dark bg
- Step number colors cycle correctly (yellow → green → blue → purple)
- No centered headlines

## Auto-fix priority

1. Em-dashes (always)
2. Forbidden fonts (would break brand instantly)
3. Pure white bg (brand violation)
4. Missing yellow highlight on hook (signature element missing)
5. Banned phrases (tone violation)
6. Emoji (brand violation)
7. Logo missing or distorted (visual)
8. Wrong brand spelling
9. Banned text contrast pairings (accessibility)

## Output of verification

Print to chat:
```
✓ no em-dashes
✓ Roboto present, no forbidden fonts
✓ no pure-white bg
✓ yellow highlight on hook (N occurrences)
✓ logo embedded (hook + cta)
✓ no banned ekspercka phrases (PL + EN)
✓ no banned universal phrases
✓ no emoji
✓ brand spelling "Growgo" consistent
✓ scroll-snap present
✓ N sections (hook, metric, steps, before-after, quote, ..., cta)
```
