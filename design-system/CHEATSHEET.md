# Airwallex Design System Cheatsheet

Quick reference for the most commonly used tokens and patterns.

---

## Colors

### Brand Orange (Primary)
```css
--awx-orange-500: #FF6B40;  /* Primary CTA, links, accents */
--awx-orange-600: #F54D1F;  /* Hover state */
--awx-orange-100: #FFEBE5;  /* Subtle backgrounds */
```

### Product Categories
| Product | Color | Hex |
|---------|-------|-----|
| Business Accounts | Orange | `#FF6B40` |
| Spend | Pink | `#FF5082` |
| Payments | Blue | `#2B7FFF` |
| Platform APIs | Purple | `#A855F7` |

### Semantic Colors
```css
--awx-success-500: #22C55E;
--awx-warning-500: #F59E0B;
--awx-error-500: #EF4444;
--awx-info-500: #3B82F6;
```

### Grays
```css
--awx-gray-50: #FAFAFA;   /* Subtle bg */
--awx-gray-200: #E5E5E5;  /* Borders */
--awx-gray-500: #737373;  /* Secondary text */
--awx-gray-900: #171717;  /* Primary text */
```

---

## Typography

### Font Stack
```css
font-family: 'Circular', 'DM Sans', sans-serif;
```

### Sizes
| Name | Size | Use |
|------|------|-----|
| `--awx-text-xs` | 12px | Captions, badges |
| `--awx-text-sm` | 14px | Body small, labels |
| `--awx-text-base` | 16px | Body text |
| `--awx-text-lg` | 18px | Lead paragraphs |
| `--awx-text-xl` | 20px | H5 |
| `--awx-text-2xl` | 24px | H4 |
| `--awx-text-3xl` | 30px | H3 |
| `--awx-text-4xl` | 36px | H2 |
| `--awx-text-5xl` | 48px | H1 |

### Weights
```css
--awx-font-normal: 400;
--awx-font-medium: 500;
--awx-font-semibold: 600;
--awx-font-bold: 700;
```

---

## Spacing

### Scale (px)
| Token | Value |
|-------|-------|
| `--awx-space-1` | 4px |
| `--awx-space-2` | 8px |
| `--awx-space-3` | 12px |
| `--awx-space-4` | 16px |
| `--awx-space-6` | 24px |
| `--awx-space-8` | 32px |
| `--awx-space-12` | 48px |
| `--awx-space-16` | 64px |

### Common Uses
```css
/* Button padding */
padding: var(--awx-space-3) var(--awx-space-6);

/* Card padding */
padding: var(--awx-space-6);

/* Form gap */
gap: var(--awx-space-4);

/* Section spacing */
padding: var(--awx-space-24) 0;
```

---

## Border Radius

```css
--awx-radius-sm: 4px;    /* Tags, badges */
--awx-radius-md: 8px;    /* Inputs */
--awx-radius-lg: 12px;   /* Buttons, cards */
--awx-radius-xl: 16px;   /* Large cards */
--awx-radius-full: 9999px; /* Pills */
```

---

## Shadows

```css
--awx-shadow-sm;     /* Subtle elevation */
--awx-shadow-md;     /* Cards */
--awx-shadow-lg;     /* Dropdowns */
--awx-shadow-xl;     /* Modals */
--awx-shadow-orange; /* CTA buttons on hover */
```

---

## Gradients

```css
/* Business Accounts */
background: linear-gradient(135deg, #FF6B40 0%, #FF6B5B 100%);

/* Spend */
background: linear-gradient(135deg, #FF5082 0%, #FF7A9E 100%);

/* Payments */
background: linear-gradient(135deg, #2B7FFF 0%, #52A3FF 100%);

/* Platform */
background: linear-gradient(135deg, #A855F7 0%, #FF5082 100%);
```

---

## Quick Component Snippets

### Primary Button
```css
.btn-primary {
  padding: 12px 24px;
  font-weight: 500;
  color: white;
  background: var(--awx-orange-500);
  border: none;
  border-radius: 12px;
  cursor: pointer;
}
.btn-primary:hover {
  background: var(--awx-orange-600);
  box-shadow: var(--awx-shadow-orange);
}
```

### Input Field
```css
.input {
  padding: 12px 16px;
  border: 1px solid var(--awx-gray-200);
  border-radius: 12px;
}
.input:focus {
  border-color: var(--awx-orange-500);
  box-shadow: 0 0 0 3px rgba(255, 107, 64, 0.15);
}
```

### Card
```css
.card {
  padding: 24px;
  background: white;
  border: 1px solid var(--awx-gray-200);
  border-radius: 16px;
}
```

---

## Tailwind Classes

### Colors
```
text-awx-orange-500
bg-awx-orange-500
border-awx-orange-500
```

### Product Themes
```
bg-awx-gradient-business
bg-awx-gradient-spend
bg-awx-gradient-payments
bg-awx-gradient-platform
```

### Shadows
```
shadow-awx-md
shadow-awx-lg
shadow-awx-orange
```

---

## Content Style

| Do | Don't |
|----|-------|
| eCommerce | e-commerce |
| fintech | FinTech |
| Cashback | cash back |
| WebApp | Web App |
| US$50 | $50 USD |
| 21 July 2025 | 21st July, 2025 |
| 15% | 15 percent |
| Use Oxford commas | Skip serial comma |
| Sentence case headings | Title Case Headings |
