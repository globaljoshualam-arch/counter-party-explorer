# Airwallex Frontend Design System

> A comprehensive design system for building Airwallex-branded interfaces.
> Based on official Brand Guidelines (March 2026).

---

## Design Philosophy

**Tone**: Confident, warm, globally-minded fintech
**Principles**: Inform, Inspire, Educate, Empower
**Aesthetic**: Clean minimalism with bold orange energy

Airwallex interfaces should feel:
- **Professional** — Trustworthy for handling global payments
- **Warm** — Approachable through orange accents and clear language
- **Global** — Designed for international audiences with localization in mind
- **Efficient** — Every element serves a purpose

---

## Quick Start

### Option 1: CSS Variables Only

```html
<!-- In your HTML head -->
<link rel="stylesheet" href="./design-system/index.css">
```

```css
/* Or in your CSS/SCSS */
@import './design-system/index.css';

/* Use variables */
.my-button {
  background: var(--awx-orange-500);
  border-radius: var(--awx-radius-lg);
}
```

### Option 2: With Tailwind CSS

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

Copy `tailwind.config.js` from this design system, then:

```html
<button class="bg-awx-orange-500 hover:bg-awx-orange-600 text-white 
               px-6 py-3 rounded-awx-lg shadow-awx-orange transition">
  Get started
</button>
```

### Option 3: React/Component Library

```jsx
import './design-system/index.css';

function Button({ children, variant = 'primary' }) {
  return (
    <button className="awx-btn-primary">
      {children}
    </button>
  );
}
```

---

## File Structure

```
design-system/
├── index.css                    # Main entry point (imports all tokens)
├── AIRWALLEX-DESIGN-SYSTEM.md   # This documentation
├── CHEATSHEET.md                # Quick reference
├── tailwind.config.js           # Tailwind configuration
├── tokens/
│   ├── colors.css               # Color system & product themes
│   ├── typography.css           # Fonts, sizes, weights
│   └── spacing.css              # Spacing, radius, shadows, z-index
└── components/
    └── guidelines.md            # Component patterns & code examples
```

---

## Core Design Tokens

### Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--awx-orange-500` | #FF6B40 | Primary brand, CTAs, links |
| `--awx-spend-500` | #FF5082 | Spend product category |
| `--awx-payments-500` | #2B7FFF | Payments product category |
| `--awx-platform-500` | #A855F7 | Platform APIs category |
| `--awx-gray-900` | #171717 | Primary text |
| `--awx-gray-200` | #E5E5E5 | Borders |

### Typography

| Token | Value | Usage |
|-------|-------|-------|
| `--awx-font-sans` | Circular, DM Sans | All text |
| `--awx-text-base` | 16px | Body copy |
| `--awx-text-4xl` | 36px | Page headings |
| `--awx-font-medium` | 500 | Labels, buttons |

### Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--awx-space-4` | 16px | Form gaps, small padding |
| `--awx-space-6` | 24px | Card padding |
| `--awx-space-8` | 32px | Section gaps |
| `--awx-radius-lg` | 12px | Buttons, cards |

---

## Product Category Themes

Apply these classes to scope product-specific styling:

```html
<section class="awx-theme-business-accounts">
  <!-- Uses orange accent colors -->
</section>

<section class="awx-theme-spend">
  <!-- Uses pink accent colors -->
</section>

<section class="awx-theme-payments">
  <!-- Uses blue accent colors -->
</section>

<section class="awx-theme-platform">
  <!-- Uses purple accent colors -->
</section>
```

---

## Dark Mode

The design system supports dark mode via class or data attribute:

```html
<!-- Option 1: Class -->
<html class="dark">

<!-- Option 2: Data attribute -->
<html data-theme="dark">
```

All semantic tokens automatically adjust:
- `--awx-bg-primary` becomes dark
- `--awx-text-primary` becomes light
- Borders and accents adapt accordingly

---

## Fonts

### Required Font Files

**Primary**: Circular (requires license)
- Download from Lineto: https://lineto.com/typefaces/circular

**Fallback**: DM Sans (Google Fonts - free)
```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
```

**Chinese**: Source Han Sans / Noto Sans SC
```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## Brand Guidelines Summary

### Logo
- Use provided assets (SVG for digital)
- Maintain clear space
- Never alter, crop, angle, or add effects
- Requires high-contrast backgrounds

### Icons
- **Detailed icons**: Use product-category colors, for marketing
- **Simple icons**: Black or white only, for UI
- Never mix detailed and simple on same page

### Content Style
- eCommerce, fintech, Cashback, WebApp (one word each)
- US$50 format for currencies
- 21 July 2025 format for dates
- Oxford commas required
- Sentence case for headings

---

## Related Files

- [CHEATSHEET.md](./CHEATSHEET.md) — Quick token reference
- [components/guidelines.md](./components/guidelines.md) — Full component documentation
- [tokens/colors.css](./tokens/colors.css) — Complete color system
- [tokens/typography.css](./tokens/typography.css) — Font definitions
- [tokens/spacing.css](./tokens/spacing.css) — Layout tokens
- [tailwind.config.js](./tailwind.config.js) — Tailwind integration
