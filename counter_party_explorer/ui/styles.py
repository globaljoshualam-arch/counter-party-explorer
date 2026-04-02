"""Airwallex design system styles for Streamlit."""

# Country to emoji flag mapping
FLAGS = {
    "AU": "🇦🇺", "Australia": "🇦🇺",
    "CN": "🇨🇳", "China": "🇨🇳",
    "HK": "🇭🇰", "Hong Kong": "🇭🇰",
    "ID": "🇮🇩", "Indonesia": "🇮🇩",
    "IN": "🇮🇳", "India": "🇮🇳",
    "JP": "🇯🇵", "Japan": "🇯🇵",
    "MY": "🇲🇾", "Malaysia": "🇲🇾",
    "NZ": "🇳🇿", "New Zealand": "🇳🇿",
    "PH": "🇵🇭", "Philippines": "🇵🇭",
    "SG": "🇸🇬", "Singapore": "🇸🇬",
    "TH": "🇹🇭", "Thailand": "🇹🇭",
    "VN": "🇻🇳", "Vietnam": "🇻🇳",
    "GB": "🇬🇧", "United Kingdom": "🇬🇧", "UK": "🇬🇧",
    "US": "🇺🇸", "United States": "🇺🇸", "USA": "🇺🇸",
    "CA": "🇨🇦", "Canada": "🇨🇦",
    "DE": "🇩🇪", "Germany": "🇩🇪",
    "FR": "🇫🇷", "France": "🇫🇷",
    "KR": "🇰🇷", "South Korea": "🇰🇷",
    "SE": "🇸🇪", "Sweden": "🇸🇪",
    "AE": "🇦🇪", "UAE": "🇦🇪",
    "EU": "🇪🇺",
}


def get_flag(country) -> str:
    """Get emoji flag for country code or name."""
    if not country or not isinstance(country, str):
        return "🌍"
    return FLAGS.get(country, FLAGS.get(country.upper(), "🌍"))


# Airwallex logo (black version, inverted to white via CSS for dark backgrounds)
AIRWALLEX_LOGO_URL = "https://images.ctfassets.net/sxag7u4cz1re/4JT4j5mM4qMIBdchA0NtuV/6182b7df2437b3b75b7b6a6d9de18d73/Airwallex_Logo_-_Black.png"

# Complete Airwallex dark theme CSS
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Airwallex logo - top right */
.awx-logo-container {
    position: fixed;
    top: 16px;
    right: 24px;
    z-index: 9999;
}

.awx-logo-container img {
    height: 28px;
    width: auto;
    opacity: 0.9;
    transition: opacity 200ms ease-out;
    /* Convert black logo to Airwallex orange (#FF6B40) */
    filter: invert(52%) sepia(93%) saturate(1352%) hue-rotate(343deg) brightness(101%) contrast(101%);
}

.awx-logo-container img:hover {
    opacity: 1;
}

:root {
    --awx-orange-50: #FFF7F5;
    --awx-orange-100: #FFEBE5;
    --awx-orange-200: #FFD4C7;
    --awx-orange-400: #FF8A66;
    --awx-orange-500: #FF6B40;
    --awx-orange-600: #F54D1F;
    --awx-payments-500: #2B7FFF;
    --awx-success-500: #22C55E;
    --awx-success-400: #4ADE80;
    --awx-warning-500: #F59E0B;
    --awx-error-500: #EF4444;
    --awx-gray-50: #FAFAFA;
    --awx-gray-100: #F5F5F5;
    --awx-gray-200: #E5E5E5;
    --awx-gray-300: #D4D4D4;
    --awx-gray-400: #A3A3A3;
    --awx-gray-500: #737373;
    --awx-gray-600: #525252;
    --awx-gray-700: #404040;
    --awx-gray-800: #262626;
    --awx-gray-900: #171717;
    --awx-gray-950: #0A0A0A;
}

