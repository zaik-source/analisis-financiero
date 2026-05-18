import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import requests
from textblob import TextBlob
from datetime import datetime
from dateutil.relativedelta import relativedelta
import io
import warnings
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Terminal Financiera",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
#  CUSTOM CSS — Dark terminal aesthetic
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600;700&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0a0e1a;
    color: #c8d6e5;
}
.stApp { background-color: #0a0e1a; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1421 0%, #111827 100%);
    border-right: 1px solid #1e3a5f;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #4fc3f7;
    font-family: 'IBM Plex Mono', monospace;
}

/* Title header */
.terminal-header {
    background: linear-gradient(135deg, #0d1421 0%, #0a1628 50%, #0d1b2e 100%);
    border: 1px solid #1e3a5f;
    border-left: 4px solid #00b4d8;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    border-radius: 4px;
    position: relative;
    overflow: hidden;
}
.terminal-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,180,216,0.02) 2px,
        rgba(0,180,216,0.02) 4px
    );
}
.terminal-header h1 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #00b4d8;
    margin: 0;
    letter-spacing: 2px;
    text-shadow: 0 0 20px rgba(0,180,216,0.4);
}
.terminal-header p {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #4a6fa5;
    margin: 0.3rem 0 0 0;
    letter-spacing: 1px;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #0d1421, #111827);
    border: 1px solid #1e3a5f;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    position: relative;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; width: 3px; height: 100%;
    background: #00b4d8;
    border-radius: 3px 0 0 3px;
}
.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #4a6fa5;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #e2e8f0;
}
.metric-value.positive { color: #00e676; }
.metric-value.negative { color: #ff5252; }
.metric-value.neutral  { color: #ffd740; }
.metric-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #64748b;
    margin-top: 0.2rem;
}

/* Section headers */
.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    color: #00b4d8;
    text-transform: uppercase;
    border-bottom: 1px solid #1e3a5f;
    padding-bottom: 0.5rem;
    margin: 1.5rem 0 1rem 0;
}

/* Sentiment badge */
.sentiment-badge {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 3px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 1px;
}
.sent-positive { background: rgba(0,230,118,0.15); color: #00e676; border: 1px solid #00e676; }
.sent-negative { background: rgba(255,82,82,0.15);  color: #ff5252; border: 1px solid #ff5252; }
.sent-neutral  { background: rgba(255,215,64,0.15); color: #ffd740; border: 1px solid #ffd740; }

/* Trend badge */
.trend-alcista { color: #00e676; font-family:'IBM Plex Mono',monospace; font-weight:700; font-size:1.1rem; }
.trend-bajista { color: #ff5252; font-family:'IBM Plex Mono',monospace; font-weight:700; font-size:1.1rem; }

/* Streamlit overrides */
div[data-testid="stMetric"] {
    background: #0d1421;
    border: 1px solid #1e3a5f;
    border-radius: 6px;
    padding: 1rem;
}
.stButton > button {
    background: linear-gradient(135deg, #00b4d8, #0077b6);
    color: white;
    border: none;
    border-radius: 4px;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    letter-spacing: 1px;
    padding: 0.6rem 2rem;
    transition: all 0.2s;
    width: 100%;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00c4e8, #0087c6);
    box-shadow: 0 0 20px rgba(0,180,216,0.4);
    transform: translateY(-1px);
}
.stTextInput > div > div > input {
    background: #0d1421;
    border: 1px solid #1e3a5f;
    color: #e2e8f0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1rem;
    border-radius: 4px;
}
.stTextInput > div > div > input:focus {
    border-color: #00b4d8;
    box-shadow: 0 0 10px rgba(0,180,216,0.2);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 1px;
    color: #4a6fa5;
}
.stTabs [aria-selected="true"] {
    color: #00b4d8 !important;
    border-bottom: 2px solid #00b4d8 !important;
}
.stAlert {
    background: #0d1421;
    border: 1px solid #1e3a5f;
    border-radius: 4px;
}

/* Score bars */
.score-bar-bg {
    background: #1e3a5f;
    border-radius: 3px;
    height: 8px;
    margin-top: 4px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, #0077b6, #00b4d8);
    transition: width 0.5s ease;
}
.score-row {
    display: flex;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #1a2a3a;
}
.score-name {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #8eacc8;
    width: 130px;
    flex-shrink: 0;
}
.score-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    color: #00b4d8;
    width: 50px;
    text-align: right;
    flex-shrink: 0;
    margin-right: 10px;
}
.score-bar-wrap { flex: 1; }

/* Levels table */
.levels-table { width:100%; border-collapse:collapse; font-family:'IBM Plex Mono',monospace; font-size:0.75rem; }
.levels-table th { color:#4a6fa5; font-weight:400; text-transform:uppercase; letter-spacing:2px; padding:0.4rem 0.6rem; border-bottom:1px solid #1e3a5f; text-align:left; }
.levels-table td { padding:0.4rem 0.6rem; border-bottom:1px solid #0d1421; }
.lvl-soporte    { color:#00e676; }
.lvl-resistencia{ color:#ff5252; }

/* Divider */
.hr-term { border: none; border-top: 1px solid #1e3a5f; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════

NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "f525b346861347859c34dfa92d6ec99a")

DARK = {
    "bg":       "#0a0e1a",
    "panel":    "#0d1421",
    "border":   "#1e3a5f",
    "accent":   "#00b4d8",
    "text":     "#c8d6e5",
    "grid":     "#1e3a5f",
    "green":    "#00e676",
    "red":      "#ff5252",
    "yellow":   "#ffd740",
}

def fig_style(fig, axes_list):
    fig.patch.set_facecolor(DARK["bg"])
    for ax in axes_list:
        ax.set_facecolor(DARK["panel"])
        ax.tick_params(colors=DARK["text"], labelsize=8)
        ax.xaxis.label.set_color(DARK["text"])
        ax.yaxis.label.set_color(DARK["text"])
        ax.title.set_color(DARK["accent"])
        for spine in ax.spines.values():
            spine.set_edgecolor(DARK["border"])
        ax.grid(color=DARK["grid"], alpha=0.3, linewidth=0.5)


@st.cache_data(ttl=300, show_spinner=False)
def cargar_df(ticker, meses=24):
    fecha_fin    = datetime.now()
    fecha_inicio = fecha_fin - relativedelta(months=meses)
    df = yf.download(
        ticker,
        start=fecha_inicio.strftime('%Y-%m-%d'),
        end=fecha_fin.strftime('%Y-%m-%d'),
        progress=False,
        auto_adjust=True,
    )
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

@st.cache_data(ttl=300, show_spinner=False)
def cargar_info(ticker):
    stock = yf.Ticker(ticker)
    return stock.info


def calcular_indicadores(df):
    df = df.copy()
    df['SMA20']      = df['Close'].rolling(20).mean()
    df['SMA50']      = df['Close'].rolling(50).mean()
    df['SMA200']     = df['Close'].rolling(200).mean()
    df['StdDev']     = df['Close'].rolling(20).std()
    df['Upper_Band'] = df['SMA20'] + df['StdDev'] * 2
    df['Lower_Band'] = df['SMA20'] - df['StdDev'] * 2
    delta    = df['Close'].diff()
    up, dn   = delta.clip(lower=0), -1 * delta.clip(upper=0)
    ma_up    = up.ewm(com=13, adjust=False).mean()
    ma_dn    = dn.ewm(com=13, adjust=False).mean()
    df['RSI']         = 100 - (100 / (1 + ma_up / ma_dn))
    ema12             = df['Close'].ewm(span=12, adjust=False).mean()
    ema26             = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD']        = ema12 - ema26
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['Histogram']   = df['MACD'] - df['Signal_Line']
    return df


def calcular_niveles(df):
    niveles = []
    start = max(2, len(df) - 180)
    for i in range(start, len(df) - 2):
        lo = df['Low'].iloc
        hi = df['High'].iloc
        if lo[i] < lo[i-1] and lo[i] < lo[i+1] and lo[i] < lo[i-2] and lo[i] < lo[i+2]:
            niveles.append((float(lo[i]), 'Soporte'))
        elif hi[i] > hi[i-1] and hi[i] > hi[i+1] and hi[i] > hi[i-2] and hi[i] > hi[i+2]:
            niveles.append((float(hi[i]), 'Resistencia'))
    limpios = []
    if niveles:
        niveles.sort()
        dist_min = float(df['Close'].mean()) * 0.015
        curr = niveles[0][0]
        limpios.append(niveles[0])
        for n in niveles[1:]:
            if n[0] - curr > dist_min:
                limpios.append(n)
                curr = n[0]
    return limpios


def calcular_scores(info):
    pm    = info.get('profitMargins',  0) or 0
    pe    = info.get('forwardPE',     25) or 25
    gr    = info.get('revenueGrowth',  0) or 0
    qr    = info.get('quickRatio',     1) or 1
    dy    = info.get('dividendYield',  0) or 0
    return {
        'Crecimiento':   min(10, max(1, gr  * 50)),
        'Valoración':    max(1,  min(10, 40 / pe * 5)),
        'Rentabilidad':  min(10, max(1, pm  * 40)),
        'Salud Deuda':   min(10, max(1, qr  * 5)),
        'Dividendos':    min(10, max(1, dy  * 200)),
    }


@st.cache_data(ttl=600, show_spinner=False)
def obtener_sentimiento(ticker):
    try:
        url = (f'https://newsapi.org/v2/everything?q={ticker}'
               f'&language=en&sortBy=publishedAt&pageSize=8&apiKey={NEWS_API_KEY}')
        res  = requests.get(url, timeout=5).json()
        arts = res.get('articles', [])
        if not arts:
            return 0, 0, []
        scores = []
        titulos = []
        for a in arts[:8]:
            pol = TextBlob(a['title']).sentiment.polarity
            scores.append(pol)
            titulos.append({'title': a['title'], 'score': pol,
                            'url': a.get('url',''), 'source': a.get('source',{}).get('name','')})
        return sum(scores) / len(scores), len(scores), titulos
    except Exception:
        return 0, 0, []


# ══════════════════════════════════════════════════════════════════
#  PLOTS
# ══════════════════════════════════════════════════════════════════

def plot_tecnico(df, ticker, niveles, target_price, low_52, high_52):
    df_p = df.iloc[-120:].copy()
    fig  = plt.figure(figsize=(14, 16), facecolor=DARK["bg"])
    gs   = gridspec.GridSpec(5, 1, figure=fig,
                             height_ratios=[3.0, 0.4, 0.8, 1.0, 0.8],
                             hspace=0.08)
    ax1  = fig.add_subplot(gs[0])
    axB  = fig.add_subplot(gs[1])
    ax2  = fig.add_subplot(gs[2])
    ax3  = fig.add_subplot(gs[3])
    ax4  = fig.add_subplot(gs[4])

    fig_style(fig, [ax1, axB, ax2, ax3, ax4])

    # — Precio principal —
    ax1.plot(df_p.index, df_p['Close'], color=DARK["text"], linewidth=1.5, label='Precio', zorder=5)
    ax1.fill_between(df_p.index, df_p['Lower_Band'], df_p['Upper_Band'],
                     color=DARK["accent"], alpha=0.07, label='Bollinger')
    ax1.plot(df_p.index, df_p['SMA20'],  color='#ffd740', label='SMA 20', linestyle='--', alpha=0.8, linewidth=1)
    ax1.plot(df_p.index, df_p['SMA50'],  color='#4fc3f7', label='SMA 50', alpha=0.8, linewidth=1.2)
    ax1.plot(df_p.index, df_p['SMA200'], color='#ff5252', linewidth=2.0, label='SMA 200')
    for nivel, tipo in niveles:
        ax1.axhline(nivel,
                    color=DARK["green"] if tipo == 'Soporte' else DARK["red"],
                    linestyle=':', alpha=0.5, linewidth=0.8)
    ax1.set_title(f"  {ticker}  —  TERMINAL TÉCNICA", fontsize=13, fontweight='bold',
                  color=DARK["accent"], loc='left', pad=10)
    ax1.legend(loc='upper left', ncol=3, fontsize=8,
               facecolor=DARK["panel"], edgecolor=DARK["border"], labelcolor=DARK["text"])
    ax1.set_xticklabels([])

    # — Bullet chart —
    curr_p = float(df['Close'].iloc[-1])
    axB.set_facecolor(DARK["panel"])
    axB.barh(0, high_52, color='#1e3a5f', height=0.5)
    axB.barh(0, curr_p,  color=DARK["accent"], height=0.25)
    if target_price:
        axB.axvline(target_price, color=DARK["green"], linewidth=3,
                    label=f'Target ${target_price:.2f}')
    axB.axvline(curr_p, color=DARK["text"], linewidth=1.5, linestyle='--')
    axB.set_yticks([])
    axB.set_xlim(low_52 * 0.95, max(high_52, target_price or 0) * 1.05)
    axB.set_xticklabels([])
    axB.set_title("  Rango 52 semanas  ·  Precio actual  ·  Target analistas",
                  fontsize=8, color='#4a6fa5', loc='left', pad=4)
    for sp in axB.spines.values():
        sp.set_edgecolor(DARK["border"])

    # — RSI —
    ax2.plot(df_p.index, df_p['RSI'], color='#ce93d8', linewidth=1.2)
    ax2.axhline(70, color=DARK["red"],   linestyle='--', alpha=0.7, linewidth=0.8)
    ax2.axhline(30, color=DARK["green"], linestyle='--', alpha=0.7, linewidth=0.8)
    ax2.fill_between(df_p.index, df_p['RSI'], 50,
                     where=df_p['RSI'] >= 50, alpha=0.1, color=DARK["green"])
    ax2.fill_between(df_p.index, df_p['RSI'], 50,
                     where=df_p['RSI'] < 50,  alpha=0.1, color=DARK["red"])
    ax2.set_ylabel("RSI", color=DARK["text"], fontsize=8)
    ax2.set_ylim(0, 100)
    ax2.set_xticklabels([])

    # — MACD —
    ax3.plot(df_p.index, df_p['MACD'],       color=DARK["accent"], linewidth=1.2, label='MACD')
    ax3.plot(df_p.index, df_p['Signal_Line'], color=DARK["yellow"], linewidth=1.0,
             linestyle='--', label='Señal')
    cols_hist = [DARK["green"] if x > 0 else DARK["red"] for x in df_p['Histogram']]
    ax3.bar(df_p.index, df_p['Histogram'], color=cols_hist, alpha=0.4, width=1)
    ax3.axhline(0, color=DARK["text"], linewidth=0.5)
    ax3.legend(loc='upper left', fontsize=8, ncol=3,
               facecolor=DARK["panel"], edgecolor=DARK["border"], labelcolor=DARK["text"])
    ax3.set_ylabel("MACD", color=DARK["text"], fontsize=8)
    ax3.set_xticklabels([])

    # — Volumen —
    cols_vol = [DARK["green"] if float(df_p['Close'].iloc[i]) >= float(df_p['Open'].iloc[i])
                else DARK["red"] for i in range(len(df_p))]
    ax4.bar(df_p.index, df_p['Volume'], color=cols_vol, alpha=0.7, width=1)
    ax4.set_ylabel("Volumen", color=DARK["text"], fontsize=8)
    plt.xticks(rotation=30, color=DARK["text"], fontsize=7)

    plt.tight_layout()
    return fig


def plot_radar(ticker, scores_dict):
    categorias = list(scores_dict.keys())
    puntajes   = list(scores_dict.values())
    N          = len(categorias)
    angles     = [n / float(N) * 2 * np.pi for n in range(N)]
    angles    += angles[:1]
    puntajes  += puntajes[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True),
                           facecolor=DARK["bg"])
    ax.set_facecolor(DARK["panel"])
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.plot(angles, puntajes, linewidth=2, color=DARK["accent"])
    ax.fill(angles, puntajes, color=DARK["accent"], alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categorias, color=DARK["text"], size=9, fontweight='bold')
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], color='#4a6fa5', size=7)
    ax.grid(color=DARK["border"], alpha=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor(DARK["border"])

    ax.set_title(f"Perfil Fundamental: {ticker}", size=12, fontweight='bold',
                 color=DARK["accent"], y=1.12)
    plt.tight_layout()
    return fig


@st.cache_data(ttl=600, show_spinner=False)
def cargar_fundamentales(ticker_symbol):
    ticker     = yf.Ticker(ticker_symbol)
    financials = ticker.financials

    cuentas = ["Total Revenue", "Gross Profit", "Operating Income", "Net Income"]
    if not all(c in financials.index for c in cuentas):
        return None

    df_f = pd.DataFrame({
        "Sales":        financials.loc["Total Revenue"],
        "Gross_Profit": financials.loc["Gross Profit"],
        "Op_Income":    financials.loc["Operating Income"],
        "Net_Income":   financials.loc["Net Income"],
    })

    for col, keys in [("EPS", ["Basic EPS", "Diluted EPS"]),
                      ("Shares", ["Basic Average Shares", "Diluted Average Shares"])]:
        for k in keys:
            if k in financials.index:
                df_f[col] = financials.loc[k]
                break
        else:
            return None

    df_f.index = pd.to_datetime(df_f.index).year
    df_f       = df_f.sort_index().dropna()

    df_f["Gross_Margin"] = (df_f["Gross_Profit"] / df_f["Sales"]) * 100
    df_f["Op_Margin"]    = (df_f["Op_Income"]    / df_f["Sales"]) * 100
    df_f["Net_Margin"]   = (df_f["Net_Income"]   / df_f["Sales"]) * 100

    hist = ticker.history(period="5y")
    if hist.empty:
        return None
    hist["Year"] = hist.index.year
    precios      = hist.groupby("Year")["Close"].mean()

    dm = df_f.join(precios, how="inner")
    dm["PE_Ratio"]   = dm["Close"] / dm["EPS"]
    dm["Market_Cap"] = dm["Close"] * dm["Shares"]
    dm["PS_Ratio"]   = dm["Market_Cap"] / dm["Sales"]
    return dm.tail(6)


def plot_matriz(dm, ticker_symbol):
    years_str = [str(y) for y in dm.index]
    plt.rcParams.update(plt.rcParamsDefault)
    fig, axes = plt.subplots(2, 4, figsize=(22, 9), facecolor=DARK["bg"])

    paleta = {
        'eps':   '#4fc3f7', 'sales': '#9b67f7', 'shares': '#00e5ff',
        'mcap':  '#ffd740', 'pe':    '#f48fb1', 'ps':     '#ff8a65',
        'gm':    '#a5d6a7', 'margins': '#ef5350',
    }

    def estilo_ax(ax):
        ax.set_facecolor(DARK["panel"])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        for sp in ['left', 'bottom']:
            ax.spines[sp].set_edgecolor(DARK["border"])
        ax.grid(axis="y", linestyle="--", alpha=0.3, color=DARK["border"])
        ax.tick_params(colors=DARK["text"], labelsize=8)
        ax.set_xticklabels(years_str, color=DARK["text"], fontsize=8)

    def etiquetar(ax, barras, fmt, ref, interior=False):
        max_h = ref.max()
        for b in barras:
            h = b.get_height()
            if h == 0 or np.isnan(h):
                continue
            y = (h - max_h * 0.07) if interior else (h + max_h * 0.02)
            c = '#ffffff' if interior else DARK["text"]
            ax.text(b.get_x() + b.get_width() / 2, y, fmt.format(h),
                    ha="center", va="center" if interior else "bottom",
                    color=c, fontsize=8, fontweight="bold")

    # 1. EPS
    estilo_ax(axes[0, 0])
    b = axes[0, 0].bar(years_str, dm["EPS"], color=paleta['eps'], width=0.55)
    etiquetar(axes[0, 0], b, "{:.2f}", dm["EPS"])
    axes[0, 0].set_title("GAAP EPS", color=DARK["accent"], fontweight="bold", pad=8, fontsize=10, loc='left')

    # 2. Sales
    estilo_ax(axes[0, 1])
    sb = dm["Sales"] / 1e9
    b  = axes[0, 1].bar(years_str, sb, color=paleta['sales'], width=0.55)
    etiquetar(axes[0, 1], b, "{:.1f}", sb)
    axes[0, 1].set_title("Sales ($bln)", color=DARK["accent"], fontweight="bold", pad=8, fontsize=10, loc='left')

    # 3. Shares
    estilo_ax(axes[0, 2])
    shb = dm["Shares"] / 1e9
    axes[0, 2].set_ylim(0, shb.max() * 1.15)
    b   = axes[0, 2].bar(years_str, shb, color=paleta['shares'], width=0.55)
    etiquetar(axes[0, 2], b, "{:.2f}", shb, interior=True)
    axes[0, 2].set_title("Shares Outstanding (bln)", color=DARK["accent"], fontweight="bold", pad=8, fontsize=10, loc='left')

    # 4. Market Cap
    estilo_ax(axes[0, 3])
    mc = dm["Market_Cap"] / 1e9
    b  = axes[0, 3].bar(years_str, mc, color=paleta['mcap'], width=0.55)
    etiquetar(axes[0, 3], b, "{:.1f}", mc)
    axes[0, 3].set_title("Market Cap ($bln)", color=DARK["accent"], fontweight="bold", pad=8, fontsize=10, loc='left')

    # 5. P/E
    estilo_ax(axes[1, 0])
    b = axes[1, 0].bar(years_str, dm["PE_Ratio"], color=paleta['pe'], width=0.55)
    etiquetar(axes[1, 0], b, "{:.1f}x", dm["PE_Ratio"])
    axes[1, 0].set_title("Price / Earnings", color=DARK["accent"], fontweight="bold", pad=8, fontsize=10, loc='left')

    # 6. P/S
    estilo_ax(axes[1, 1])
    b = axes[1, 1].bar(years_str, dm["PS_Ratio"], color=paleta['ps'], width=0.55)
    etiquetar(axes[1, 1], b, "{:.2f}x", dm["PS_Ratio"])
    axes[1, 1].set_title("Price / Sales", color=DARK["accent"], fontweight="bold", pad=8, fontsize=10, loc='left')

    # 7. Gross Margin
    estilo_ax(axes[1, 2])
    axes[1, 2].set_ylim(0, 110)
    b = axes[1, 2].bar(years_str, dm["Gross_Margin"], color=paleta['gm'], width=0.55)
    etiquetar(axes[1, 2], b, "{:.1f}%", dm["Gross_Margin"], interior=True)
    axes[1, 2].set_title("Gross Margin (%)", color=DARK["accent"], fontweight="bold", pad=8, fontsize=10, loc='left')

    # 8. Op vs Net Margin
    estilo_ax(axes[1, 3])
    axes[1, 3].bar(years_str, dm["Net_Margin"], color="#2b5c8f", width=0.55, label="Net Margin")
    axes[1, 3].plot(years_str, dm["Op_Margin"], color=paleta['margins'],
                    marker="o", linewidth=2, label="Op Margin")
    axes[1, 3].set_title("Op vs Net Margin (%)", color=DARK["accent"], fontweight="bold", pad=8, fontsize=10, loc='left')
    axes[1, 3].legend(frameon=False, fontsize=8, loc="upper left",
                      labelcolor=DARK["text"])

    fig.suptitle(f"ESCÁNER FUNDAMENTAL  ·  {ticker_symbol.upper()}",
                 color=DARK["accent"], fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem 0;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:1.3rem;
                    font-weight:700; color:#00b4d8; letter-spacing:3px;">
            TERMINAL
        </div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.6rem;
                    color:#4a6fa5; letter-spacing:4px; margin-top:2px;">
            ANÁLISIS INTEGRAL
        </div>
    </div>
    """, unsafe_allow_html=True)

    ticker_input = st.text_input(
        "Ticker",
        value="AAPL",
        placeholder="AAPL, MSFT, TSLA...",
        help="Introduce el símbolo de Yahoo Finance"
    ).upper().strip()

    analizar = st.button("▶  ANALIZAR", use_container_width=True)

    st.markdown('<hr class="hr-term">', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace; font-size:0.6rem;
                color:#4a6fa5; letter-spacing:2px; text-transform:uppercase;">
        Módulos activos
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace; font-size:0.72rem; color:#8eacc8; line-height:2;">
        ✦ &nbsp;Análisis Técnico<br>
        ✦ &nbsp;Indicadores (RSI · MACD · BB)<br>
        ✦ &nbsp;Soportes &amp; Resistencias<br>
        ✦ &nbsp;Escáner Fundamental<br>
        ✦ &nbsp;Sentimiento de Noticias<br>
        ✦ &nbsp;Scores Fundamentales
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="hr-term">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-family:'IBM Plex Mono',monospace; font-size:0.6rem; color:#2a4a6a;">
        Datos: Yahoo Finance · NewsAPI<br>
        Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════

st.markdown("""
<div class="terminal-header">
    <h1>📈 TERMINAL FINANCIERA</h1>
    <p>ANÁLISIS TÉCNICO · FUNDAMENTAL · SENTIMIENTO DE MERCADO</p>
</div>
""", unsafe_allow_html=True)

if not analizar:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem; font-family:'IBM Plex Mono',monospace;">
        <div style="font-size:3rem; margin-bottom:1rem;">⬡</div>
        <div style="font-size:0.8rem; color:#4a6fa5; letter-spacing:3px;">
            INTRODUCE UN TICKER Y PRESIONA ANALIZAR
        </div>
        <div style="font-size:0.65rem; color:#2a4a6a; margin-top:0.5rem;">
            Ejemplos: AAPL · MSFT · TSLA · NVDA · AMZN · GOOGL
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Carga de datos ──────────────────────────────────────────────
with st.spinner(f"Descargando datos para {ticker_input}..."):
    try:
        df_raw = cargar_df(ticker_input)
        if df_raw.empty:
            st.error(f"❌ No se encontraron datos para **{ticker_input}**. Verifica el símbolo.")
            st.stop()
        info     = cargar_info(ticker_input)
        df       = calcular_indicadores(df_raw)
        niveles  = calcular_niveles(df)
        scores   = calcular_scores(info)
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")
        st.stop()

# ── Variables clave ──────────────────────────────────────────────
u            = df.iloc[-1]
precio       = float(u['Close'])
target_price = info.get('targetMeanPrice')
low_52       = info.get('fiftyTwoWeekLow',  float(df['Low'].min()))
high_52      = info.get('fiftyTwoWeekHigh', float(df['High'].max()))
vol_prom     = float(df['Volume'].tail(20).mean())
rsi_val      = float(u['RSI'])
sops = [n[0] for n in niveles if n[1] == 'Soporte'     and n[0] < precio]
ress = [n[0] for n in niveles if n[1] == 'Resistencia' and n[0] > precio]
tendencia    = "ALCISTA" if precio > float(u['SMA200']) else "BAJISTA"

nombre       = info.get('longName', ticker_input)
sector       = info.get('sector', 'N/D')
industria    = info.get('industry', 'N/D')

# ── Header con nombre ─────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex; align-items:baseline; gap:1rem; margin-bottom:1rem;">
    <span style="font-family:'IBM Plex Mono',monospace; font-size:1.8rem;
                 font-weight:700; color:#e2e8f0;">{ticker_input}</span>
    <span style="font-family:'IBM Plex Sans',sans-serif; font-size:1rem;
                 color:#64748b;">{nombre}</span>
    <span style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem;
                 color:#4a6fa5; border:1px solid #1e3a5f; padding:0.2rem 0.5rem;
                 border-radius:3px;">{sector}</span>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊  TÉCNICO", "🏛️  FUNDAMENTAL", "📰  SENTIMIENTO"])

# ═══════════════════════════
#  TAB 1 — TÉCNICO
# ═══════════════════════════
with tab1:
    # Métricas rápidas en fila
    c1, c2, c3, c4, c5 = st.columns(5)

    def color_class(val, ref, invert=False):
        if invert:
            return "negative" if val > ref else "positive"
        return "positive" if val > ref else "negative"

    pot_str = ""
    if target_price:
        pot = ((target_price - precio) / precio) * 100
        pot_str = f'<div class="metric-sub">Target ${target_price:.2f} · {pot:+.1f}%</div>'

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Precio Actual</div>
            <div class="metric-value">${precio:,.2f}</div>
            {pot_str}
        </div>""", unsafe_allow_html=True)

    rsi_cls = "negative" if rsi_val > 70 else ("positive" if rsi_val < 30 else "neutral")
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">RSI (14)</div>
            <div class="metric-value {rsi_cls}">{rsi_val:.1f}</div>
            <div class="metric-sub">{'Sobrecompra' if rsi_val>70 else 'Sobreventa' if rsi_val<30 else 'Zona Neutra'}</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        t_cls = "positive" if tendencia == "ALCISTA" else "negative"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Tendencia SMA200</div>
            <div class="metric-value {t_cls}">{tendencia}</div>
            <div class="metric-sub">SMA200: ${float(u['SMA200']):.2f}</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        sop_str = f"${sops[-1]:.2f}" if sops else "N/D"
        res_str = f"${ress[-1]:.2f}" if ress else "N/D"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Soporte / Resistencia</div>
            <div class="metric-value positive" style="font-size:1rem;">{sop_str}</div>
            <div class="metric-sub" style="color:#ff5252;">{res_str} Resist.</div>
        </div>""", unsafe_allow_html=True)

    vol_cls = "positive" if float(u['Volume']) > vol_prom else "neutral"
    with c5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Volumen Hoy</div>
            <div class="metric-value {vol_cls}">{int(u['Volume']):,}</div>
            <div class="metric-sub">Prom 20d: {int(vol_prom):,}</div>
        </div>""", unsafe_allow_html=True)

    # Gráfico técnico
    with st.spinner("Renderizando gráfico técnico..."):
        fig_tec = plot_tecnico(df, ticker_input, niveles, target_price, low_52, high_52)
        st.pyplot(fig_tec, use_container_width=True)
        plt.close(fig_tec)

    # Niveles de soporte / resistencia
    if niveles:
        st.markdown('<div class="section-header">SOPORTES &amp; RESISTENCIAS DETECTADOS</div>', unsafe_allow_html=True)
        col_s, col_r = st.columns(2)
        sops_all = [(n, t) for n, t in niveles if t == 'Soporte']
        ress_all = [(n, t) for n, t in niveles if t == 'Resistencia']

        with col_s:
            if sops_all:
                html = '<table class="levels-table"><thead><tr><th>Soporte</th><th>Dist. actual</th></tr></thead><tbody>'
                for n, _ in sorted(sops_all, reverse=True)[:6]:
                    dist = ((precio - n) / precio) * 100
                    html += f'<tr><td class="lvl-soporte">${n:.2f}</td><td style="color:#64748b;">{dist:.2f}%</td></tr>'
                html += '</tbody></table>'
                st.markdown(html, unsafe_allow_html=True)

        with col_r:
            if ress_all:
                html = '<table class="levels-table"><thead><tr><th>Resistencia</th><th>Dist. actual</th></tr></thead><tbody>'
                for n, _ in sorted(ress_all)[:6]:
                    dist = ((n - precio) / precio) * 100
                    html += f'<tr><td class="lvl-resistencia">${n:.2f}</td><td style="color:#64748b;">+{dist:.2f}%</td></tr>'
                html += '</tbody></table>'
                st.markdown(html, unsafe_allow_html=True)

    # Bollinger
    st.markdown('<div class="section-header">BANDAS DE BOLLINGER</div>', unsafe_allow_html=True)
    bcol1, bcol2, bcol3 = st.columns(3)
    bb_status = ("🔴 SOBRECOMPRA" if precio >= float(u['Upper_Band'])
                 else "🟢 SOBREVENTA" if precio <= float(u['Lower_Band']) else "⚪ NEUTRO")
    with bcol1:
        st.markdown(f"""
        <div class="metric-card"><div class="metric-label">Banda Superior</div>
        <div class="metric-value" style="font-size:1.1rem;">${float(u['Upper_Band']):.2f}</div></div>
        """, unsafe_allow_html=True)
    with bcol2:
        st.markdown(f"""
        <div class="metric-card"><div class="metric-label">SMA20 / Media</div>
        <div class="metric-value" style="font-size:1.1rem;">${float(u['SMA20']):.2f}</div>
        <div class="metric-sub">{bb_status}</div></div>
        """, unsafe_allow_html=True)
    with bcol3:
        st.markdown(f"""
        <div class="metric-card"><div class="metric-label">Banda Inferior</div>
        <div class="metric-value" style="font-size:1.1rem;">${float(u['Lower_Band']):.2f}</div></div>
        """, unsafe_allow_html=True)


# ═══════════════════════════
#  TAB 2 — FUNDAMENTAL
# ═══════════════════════════
with tab2:
    col_radar, col_scores = st.columns([1, 1])

    with col_radar:
        st.markdown('<div class="section-header">RADAR FUNDAMENTAL</div>', unsafe_allow_html=True)
        fig_rad = plot_radar(ticker_input, scores)
        st.pyplot(fig_rad, use_container_width=True)
        plt.close(fig_rad)

    with col_scores:
        st.markdown('<div class="section-header">SCORES (/ 10)</div>', unsafe_allow_html=True)
        for cat, val in scores.items():
            pct = int(val * 10)
            st.markdown(f"""
            <div class="score-row">
                <div class="score-name">{cat}</div>
                <div class="score-num">{val:.1f}</div>
                <div class="score-bar-wrap">
                    <div class="score-bar-bg">
                        <div class="score-bar-fill" style="width:{pct}%"></div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Info adicional
        st.markdown('<div class="section-header" style="margin-top:1.5rem;">DATOS EMPRESA</div>', unsafe_allow_html=True)
        datos = [
            ("Sector",      sector),
            ("Industria",   industria),
            ("P/E Fwd.",    f"{info.get('forwardPE', 'N/D'):.1f}x" if info.get('forwardPE') else "N/D"),
            ("P/B",         f"{info.get('priceToBook', 'N/D'):.2f}x" if info.get('priceToBook') else "N/D"),
            ("Div. Yield",  f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "N/D"),
            ("Mkt Cap",     f"${info.get('marketCap', 0)/1e9:.1f}B" if info.get('marketCap') else "N/D"),
            ("52W Low",     f"${low_52:.2f}"),
            ("52W High",    f"${high_52:.2f}"),
        ]
        for label, val in datos:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:0.35rem 0;
                        border-bottom:1px solid #1a2a3a; font-family:'IBM Plex Mono',monospace;">
                <span style="font-size:0.7rem; color:#4a6fa5;">{label}</span>
                <span style="font-size:0.72rem; color:#c8d6e5;">{val}</span>
            </div>""", unsafe_allow_html=True)

    # Matriz 2x4
    st.markdown('<div class="section-header">MATRIZ DE VALORACIÓN HISTÓRICA</div>', unsafe_allow_html=True)
    with st.spinner("Cargando datos financieros históricos..."):
        dm = cargar_fundamentales(ticker_input)

    if dm is not None and not dm.empty:
        fig_mat = plot_matriz(dm, ticker_input)
        st.pyplot(fig_mat, use_container_width=True)
        plt.close(fig_mat)
    else:
        st.warning("⚠️ No se pudieron obtener estados financieros completos para este ticker. "
                   "Es posible que Yahoo Finance no tenga datos suficientes.")


# ═══════════════════════════
#  TAB 3 — SENTIMIENTO
# ═══════════════════════════
with tab3:
    st.markdown('<div class="section-header">ANÁLISIS DE SENTIMIENTO DE NOTICIAS</div>', unsafe_allow_html=True)

    with st.spinner("Analizando noticias recientes..."):
        score_sent, count_news, titulos = obtener_sentimiento(ticker_input)

    if count_news == 0:
        st.warning("⚠️ No se encontraron noticias recientes o la NewsAPI no está disponible.")
    else:
        # Score global
        sent_label = ("POSITIVO" if score_sent > 0.05 else
                      "NEGATIVO" if score_sent < -0.05 else "NEUTRAL")
        sent_cls   = ("sent-positive" if score_sent > 0.05 else
                      "sent-negative" if score_sent < -0.05 else "sent-neutral")
        emoji      = "😊" if score_sent > 0.05 else "😡" if score_sent < -0.05 else "😐"

        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Sentimiento Global</div>
                <div class="metric-value" style="font-size:1.2rem;">{emoji} {sent_label}</div>
                <div class="metric-sub">Score promedio: {score_sent:.3f}</div>
            </div>""", unsafe_allow_html=True)
        with mc2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Artículos analizados</div>
                <div class="metric-value neutral">{count_news}</div>
                <div class="metric-sub">Últimas noticias en inglés</div>
            </div>""", unsafe_allow_html=True)
        with mc3:
            positivas = sum(1 for t in titulos if t['score'] > 0.05)
            negativas = sum(1 for t in titulos if t['score'] < -0.05)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Distribución</div>
                <div class="metric-value positive" style="font-size:1rem; display:inline;">{positivas}+</div>
                &nbsp;
                <div class="metric-value negative" style="font-size:1rem; display:inline;">{negativas}-</div>
                <div class="metric-sub">{count_news - positivas - negativas} neutras</div>
            </div>""", unsafe_allow_html=True)

        # Gauge visual
        gauge_pct = int((score_sent + 1) / 2 * 100)
        gauge_color = ("#00e676" if score_sent > 0.05 else
                       "#ff5252" if score_sent < -0.05 else "#ffd740")
        st.markdown(f"""
        <div style="margin: 1.5rem 0; padding: 1rem; background:#0d1421;
                    border:1px solid #1e3a5f; border-radius:6px;">
            <div style="font-family:'IBM Plex Mono',monospace; font-size:0.65rem;
                        color:#4a6fa5; letter-spacing:2px; margin-bottom:0.6rem;">
                MEDIDOR DE SENTIMIENTO
            </div>
            <div style="background:#1e3a5f; border-radius:10px; height:12px; position:relative;">
                <div style="width:{gauge_pct}%; height:100%; background:{gauge_color};
                            border-radius:10px; transition:width 0.5s;"></div>
                <div style="position:absolute; left:50%; top:-4px; width:2px; height:20px;
                            background:#4a6fa5; transform:translateX(-50%);"></div>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:0.3rem;
                        font-family:'IBM Plex Mono',monospace; font-size:0.6rem; color:#4a6fa5;">
                <span>MUY NEGATIVO</span><span>NEUTRAL</span><span>MUY POSITIVO</span>
            </div>
        </div>""", unsafe_allow_html=True)

        # Tabla de noticias
        st.markdown('<div class="section-header">NOTICIAS RECIENTES</div>', unsafe_allow_html=True)
        for t in titulos:
            s = t['score']
            cls_ = "sent-positive" if s > 0.05 else "sent-negative" if s < -0.05 else "sent-neutral"
            icon = "▲" if s > 0.05 else "▼" if s < -0.05 else "—"
            url_link = f'<a href="{t["url"]}" target="_blank" style="color:#00b4d8;">↗</a>' if t.get('url') else ''
            st.markdown(f"""
            <div style="display:flex; align-items:flex-start; gap:0.8rem; padding:0.8rem 0;
                        border-bottom:1px solid #1a2a3a;">
                <span class="sentiment-badge {cls_}" style="flex-shrink:0;">{icon} {s:+.2f}</span>
                <div>
                    <div style="font-family:'IBM Plex Sans',sans-serif; font-size:0.82rem;
                                color:#c8d6e5; line-height:1.4;">{t['title']} {url_link}</div>
                    <div style="font-family:'IBM Plex Mono',monospace; font-size:0.65rem;
                                color:#4a6fa5; margin-top:0.3rem;">{t.get('source','')}</div>
                </div>
            </div>""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem 0; font-family:'IBM Plex Mono',monospace;
            font-size:0.6rem; color:#2a4a6a; letter-spacing:1px;">
    Datos: Yahoo Finance · NewsAPI · TextBlob &nbsp;·&nbsp;
    No constituye asesoría financiera &nbsp;·&nbsp;
    Solo para fines informativos
</div>""", unsafe_allow_html=True)
