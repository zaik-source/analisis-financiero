# 📈 Terminal Financiera — Streamlit App

Análisis integral de acciones: técnico, fundamental y sentimiento de noticias.

## Estructura de archivos

```
terminal-financiera/
├── app.py                    ← App principal
├── requirements.txt          ← Dependencias
└── .streamlit/
    ├── config.toml           ← Tema oscuro
    └── secrets.toml          ← API keys (NO subir a GitHub)
```

---

## 🚀 Despliegue en Streamlit Cloud (gratis)

### Paso 1 — Crear repositorio en GitHub
1. Ve a [github.com](https://github.com) → **New repository**
2. Nombre: `terminal-financiera` (o el que prefieras)
3. Visibilidad: **Public** (requerido para Streamlit Cloud gratuito)
4. Sube los archivos:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
   - ⚠️ **NO subas** `.streamlit/secrets.toml` (contiene tu API key)

### Paso 2 — Conectar con Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con tu cuenta de GitHub
3. Clic en **"New app"**
4. Selecciona tu repositorio y rama (`main`)
5. En **"Main file path"** escribe: `app.py`
6. Clic en **"Deploy"**

### Paso 3 — Configurar el Secret (NewsAPI)
1. En Streamlit Cloud, ve a tu app → **⚙️ Settings → Secrets**
2. Pega exactamente esto:
   ```toml
   NEWS_API_KEY = "f525b346861347859c34dfa92d6ec99a"
   ```
3. Clic en **Save**

### ✅ ¡Listo!
Tu app estará disponible en una URL pública tipo:
`https://tu-usuario-terminal-financiera-app-xxxx.streamlit.app`

---

## 🖥️ Correr en local (opcional)

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Módulos incluidos

| Tab | Contenido |
|-----|-----------|
| 📊 Técnico | Precio · SMA 20/50/200 · Bollinger · RSI · MACD · Volumen · Bullet Chart |
| 🏛️ Fundamental | Radar de scores · Matriz 2×4 (EPS, Sales, P/E, P/S, Márgenes) |
| 📰 Sentimiento | Score TextBlob de noticias · Gauge · Tabla con links |

---

## Notas
- Datos extraídos de **Yahoo Finance** (yfinance) y **NewsAPI**
- La NewsAPI gratuita tiene límite de 100 requests/día
- Para uso intensivo, considera actualizar a un plan de pago en newsapi.org