/* Global font override */
html, body, [class*="css"] {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* Dark background */
.stApp, [data-testid="stAppViewContainer"], .main .block-container {
    background-color: var(--awx-gray-950) !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: var(--awx-gray-900) !important;
    border-right: 1px solid var(--awx-gray-800) !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: var(--awx-gray-100);
}

[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: var(--awx-gray-400) !important;
    text-align: left !important;
    padding: 12px 14px !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    width: 100% !important;
    justify-content: flex-start !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--awx-gray-800) !important;
    color: var(--awx-gray-100) !important;
}

/* Headers */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--awx-gray-50) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}

h1 { font-size: 28px !important; }
h2 { font-size: 22px !important; }
h3 { font-size: 18px !important; }

/* Text - improved readability */
p, span, label, .stMarkdown, .stMarkdown p, .stMarkdown span {
    color: var(--awx-gray-100) !important;
}

/* Make strong/bold text even brighter */
strong, b, .stMarkdown strong, .stMarkdown b {
    color: var(--awx-gray-50) !important;
    font-weight: 600 !important;
}

/* Captions should be slightly dimmer but still readable */
.stCaption, [data-testid="stCaptionContainer"], small {
    color: var(--awx-gray-400) !important;
}

/* Code blocks - high contrast */
code, .stCode, pre {
    background: var(--awx-gray-800) !important;
    color: var(--awx-orange-400) !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
}

/* Info boxes - better contrast */
[data-testid="stAlert"] p, .stAlert p {
    color: var(--awx-gray-100) !important;
}

/* Dividers */
hr, [data-testid="stHorizontalRule"] {
    border-color: var(--awx-gray-700) !important;
    opacity: 0.5 !important;
}

/* Metrics - stat cards */
[data-testid="stMetric"] {
    background: var(--awx-gray-900) !important;
    border: 1px solid var(--awx-gray-800) !important;
    border-radius: 14px !important;
    padding: 22px !important;
}

[data-testid="stMetric"] label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--awx-gray-500) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.03em !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 32px !important;
    font-weight: 600 !important;
    color: var(--awx-gray-50) !important;
}

[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Buttons */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    transition: all 150ms !important;
}

.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background: var(--awx-orange-500) !important;
    color: white !important;
    border: none !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
    background: var(--awx-orange-600) !important;
    box-shadow: 0 10px 40px -10px rgba(255, 107, 64, 0.4) !important;
}

.stButton > button[kind="secondary"],
.stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]) {
    background: var(--awx-gray-800) !important;
    color: var(--awx-gray-300) !important;
    border: 1px solid var(--awx-gray-700) !important;
}

.stButton > button[kind="secondary"]:hover,
.stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]):hover {
    background: var(--awx-gray-700) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--awx-gray-900) !important;
    border: 1px solid var(--awx-gray-700) !important;
    border-radius: 10px !important;
    color: var(--awx-gray-100) !important;
    font-size: 15px !important;
    padding: 14px 16px !important;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div:focus-within {
    border-color: var(--awx-orange-500) !important;
    box-shadow: 0 0 0 3px rgba(255, 107, 64, 0.15) !important;
}

.stTextInput > div > div > input::placeholder {
    color: var(--awx-gray-500) !important;
}

/* Selectbox dropdown */
[data-baseweb="select"] {
    background: var(--awx-gray-900) !important;
}

[data-baseweb="popover"] {
    background: var(--awx-gray-800) !important;
    border: 1px solid var(--awx-gray-700) !important;
}

[data-baseweb="menu"] {
    background: var(--awx-gray-800) !important;
}

[role="option"] {
    background: transparent !important;
    color: var(--awx-gray-200) !important;
}

[role="option"]:hover {
    background: var(--awx-gray-700) !important;
}

/* Dividers */
hr {
    border-color: var(--awx-gray-800) !important;
    margin: 24px 0 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--awx-gray-900) !important;
    border: 2px dashed var(--awx-gray-700) !important;
    border-radius: 14px !important;
    padding: 24px !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--awx-orange-500) !important;
}

/* File uploader internal elements - dark theme */
[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] div,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] label {
    background: transparent !important;
    color: var(--awx-gray-100) !important;
}

