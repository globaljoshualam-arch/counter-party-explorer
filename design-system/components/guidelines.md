# Airwallex Component Guidelines

> Design patterns and component specifications for Airwallex interfaces.

---

## Table of Contents

1. [Buttons](#buttons)
2. [Forms](#forms)
3. [Cards](#cards)
4. [Navigation](#navigation)
5. [Data Display](#data-display)
6. [Feedback](#feedback)
7. [Icons](#icons)
8. [Logo Usage](#logo-usage)

---

## Buttons

### Primary Button

The primary action button uses the Airwallex orange. Use for main CTAs.

```html
<button class="awx-btn-primary">
  Get started
</button>
```

```css
.awx-btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--awx-space-2);
  padding: var(--awx-space-3) var(--awx-space-6);
  font-family: var(--awx-font-sans);
  font-size: var(--awx-text-sm);
  font-weight: var(--awx-font-medium);
  color: var(--awx-white);
  background: var(--awx-orange-500);
  border: none;
  border-radius: var(--awx-radius-lg);
  cursor: pointer;
  transition: all var(--awx-duration-200) var(--awx-ease-out);
}

.awx-btn-primary:hover {
  background: var(--awx-orange-600);
  box-shadow: var(--awx-shadow-orange);
  transform: translateY(-1px);
}

.awx-btn-primary:active {
  background: var(--awx-orange-700);
  transform: translateY(0);
}

.awx-btn-primary:focus-visible {
  outline: 2px solid var(--awx-orange-500);
  outline-offset: 2px;
}

.awx-btn-primary:disabled {
  background: var(--awx-gray-300);
  color: var(--awx-gray-500);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
```

### Secondary Button

For secondary actions. Uses outline style.

```css
.awx-btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--awx-space-2);
  padding: var(--awx-space-3) var(--awx-space-6);
  font-family: var(--awx-font-sans);
  font-size: var(--awx-text-sm);
  font-weight: var(--awx-font-medium);
  color: var(--awx-gray-900);
  background: transparent;
  border: 1px solid var(--awx-gray-300);
  border-radius: var(--awx-radius-lg);
  cursor: pointer;
  transition: all var(--awx-duration-200) var(--awx-ease-out);
}

.awx-btn-secondary:hover {
  background: var(--awx-gray-50);
  border-color: var(--awx-gray-400);
}
```

### Ghost Button

For tertiary actions or text-like buttons.

```css
.awx-btn-ghost {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--awx-space-2);
  padding: var(--awx-space-2) var(--awx-space-4);
  font-family: var(--awx-font-sans);
  font-size: var(--awx-text-sm);
  font-weight: var(--awx-font-medium);
  color: var(--awx-orange-600);
  background: transparent;
  border: none;
  border-radius: var(--awx-radius-md);
  cursor: pointer;
  transition: all var(--awx-duration-150) var(--awx-ease-out);
}

.awx-btn-ghost:hover {
  background: var(--awx-orange-50);
}
```

### Product-Specific Buttons

Use product category colors for product-specific CTAs:

```css
/* Spend Product */
.awx-btn-spend {
  background: var(--awx-spend-500);
}
.awx-btn-spend:hover {
  background: var(--awx-spend-600);
}

/* Payments Product */
.awx-btn-payments {
  background: var(--awx-payments-500);
}
.awx-btn-payments:hover {
  background: var(--awx-payments-600);
}

/* Platform APIs Product */
.awx-btn-platform {
  background: var(--awx-gradient-platform);
}
```

### Button Sizes

```css
.awx-btn-sm {
  padding: var(--awx-space-2) var(--awx-space-4);
  font-size: var(--awx-text-xs);
}

.awx-btn-lg {
  padding: var(--awx-space-4) var(--awx-space-8);
  font-size: var(--awx-text-base);
}
```

---

## Forms

### Text Input

```css
.awx-input {
  width: 100%;
  padding: var(--awx-space-3) var(--awx-space-4);
  font-family: var(--awx-font-sans);
  font-size: var(--awx-text-base);
  color: var(--awx-text-primary);
  background: var(--awx-white);
  border: 1px solid var(--awx-border-default);
  border-radius: var(--awx-radius-lg);
  transition: all var(--awx-duration-150) var(--awx-ease-out);
}

.awx-input::placeholder {
  color: var(--awx-text-tertiary);
}

.awx-input:hover {
  border-color: var(--awx-gray-400);
}

.awx-input:focus {
  outline: none;
  border-color: var(--awx-orange-500);
  box-shadow: 0 0 0 3px rgba(255, 107, 64, 0.15);
}

.awx-input:disabled {
  background: var(--awx-gray-100);
  color: var(--awx-text-disabled);
  cursor: not-allowed;
}

.awx-input.error {
  border-color: var(--awx-error-500);
}

.awx-input.error:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15);
}
```

### Form Label

```css
.awx-label {
  display: block;
  margin-bottom: var(--awx-space-2);
  font-family: var(--awx-font-sans);
  font-size: var(--awx-text-sm);
  font-weight: var(--awx-font-medium);
  color: var(--awx-text-primary);
}

.awx-label-required::after {
  content: ' *';
  color: var(--awx-error-500);
}
```

### Helper Text

```css
.awx-helper-text {
  margin-top: var(--awx-space-1);
  font-size: var(--awx-text-sm);
  color: var(--awx-text-secondary);
}

.awx-helper-text.error {
  color: var(--awx-error-600);
}
```

### Select

```css
.awx-select {
  appearance: none;
  width: 100%;
  padding: var(--awx-space-3) var(--awx-space-10) var(--awx-space-3) var(--awx-space-4);
  font-family: var(--awx-font-sans);
  font-size: var(--awx-text-base);
  color: var(--awx-text-primary);
  background: var(--awx-white) url("data:image/svg+xml,...") no-repeat right var(--awx-space-3) center;
  background-size: 16px;
  border: 1px solid var(--awx-border-default);
  border-radius: var(--awx-radius-lg);
  cursor: pointer;
}
```

---

## Cards

### Basic Card

```css
.awx-card {
  background: var(--awx-bg-primary);
  border: 1px solid var(--awx-border-default);
  border-radius: var(--awx-radius-xl);
  padding: var(--awx-space-6);
  transition: all var(--awx-duration-200) var(--awx-ease-out);
}

.awx-card:hover {
  box-shadow: var(--awx-shadow-md);
}
```

### Interactive Card

```css
.awx-card-interactive {
  background: var(--awx-bg-primary);
  border: 1px solid var(--awx-border-default);
  border-radius: var(--awx-radius-xl);
  padding: var(--awx-space-6);
  cursor: pointer;
  transition: all var(--awx-duration-200) var(--awx-ease-out);
}

.awx-card-interactive:hover {
  border-color: var(--awx-orange-300);
  box-shadow: var(--awx-shadow-lg);
  transform: translateY(-2px);
}

.awx-card-interactive:active {
  transform: translateY(0);
}
```

### Product Card

For product category sections:

```css
.awx-card-product {
  background: var(--awx-bg-primary);
  border-radius: var(--awx-radius-2xl);
  padding: var(--awx-space-8);
  overflow: hidden;
  position: relative;
}

.awx-card-product::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--awx-product-gradient);
}

/* Apply product theme class to card */
.awx-card-product.awx-theme-business-accounts::before {
  background: var(--awx-gradient-business);
}

.awx-card-product.awx-theme-spend::before {
  background: var(--awx-gradient-spend);
}

.awx-card-product.awx-theme-payments::before {
  background: var(--awx-gradient-payments);
}

.awx-card-product.awx-theme-platform::before {
  background: var(--awx-gradient-platform);
}
```

---

## Navigation

### Header Navigation

```css
.awx-nav {
  display: flex;
  align-items: center;
  gap: var(--awx-space-8);
}

.awx-nav-link {
  font-family: var(--awx-font-sans);
  font-size: var(--awx-text-sm);
  font-weight: var(--awx-font-medium);
  color: var(--awx-text-secondary);
  text-decoration: none;
  padding: var(--awx-space-2) 0;
  position: relative;
  transition: color var(--awx-duration-150) var(--awx-ease-out);
}

.awx-nav-link:hover {
  color: var(--awx-text-primary);
}

.awx-nav-link.active {
  color: var(--awx-orange-600);
}

.awx-nav-link.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--awx-orange-500);
  border-radius: var(--awx-radius-full);
}
```

### Tab Navigation

```css
.awx-tabs {
  display: flex;
  gap: var(--awx-space-1);
  background: var(--awx-gray-100);
  padding: var(--awx-space-1);
  border-radius: var(--awx-radius-lg);
}

.awx-tab {
  flex: 1;
  padding: var(--awx-space-2) var(--awx-space-4);
  font-family: var(--awx-font-sans);
  font-size: var(--awx-text-sm);
  font-weight: var(--awx-font-medium);
  color: var(--awx-text-secondary);
  background: transparent;
  border: none;
  border-radius: var(--awx-radius-md);
  cursor: pointer;
  transition: all var(--awx-duration-150) var(--awx-ease-out);
}

.awx-tab:hover {
  color: var(--awx-text-primary);
}

.awx-tab.active {
  color: var(--awx-text-primary);
  background: var(--awx-white);
  box-shadow: var(--awx-shadow-sm);
}
```

---

## Data Display

### Badge

```css
.awx-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--awx-space-1);
  padding: var(--awx-space-1) var(--awx-space-2);
  font-family: var(--awx-font-sans);
  font-size: var(--awx-text-xs);
  font-weight: var(--awx-font-medium);
  border-radius: var(--awx-radius-full);
}

.awx-badge-orange {
  color: var(--awx-orange-700);
  background: var(--awx-orange-100);
}

.awx-badge-success {
  color: var(--awx-success-700);
  background: var(--awx-success-100);
}

.awx-badge-warning {
  color: var(--awx-warning-700);
  background: var(--awx-warning-100);
}

.awx-badge-error {
  color: var(--awx-error-700);
  background: var(--awx-error-100);
}

.awx-badge-gray {
  color: var(--awx-gray-700);
  background: var(--awx-gray-100);
}
```

### Table

```css
.awx-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--awx-font-sans);
}

.awx-table th {
  padding: var(--awx-space-3) var(--awx-space-4);
  font-size: var(--awx-text-xs);
  font-weight: var(--awx-font-semibold);
  color: var(--awx-text-secondary);
  text-align: left;
  text-transform: uppercase;
  letter-spacing: var(--awx-tracking-wider);
  background: var(--awx-gray-50);
  border-bottom: 1px solid var(--awx-border-default);
}

.awx-table td {
  padding: var(--awx-space-4);
  font-size: var(--awx-text-sm);
  color: var(--awx-text-primary);
  border-bottom: 1px solid var(--awx-border-subtle);
}

.awx-table tr:hover td {
  background: var(--awx-gray-50);
}
```

### Stat/Metric Card

```css
.awx-stat {
  display: flex;
  flex-direction: column;
  gap: var(--awx-space-1);
}

.awx-stat-label {
  font-size: var(--awx-text-sm);
  font-weight: var(--awx-font-medium);
  color: var(--awx-text-secondary);
}

.awx-stat-value {
  font-size: var(--awx-text-3xl);
  font-weight: var(--awx-font-bold);
  color: var(--awx-text-primary);
  letter-spacing: var(--awx-tracking-tight);
}

.awx-stat-change {
  display: inline-flex;
  align-items: center;
  gap: var(--awx-space-1);
  font-size: var(--awx-text-sm);
  font-weight: var(--awx-font-medium);
}

.awx-stat-change.positive {
  color: var(--awx-success-600);
}

.awx-stat-change.negative {
  color: var(--awx-error-600);
}
```

---

## Feedback

### Alert

```css
.awx-alert {
  display: flex;
  gap: var(--awx-space-3);
  padding: var(--awx-space-4);
  border-radius: var(--awx-radius-lg);
  font-family: var(--awx-font-sans);
  font-size: var(--awx-text-sm);
}

.awx-alert-info {
  color: var(--awx-info-700);
  background: var(--awx-info-50);
  border: 1px solid var(--awx-info-200);
}

.awx-alert-success {
  color: var(--awx-success-700);
  background: var(--awx-success-50);
  border: 1px solid var(--awx-success-200);
}

.awx-alert-warning {
  color: var(--awx-warning-700);
  background: var(--awx-warning-50);
  border: 1px solid var(--awx-warning-200);
}

.awx-alert-error {
  color: var(--awx-error-700);
  background: var(--awx-error-50);
  border: 1px solid var(--awx-error-200);
}
```

### Toast Notification

```css
.awx-toast {
  display: flex;
  align-items: center;
  gap: var(--awx-space-3);
  padding: var(--awx-space-4) var(--awx-space-5);
  background: var(--awx-gray-900);
  color: var(--awx-white);
  border-radius: var(--awx-radius-lg);
  box-shadow: var(--awx-shadow-xl);
  font-family: var(--awx-font-sans);
  font-size: var(--awx-text-sm);
  animation: awx-slide-in-right var(--awx-duration-300) var(--awx-ease-out);
}
```

### Loading Spinner

```css
.awx-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--awx-gray-200);
  border-top-color: var(--awx-orange-500);
  border-radius: var(--awx-radius-full);
  animation: awx-spin 0.8s linear infinite;
}

@keyframes awx-spin {
  to {
    transform: rotate(360deg);
  }
}

.awx-spinner-sm {
  width: 16px;
  height: 16px;
}

.awx-spinner-lg {
  width: 32px;
  height: 32px;
  border-width: 3px;
}
```

---

## Icons

### Icon Guidelines

**Detailed Icons** (for marketing/brand materials):
- Use 4 color variants matching product categories
- Use on light backgrounds: Brand color highlight version
- Use on dark backgrounds: Gray highlight version
- Never mix detailed with simple icons on same page

**Simple Icons** (for UI/functional elements):
- Use white or black only
- 24px default size, 16px for compact UI
- 1.5px stroke weight
- Consistent with product-agnostic contexts

```css
/* Icon sizes */
.awx-icon-sm {
  width: 16px;
  height: 16px;
}

.awx-icon-md {
  width: 24px;
  height: 24px;
}

.awx-icon-lg {
  width: 32px;
  height: 32px;
}

.awx-icon-xl {
  width: 48px;
  height: 48px;
}

/* Icon colors */
.awx-icon-primary {
  color: var(--awx-text-primary);
}

.awx-icon-secondary {
  color: var(--awx-text-secondary);
}

.awx-icon-brand {
  color: var(--awx-orange-500);
}

/* Detailed icon containers */
.awx-icon-detailed {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--awx-space-3);
  background: var(--awx-orange-100);
  border-radius: var(--awx-radius-lg);
}
```

---

## Logo Usage

### Do's

- Use provided logo files (SVG for digital, CMYK for print)
- Maintain clear space around logo (minimum: height of the "A")
- Use high-contrast backgrounds
- Use appropriate color version for background

### Don'ts

- Never crop or display at an angle
- Never alter the logo proportions
- Never add drop shadows or effects
- Never place on low-contrast backgrounds
- Never recreate or modify the logo

### Logo Wrapper

```css
.awx-logo {
  display: inline-flex;
  align-items: center;
}

.awx-logo img,
.awx-logo svg {
  height: 32px;
  width: auto;
}

.awx-logo-sm img,
.awx-logo-sm svg {
  height: 24px;
}

.awx-logo-lg img,
.awx-logo-lg svg {
  height: 48px;
}
```

---

## Accessibility

### Focus States

All interactive elements must have visible focus states:

```css
*:focus-visible {
  outline: 2px solid var(--awx-orange-500);
  outline-offset: 2px;
}
```

### Color Contrast

- Text on white: Use `--awx-gray-900` minimum
- Text on colored backgrounds: Ensure 4.5:1 contrast ratio
- Small text (< 14px): Ensure 7:1 contrast ratio

### Motion Preferences

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Content Guidelines

Based on the Airwallex Editorial Style Guide:

### Writing Style

- **Voice**: Confident, warm, globally-minded
- **Tone**: Inform, Inspire, Educate, Empower
- **Language**: Clear, concise, jargon-free

### Numbers

- Spell out one through nine
- Use numerals for 10+
- Use % symbol: 15%, 80.5%
- Use numerals in tables and lists

### Dates

- Format: 21 July 2025 (day month year)
- US format: July 21 2025 (month day year)
- No ordinals: 21 July, not 21st July

### Currencies

- US$50, A$50, HK$50, S$50, C$50
- GBP: £10.50
- EUR: €10
- Spell out: 100 yuan, 100,000 yen

### Product Names (Title Case)

- Airwallex (one word, capital A)
- Global Accounts
- Corporate Cards
- Bill Pay
- Expense Management

### Terminology

- eCommerce (not e-commerce)
- fintech (not FinTech)
- Cashback (one word)
- WebApp (one word)
- Startup (one word)
- Payment platform (singular)

### Punctuation

- Use Oxford commas
- Sentence case for headings
- Capitalise first word after colon in titles
