# Verification Rules

Run this checklist after writing the HTML file. Fix issues, re-verify, only then hand back.

## Static checks (always run)

Run these via `Bash`/`Grep`/`Read`. Each must pass.

### 1. No em-dashes
```bash
grep -c '—' presentations/<slug>.html
```
Must return `0`. If not, find and replace all `—` with `-`.

### 2. No forbidden fonts
```bash
grep -iE "font-family[^;]*(Inter[^- ]|Roboto|Arial|system-ui|Helvetica|Times New Roman)" presentations/<slug>.html
```
Must return nothing. Plain `Inter` (no `Tight`) and the others are banned.

### 3. No banned AI vocabulary
```bash
grep -iE "delve|leverage|unlock the|navigate the complex|stands as a testament|seamless|evolving landscape|robust solution|vibrant" presentations/<slug>.html
```
Must return nothing. If hits, rewrite those sentences.

### 4. Scroll-snap CSS present
```bash
grep -c "scroll-snap-type" presentations/<slug>.html
```
Must return `>= 1`.

### 5. All referenced assets exist
For each `./assets/<file>` referenced in the HTML, verify the file exists on disk. If missing, either inline the asset as base64 or remove the reference.

### 6. Required section types present
Count occurrences of each section data attribute (`data-section-type="hook"`, etc.):
- exactly 1 `hook`
- exactly 1 `cta`
- at least 1 of each: `quote`, `metric`, `steps`, `before-after`
- total sections between 8 and 14

### 7. No purple-on-white gradient
```bash
grep -iE "linear-gradient.*(#[a-f0-9]*purple|rgb\(.*128.*0.*255)" presentations/<slug>.html
```
Must return nothing. Forbidden combo.

## Dynamic checks (when Claude_in_Chrome is available)

If `mcp__Claude_in_Chrome__*` tools are loaded:

### 8. Render check
1. `navigate` to `file:///<absolute-path>/presentations/<slug>.html`
2. `screenshot` the first viewport (hook section)
3. Scroll to mid-deck (`scroll by 4 * viewport-height`)
4. `screenshot` again
5. Visually scan each screenshot for:
   - Text overflowing its container
   - Missing images (broken icon)
   - Color contrast issues (text invisible on background)
   - Layout broken (overlapping, mis-aligned)

If any issue: fix the CSS, re-write file, re-verify.

### 9. Console errors
1. `read_console_messages`
2. Must have zero errors. Warnings are OK (font loading warnings, etc.).

### 10. Network 404s
1. `read_network_requests`
2. Any 404 means an asset is missing - fix the path or embed inline.

## When Claude_in_Chrome is unavailable

State this in the handback message: *"Headless browser not available - please open the file in Chrome and confirm: (a) scroll-snap works on PgDn, (b) all sections render, (c) no missing images."*

## Auto-fix priority

If multiple issues, fix in this order:
1. Em-dashes (always, every time)
2. Forbidden fonts (always)
3. Asset 404s (functional break)
4. Banned AI vocabulary (voice break)
5. Layout overflow (visual break)
6. Section count / required types (structural)
7. Console errors (last)

## Output of verification step

Print to chat:
```
✓ no em-dashes
✓ no forbidden fonts  
✓ no banned vocab
✓ scroll-snap present
✓ N sections (hook, metric, steps, before-after, quote, ..., cta)
✓ all assets resolved
✓ render check (if Chrome available)
```

If any line fails, mark with `✗` and describe the fix you applied.