/* File uploader button (Browse files) */
[data-testid="stFileUploader"] button,
[data-testid="stFileUploaderDropzone"] button {
    background: var(--awx-gray-800) !important;
    color: var(--awx-gray-100) !important;
    border: 1px solid var(--awx-gray-600) !important;
}

[data-testid="stFileUploader"] button:hover {
    background: var(--awx-gray-700) !important;
    color: white !important;
}

/* File uploader dropzone */
[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploaderDropzoneInstructions"] {
    background: var(--awx-gray-900) !important;
    color: var(--awx-gray-300) !important;
}

/* Uploaded file info */
[data-testid="stFileUploaderFile"] {
    background: var(--awx-gray-800) !important;
    border: 1px solid var(--awx-gray-700) !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploaderFile"] span,
[data-testid="stFileUploaderFile"] div {
    color: var(--awx-gray-100) !important;
}

/* Delete button on uploaded files */
[data-testid="stFileUploaderFile"] button {
    background: var(--awx-gray-700) !important;
    color: var(--awx-gray-200) !important;
}

/* Any remaining white backgrounds - force dark */
section[data-testid="stFileUploader"] > div {
    background: var(--awx-gray-900) !important;
}

/* Base web components (dropdowns, etc) */
[data-baseweb="base-input"],
[data-baseweb="input"],
[data-baseweb="textarea"] {
    background: var(--awx-gray-900) !important;
    color: var(--awx-gray-100) !important;
}

/* Progress bars */
[data-testid="stProgress"] > div {
    background: var(--awx-gray-800) !important;
}

[data-testid="stProgress"] > div > div {
    background: var(--awx-orange-500) !important;
}

/* Tooltips */
[data-testid="stTooltipContent"] {
    background: var(--awx-gray-800) !important;
    color: var(--awx-gray-100) !important;
    border: 1px solid var(--awx-gray-700) !important;
}

/* Modal/Dialog backgrounds */
[data-testid="stModal"],
[role="dialog"] {
    background: var(--awx-gray-900) !important;
}

/* Any element with white/light background - override */
.st-emotion-cache-1v0mbdj,
.st-emotion-cache-16idsys,
.st-emotion-cache-1wbqy5l {
    background: var(--awx-gray-900) !important;
    color: var(--awx-gray-100) !important;
}

/* Alerts / Info boxes */
.stAlert, [data-testid="stAlert"] {
    background: var(--awx-gray-900) !important;
    border: 1px solid var(--awx-gray-800) !important;
    border-radius: 12px !important;
    color: var(--awx-gray-200) !important;
}

[data-testid="stAlert"][data-baseweb="notification"][kind="positive"],
.stSuccess {
    background: rgba(34, 197, 94, 0.1) !important;
    border-color: rgba(34, 197, 94, 0.3) !important;
}

[data-testid="stAlert"][data-baseweb="notification"][kind="info"],
.stInfo {
    background: rgba(43, 127, 255, 0.1) !important;
    border-color: rgba(43, 127, 255, 0.3) !important;
}

[data-testid="stAlert"][data-baseweb="notification"][kind="warning"],
.stWarning {
    background: rgba(245, 158, 11, 0.1) !important;
    border-color: rgba(245, 158, 11, 0.3) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--awx-gray-900) !important;
    border: 1px solid var(--awx-gray-800) !important;
    border-radius: 12px !important;
    color: var(--awx-gray-100) !important;
}

/* Captions */
.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--awx-gray-500) !important;
    font-size: 13px !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header {
    visibility: hidden !important;
}

/* IMPORTANT: Prevent sidebar from being hidden */
/* Hide the collapse/expand button */
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Ensure sidebar is always visible */
[data-testid="stSidebar"] {
    transform: none !important;
    position: relative !important;
    min-width: 260px !important;
}

/* Hide the X close button in sidebar */
[data-testid="stSidebar"] button[kind="header"] {
    display: none !important;
}

