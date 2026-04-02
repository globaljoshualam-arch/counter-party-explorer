"""Airwallex design system styles and components."""

# Airwallex color palette
COLORS = {
    "orange_500": "#FF6B40",
    "orange_400": "#FF8461",
    "orange_600": "#E65539",
    "gray_50": "#F9FAFB",
    "gray_100": "#F3F4F6",
    "gray_200": "#E5E7EB",
    "gray_300": "#D1D5DB",
    "gray_400": "#9CA3AF",
    "gray_500": "#6B7280",
    "gray_600": "#4B5563",
    "gray_700": "#374151",
    "gray_800": "#1F2937",
    "gray_900": "#111827",
    "background": "#0A0A0A",
    "surface": "#1A1A1A",
    "border": "#2A2A2A",
}

# Country to emoji flag mapping
FLAGS = {
    "AU": "🇦🇺",
    "CN": "🇨🇳",
    "HK": "🇭🇰",
    "ID": "🇮🇩",
    "IN": "🇮🇳",
    "JP": "🇯🇵",
    "MY": "🇲🇾",
    "NZ": "🇳🇿",
    "PH": "🇵🇭",
    "SG": "🇸🇬",
    "TH": "🇹🇭",
    "VN": "🇻🇳",
    "GB": "🇬🇧",
    "US": "🇺🇸",
    "CA": "🇨🇦",
    "EU": "🇪🇺",
    "AE": "🇦🇪",
}


def get_flag(country: str) -> str:
    """Get emoji flag for country code."""
    return FLAGS.get(country, "🌍")


# Global CSS for dark theme
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --orange-500: #FF6B40;
    --orange-400: #FF8461;
    --orange-600: #E65539;
    --background: #0A0A0A;
    --surface: #1A1A1A;
    --border: #2A2A2A;
    --text-primary: #F9FAFB;
    --text-secondary: #9CA3AF;
}

/* Global font */
* {
    font-family: 'DM Sans', sans-serif !important;
}

/* Monospace for numbers */
.mono {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Dark theme */
.stApp {
    background-color: var(--background);
    color: var(--text-primary);
}

/* Cards and containers */
.element-container, .stMarkdown {
    background-color: var(--surface);
}

/* Inputs and selectboxes */
.stSelectbox, .stTextInput, .stNumberInput {
    background-color: var(--surface);
    border-color: var(--border);
}

/* Dataframe styling */
.dataframe {
    background-color: var(--surface) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

.dataframe th {
    background-color: var(--border) !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

.dataframe td {
    border-color: var(--border) !important;
}

/* Numbers in tables */
.dataframe td:has(.mono), .dataframe td > div > span {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    margin: 2px;
}

.score-badge {
    background: linear-gradient(135deg, var(--orange-500), var(--orange-600));
    color: white;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 500;
    padding: 6px 14px;
    border-radius: 8px;
}

.type-badge {
    background-color: var(--surface);
    border: 1px solid var(--border);
    color: var(--text-secondary);
}

.region-badge {
    background-color: rgba(255, 107, 64, 0.1);
    border: 1px solid rgba(255, 107, 64, 0.3);
    color: var(--orange-400);
    font-size: 14px;
    padding: 6px 12px;
}

/* Buttons */
.stButton > button {
    background-color: var(--orange-500);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    transition: background-color 0.2s;
}

.stButton > button:hover {
    background-color: var(--orange-600);
}

/* Metrics */
.stMetric {
    background-color: var(--surface);
    padding: 16px;
    border-radius: 8px;
    border: 1px solid var(--border);
}

.stMetric label {
    color: var(--text-secondary) !important;
    font-size: 14px !important;
}

.stMetric [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    color: var(--text-primary) !important;
}
</style>
"""


def score_badge(score: float) -> str:
    """Return HTML for score badge."""
    return f'<span class="badge score-badge">{score:.1f}</span>'


def type_badges(receives: str, pays: str) -> str:
    """Return HTML for type badges (receives/pays currencies)."""
    receives_html = f'<span class="badge type-badge">▼ {receives}</span>'
    pays_html = f'<span class="badge type-badge">▲ {pays}</span>'
    return f"{receives_html} {pays_html}"


def region_badge(country: str) -> str:
    """Return HTML for region badge with flag."""
    flag = get_flag(country)
    return f'<span class="badge region-badge">{flag} {country}</span>'