/* Ensure sidebar content area doesn't collapse */
[data-testid="stSidebarContent"] {
    display: block !important;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--awx-gray-900);
}

::-webkit-scrollbar-thumb {
    background: var(--awx-gray-700);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--awx-gray-600);
}
</style>
"""


def render_logo() -> str:
    """Return HTML for Airwallex logo in top right corner."""
    return f'''<div class="awx-logo-container">
        <img src="{AIRWALLEX_LOGO_URL}" alt="Airwallex" />
    </div>'''


def score_badge(score: int) -> str:
    """Return HTML for score badge with color based on value."""
    if score >= 80:
        bg_color = "#22C55E"  # green
    elif score >= 60:
        bg_color = "#F59E0B"  # amber
    else:
        bg_color = "#404040"  # gray

    return f'''<div style="
        background: {bg_color};
        color: white;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        font-size: 15px;
        padding: 6px 10px;
        border-radius: 8px;
        display: inline-block;
        min-width: 42px;
        text-align: center;
    ">{score}</div>'''


def type_badges(receives: bool, pays: bool) -> str:
    """Return HTML for receives/pays type badges."""
    badges = []
    if receives:
        badges.append('''<span style="
            background: rgba(34, 197, 94, 0.15);
            color: #4ADE80;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            padding: 5px 10px;
            border-radius: 6px;
        ">Recv</span>''')
    if pays:
        badges.append('''<span style="
            background: rgba(43, 127, 255, 0.15);
            color: #60A5FA;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            padding: 5px 10px;
            border-radius: 6px;
        ">Pay</span>''')
    return ' '.join(badges) if badges else '—'


def region_badge(country) -> str:
    """Return HTML for region badge with flag."""
    if not country or not isinstance(country, str):
        return '<span style="color: #737373;">—</span>'
    flag = get_flag(country)
    return f'''<span style="
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 13px;
        font-weight: 500;
        color: #FF8A66;
        background: rgba(255, 107, 64, 0.1);
        padding: 3px 10px;
        border-radius: 6px;
    ">{flag} {country}</span>'''


def currency_badges(currencies: list) -> str:
    """Return HTML for currency badges."""
    if not currencies:
        return '—'
    badges = []
    for ccy in currencies[:3]:
        badges.append(f'''<span style="
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 500;
            padding: 4px 8px;
            background: #262626;
            color: #D4D4D4;
            border-radius: 5px;
        ">{ccy}</span>''')
    if len(currencies) > 3:
        badges.append(f'''<span style="
            font-size: 12px;
            color: #737373;
        ">+{len(currencies) - 3}</span>''')
    return ' '.join(badges)


def network_bar(count: int, max_count: int = 5) -> str:
    """Return HTML for network count with visual bar."""
    pct = min(100, (count / max_count) * 100)
    return f'''<div style="display: flex; align-items: center; gap: 10px;">
        <span style="
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            font-size: 15px;
            color: #E5E5E5;
            min-width: 24px;
        ">{count}</span>
        <div style="
            width: 50px;
            height: 6px;
            background: #404040;
            border-radius: 3px;
            overflow: hidden;
        ">
            <div style="
                width: {pct}%;
                height: 100%;
                background: #FF6B40;
                border-radius: 3px;
            "></div>
        </div>
    </div>'''


def volume_cell(amount: float, txn_count: int = None) -> str:
    """Return HTML for volume display with optional transaction count."""
    if not amount:
        return '—'
    if amount >= 1_000_000_000:
        formatted = f"${amount / 1_000_000_000:.1f}B"
    elif amount >= 1_000_000:
        formatted = f"${amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        formatted = f"${amount / 1_000:.0f}K"
    else:
        formatted = f"${amount:.0f}"

    html = f'''<div style="
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        font-size: 15px;
        color: #F5F5F5;
    ">{formatted}</div>'''

    if txn_count:
        html += f'''<div style="
            font-size: 12px;
            color: #737373;
            margin-top: 2px;
        ">{txn_count} txn/mo</div>'''

    return html
