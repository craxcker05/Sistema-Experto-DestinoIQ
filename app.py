# ==========================================
# Archivo: app.py
# Sistema Experto: Recomendador de Destinos de Viaje
# Interfaz tipo Dashboard SaaS con paleta veraniega (mar, sol y coral)
# construida con CSS personalizado sobre Streamlit.
# Ejecutar con:  streamlit run app.py
# ==========================================

import html

import streamlit as st

from motor import (
    PREGUNTAS,
    REGLAS,
    evaluar_reglas,
    inferir_destino,
    inferir_top,
)

st.set_page_config(
    page_title="DestinoIQ · Sistema Experto de Viajes",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 1. ESTILO GENERAL — paleta veraniega (mar, sol y coral)
#    Todas las variables de color están en :root para poder
#    retocar la gama desde un único sitio.
# =========================================================
CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
  /* Superficies: arena clara y agua fría */
  --bg:#FFF9F0;            /* fondo general: crema arena */
  --bg-side:#EAFBF6;       /* sidebar: agua muy clara */
  --card:#FFFFFF;          /* tarjetas */
  --card-2:#F4FBFC;        /* píldoras / superficie 2: celeste muy claro */
  --line:rgba(11,92,102,.12);

  /* Textos: tinta marina sobre claro */
  --txt:#0E3B44;
  --txt-dim:#5E8189;

  /* Acentos de verano */
  --accent:#00C2A8;        /* turquesa mar */
  --accent-2:#38D5E8;      /* celeste */
  --sun:#FFC53D;           /* sol */
  --coral:#FF7B6B;         /* coral atardecer */
  --ok:#12A97B;
  --warn:#F59E0B;
}

/* ---------- Tipografía ---------- */
html, body, .stApp, .stApp *{
  font-family:'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
  letter-spacing:.005em;
}

/* ---------- Fondo y superficies ---------- */
[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(1100px 520px at 12% -8%, rgba(0,194,168,.16), transparent 60%),
    radial-gradient(900px 480px at 95% 8%, rgba(255,197,61,.20), transparent 55%),
    radial-gradient(800px 520px at 62% 105%, rgba(255,123,107,.12), transparent 60%),
    var(--bg) !important;
}
[data-testid="stHeader"]{ background:transparent !important; }
[data-testid="stToolbar"]{ background:transparent !important; }
[data-testid="stDecoration"]{ display:none !important; }
[data-testid="stDeployButton"]{ display:none !important; }
#MainMenu{ visibility:hidden !important; }
[data-testid="stSidebar"]{
  background:var(--bg-side) !important;
  border-right:1px solid var(--line) !important;
}
[data-testid="stSidebar"] > div{ padding-top:1.4rem !important; padding-left:1.1rem !important; padding-right:1.1rem !important; }
[data-testid="stMainBlockContainer"]{ max-width:1140px !important; padding-top:2.4rem !important; padding-bottom:3.5rem !important; }

/* ---------- Título de página (oculto: usamos cabecera HTML) ---------- */
h1{ font-size:inherit !important; }

/* ---------- Divisores suaves ---------- */
hr{ border:none !important; height:1px !important;
    background:linear-gradient(90deg, transparent, rgba(11,92,102,.18), transparent) !important; }

/* ---------- Cabecera de la app ---------- */
.app-badge{
  display:inline-block; padding:.3rem .75rem; border-radius:999px;
  background:rgba(0,194,168,.13); border:1px solid rgba(0,194,168,.42);
  color:#0A9C88; font-size:.68rem; font-weight:700;
  letter-spacing:.18em; text-transform:uppercase;
}
.app-header h1{
  margin:.6rem 0 .35rem !important; font-size:2.15rem !important; font-weight:800 !important;
  letter-spacing:-.02em; line-height:1.15;
  background:linear-gradient(92deg,#FF6B6B 6%, #FFB347 52%, #00C2A8 96%);
  -webkit-background-clip:text; background-clip:text; color:transparent; font-family:inherit !important;
}
.app-header p{ margin:0; color:var(--txt-dim); font-size:.97rem; max-width:780px; line-height:1.6; }

/* ---------- Títulos de sección ---------- */
.section{ display:flex; align-items:center; gap:.65rem; margin:1.6rem 0 .7rem; }
.section .bar{ flex:none; width:4px; height:20px; border-radius:4px;
  background:linear-gradient(180deg,var(--accent),var(--sun)); }
.section h3{ margin:0 !important; font-size:1.1rem !important; font-weight:700 !important; color:#0E3B44 !important; }
.section .hint{ margin-left:auto; font-size:.76rem; color:var(--txt-dim); }

/* ---------- Barra de progreso integrada ---------- */
.progress-wrap{
  background:var(--card); border:1px solid var(--line); border-radius:12px;
  padding:13px 17px; margin:.1rem 0 1.1rem;
  box-shadow:0 8px 22px rgba(6,90,100,.10);
}
.progress-head{ display:flex; justify-content:space-between; font-size:.77rem;
  color:var(--txt-dim); margin-bottom:.55rem; letter-spacing:.05em; text-transform:uppercase; }
.progress-head b{ color:#0E3B44; font-weight:700; }
.progress-track{ height:6px; background:#E7F4F1; border-radius:99px; overflow:hidden;
  border:1px solid rgba(11,92,102,.08); }
.progress-fill{ height:100%; border-radius:99px;
  background:linear-gradient(90deg,#00C2A8,#7BDFF2 55%,#FFC53D);
  box-shadow:0 0 12px rgba(0,194,168,.45); transition:width .45s cubic-bezier(.4,0,.2,1); }

/* ---------- Tarjetas de preguntas ---------- */
[data-testid="stVerticalBlockBorderWrapper"]{
  background:linear-gradient(180deg, #FFFFFF, #F8FDFC) !important;
  border:1px solid var(--line) !important;
  border-radius:14px !important;
  box-shadow:0 10px 26px rgba(6,90,100,.10) !important;
}
[data-testid="stVerticalBlockBorderWrapper"] > div{ border-radius:14px !important; border-color:transparent !important; }
.stVerticalBlockBorderWrapper > div{ border:none !important; }

/* Etiqueta de la pregunta */
[data-testid="stWidgetLabel"] p{
  color:#0E3B44 !important; font-weight:600 !important; font-size:.93rem !important;
  line-height:1.4 !important;
}
[data-testid="stWidgetLabel"]{ color:#0E3B44 !important; }

/* ---------- Opciones tipo radio (píldoras) ---------- */
[data-testid="stRadio"] label,
[data-testid="stRadio"] div[role="radio"]{
  background:var(--card-2);
  border:1px solid var(--line);
  border-radius:10px;
  padding:.45rem .85rem;
  margin:.05rem 0 .4rem;
  color:#33636C;
  font-size:.89rem;
  transition:all .18s ease;
}
[data-testid="stRadio"] label:hover,
[data-testid="stRadio"] div[role="radio"]:hover{
  border-color:rgba(255,123,107,.55);
  background:rgba(255,123,107,.10);
  color:#0E3B44;
}
[data-testid="stRadio"] label:has(input:checked),
[data-testid="stRadio"] div[role="radio"][aria-checked="true"],
[data-testid="stRadio"] div:has(> input:checked){
  background:linear-gradient(135deg, #00C2A8 0%, #2BB8E8 100%) !important;
  border-color:transparent !important;
  color:#fff !important;
  font-weight:600;
  box-shadow:0 6px 16px rgba(0,194,168,.35);
}
input[type="radio"], input[type="checkbox"]{ accent-color:var(--accent); }

/* ---------- Botones ---------- */
[data-testid="stButton"] button{
  width:100% !important;
  border-radius:12px !important;
  padding:.72rem 1.1rem !important;
  font-weight:600 !important;
  font-size:.95rem !important;
  transition:all .22s cubic-bezier(.4,0,.2,1) !important;
}
/* Base neutra = estilo secundario (outline minimalista) */
[data-testid="stButton"] button{
  background:rgba(255,255,255,.75) !important;
  border:1px solid rgba(11,92,102,.20) !important;
  color:#35606B !important;
}
[data-testid="stButton"] button:hover{
  border-color:rgba(255,123,107,.6) !important;
  background:rgba(255,123,107,.10) !important;
  color:#C9472F !important;
}
/* CTA principal: degradado de atardecer (coral → sol). Identificado por la
   columna con .cta-tag, más selectores de respaldo según versión de Streamlit */
[data-testid="stColumn"]:has(.cta-tag) [data-testid="stButton"] button,
button[kind="primary"],
[data-testid="stBaseButton-primary"]{
  background:linear-gradient(135deg,#FF7B6B 0%, #FF9E5E 50%, #FFC53D 100%) !important;
  border:1px solid rgba(255,255,255,.35) !important;
  color:#fff !important;
  box-shadow:0 10px 26px rgba(255,123,107,.40);
  font-weight:700 !important;
  letter-spacing:.02em;
  text-shadow:0 1px 2px rgba(180,70,40,.25);
}
[data-testid="stColumn"]:has(.cta-tag) [data-testid="stButton"] button:hover,
button[kind="primary"]:hover,
[data-testid="stBaseButton-primary"]:hover{
  transform:translateY(-2px);
  box-shadow:0 16px 36px rgba(255,139,91,.55);
  filter:brightness(1.06) saturate(1.05);
  color:#fff !important;
}
/* Contenedor oculto para identificar columnas */
.cta-tag, .reset-tag{ display:none !important; }

/* ---------- Alertas ---------- */
[data-testid="stAlert"]{
  background:#FFF6E6 !important;
  border:1px solid rgba(245,158,11,.45) !important;
  border-radius:12px !important;
  color:#8A5B00 !important;
  font-size:.9rem !important;
}
[data-testid="stAlert"] p{ color:#8A5B00 !important; }

/* ---------- Hero Card: recomendación principal ---------- */
.hero-card{
  position:relative; overflow:hidden;
  background:linear-gradient(135deg, rgba(0,194,168,.17), rgba(255,197,61,.20) 70%);
  border:1px solid rgba(0,194,168,.45);
  border-radius:18px;
  padding:28px 32px;
  margin:.3rem 0 1.2rem;
  box-shadow:0 22px 48px rgba(6,90,100,.18);
}
.hero-card .kicker{
  display:inline-block; font-size:.7rem; font-weight:700; letter-spacing:.2em;
  text-transform:uppercase; color:#0A9C88;
}
.hero-card h2{
  margin:.5rem 0 .5rem; font-size:1.55rem !important; font-weight:750 !important;
  line-height:1.3; color:#0C3B44; font-family:inherit !important;
}
.hero-card p{ margin:0; color:#3E646E; font-size:1rem; line-height:1.6; }
.hero-card .glow{
  position:absolute; right:-45px; top:-45px; width:190px; height:190px; border-radius:50%;
  background:radial-gradient(circle, rgba(255,255,255,.75), transparent 70%);
  pointer-events:none;
}
.hero-card.hero-warn{
  background:linear-gradient(135deg, rgba(255,197,61,.25), rgba(255,123,107,.16) 70%);
  border-color:rgba(255,158,28,.50);
}
.hero-card.hero-warn .kicker{ color:#C97A00; }

/* ---------- Tarjetas secundarias: otras opciones ---------- */
.alt-grid{ display:flex; flex-direction:column; gap:.7rem; margin:.3rem 0 1.3rem; }
.alt-card{
  display:flex; gap:.95rem; align-items:flex-start;
  background:var(--card); border:1px solid var(--line);
  border-radius:14px; padding:15px 17px;
  transition:all .2s ease;
}
.alt-card:hover{
  border-color:rgba(255,123,107,.5);
  transform:translateY(-2px);
  box-shadow:0 12px 26px rgba(6,90,100,.14);
}
.alt-num{
  flex:none; width:30px; height:30px; border-radius:9px;
  display:flex; align-items:center; justify-content:center;
  font-weight:700; font-size:.85rem; color:#fff;
  background:linear-gradient(135deg,var(--accent),var(--accent-2));
  box-shadow:0 6px 14px rgba(0,194,168,.35);
}
.alt-txt{ color:#3E646E; font-size:.93rem; line-height:1.55; }

/* ---------- Chips de razonamiento ---------- */
.trace-title{
  font-size:.78rem; font-weight:700; letter-spacing:.14em; text-transform:uppercase;
  color:#5E8189; margin:.9rem 0 .45rem;
}
.chip{
  display:inline-block; padding:.26rem .62rem; border-radius:8px;
  font-size:.78rem; margin:.16rem .28rem .16rem 0; font-weight:500;
  font-family:ui-monospace,'JetBrains Mono',Menlo,Consolas,monospace !important;
}
.chip-ok{ background:rgba(18,169,123,.13); color:#0E7A5B; border:1px solid rgba(18,169,123,.35); }
.chip-wild{ background:rgba(0,194,168,.14); color:#088F7E; border:1px solid rgba(0,194,168,.40); }
.chip-miss{ background:rgba(255,123,107,.14); color:#C9472F; border:1px solid rgba(255,123,107,.35); }
.rule-line{ color:#1F4A54; font-size:.9rem; line-height:1.6; margin:.2rem 0 .1rem; }
.rule-line b{ color:#0E3B44; }
.rule-sub{ color:var(--txt-dim); font-size:.84rem; line-height:1.55; }

/* ---------- Expander claro ---------- */
[data-testid="stExpander"] details{
  background:#FFFFFF !important;
  border:1px solid var(--line) !important;
  border-radius:14px !important;
  padding:.35rem 1.05rem !important;
}
[data-testid="stExpander"] summary{
  color:#0E3B44 !important; font-weight:600 !important; font-size:.93rem !important;
  padding:.55rem 0 !important;
}
[data-testid="stExpander"] summary:hover{ color:#0A9C88 !important; }
[data-testid="stExpander"] details[open]{ box-shadow:0 14px 30px rgba(6,90,100,.14); }
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p{ color:#4A707A; font-size:.88rem; }

/* ---------- Sidebar: tarjetas de métricas ---------- */
.side-title{
  font-size:.74rem; letter-spacing:.16em; text-transform:uppercase;
  color:#5E8189; font-weight:700; margin:.2rem 0 .85rem;
}
.metric-card{
  display:flex; align-items:center; gap:.85rem;
  background:linear-gradient(180deg,#FFFFFF,#F7FDFB);
  border:1px solid var(--line);
  border-radius:12px;
  padding:14px 16px;
  margin-bottom:.7rem;
  box-shadow:0 10px 24px rgba(6,90,100,.12);
}
.metric-ico{
  width:40px; height:40px; border-radius:11px;
  display:flex; align-items:center; justify-content:center; font-size:1.15rem;
  background:linear-gradient(135deg, rgba(0,194,168,.22), rgba(255,197,61,.30));
  border:1px solid rgba(0,194,168,.35);
}
.metric-val{ font-size:1.4rem; font-weight:800; color:#0E3B44; line-height:1.05; }
.metric-lab{ font-size:.75rem; color:#5E8189; letter-spacing:.05em; margin-top:.12rem; }
.side-note{
  background:var(--card); border:1px solid var(--line); border-radius:12px;
  padding:12px 14px; color:var(--txt-dim); font-size:.78rem; line-height:1.6;
}
.side-note b{ color:#0E3B44; }

/* ---------- Pies y subtítulos ---------- */
[data-testid="stCaptionContainer"], p small{ color:#7A969E !important; font-size:.78rem !important; }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# =========================================================
# 2. ESTADO Y LÓGICA (idéntica a la versión anterior)
# =========================================================
if "resultado" not in st.session_state:
    st.session_state["resultado"] = None


def _obtener_hechos():
    """Lee las respuestas actuales de los widgets (None = sin responder)."""
    return {p["id"]: st.session_state.get(f"p_{p['id']}") for p in PREGUNTAS}


def _firma(hechos):
    """Huella del perfil actual: cambia si el usuario modifica cualquier respuesta."""
    return tuple(sorted(hechos.items()))


def _realizar_inferencia(hechos):
    """Ejecuta el motor y guarda todo lo necesario para explicar el razonamiento."""
    principal = inferir_destino(hechos)
    alternativas = [r for r in inferir_top(hechos, n=3) if r != principal]
    evaluacion = evaluar_reglas(hechos)
    st.session_state["firma_resultado"] = _firma(hechos)
    st.session_state["resultado"] = {
        "hechos": dict(hechos),
        "principal": principal,
        "es_fallback": principal.startswith("Destino Explorador"),
        "alternativas": alternativas,
        "ganadora": next((e for e in evaluacion if e["conclusion"] == principal), None),
        "activadas": [e for e in evaluacion if e["activada"] and e["conclusion"] != principal],
        "casi_ganadoras": [
            e for e in evaluacion if not e["activada"] and 0 < e["porcentaje"] < 100
        ][:3],
        "reglas_evaluadas": len(evaluacion),
    }


def _section(titulo, hint=""):
    """Cabecera de sección con barra de acento."""
    extra = f'<span class="hint">{hint}</span>' if hint else ""
    st.markdown(
        f'<div class="section"><span class="bar"></span><h3>{titulo}</h3>{extra}</div>',
        unsafe_allow_html=True,
    )


def _chips(valores, clase="auto"):
    """Renderiza chips HTML. 'auto': verde si se cumplió, violeta si fue por 'Me da igual'."""
    salida = []
    for valor in valores:
        css = clase
        if clase == "auto":
            css = "chip-wild" if "Me da igual" in valor else "chip-ok"
        salida.append(f'<span class="chip {css}">{html.escape(valor)}</span>')
    return "".join(salida)


# =========================================================
# 3. BARRA LATERAL — tarjetas de métricas
# =========================================================
with st.sidebar:
    st.markdown(
        '<div class="side-title">📊 Panel del sistema</div>', unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-ico">📚</div>
          <div>
            <div class="metric-val">{len(REGLAS)}</div>
            <div class="metric-lab">REGLAS CARGADAS</div>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-ico">🧭</div>
          <div>
            <div class="metric-val">{len(PREGUNTAS)}</div>
            <div class="metric-lab">ATRIBUTOS DEL PERFIL</div>
          </div>
        </div>
        <div class="metric-ico" style="width:auto;border:none;background:none;box-shadow:none;">&nbsp;</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="side-note">
          <b>Cómo funciona</b><br>
          El motor equipara tus respuestas con las reglas de la base de
          conocimiento y resuelve los conflictos eligiendo la regla más
          específica.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="side-note" style="margin-top:.7rem;">Motor: <b>motor.py</b> · '
        'Interfaz: <b>app.py</b></div>',
        unsafe_allow_html=True,
    )

# =========================================================
# 4. CABECERA PRINCIPAL
# =========================================================
st.markdown(
    """
    <div class="app-header">
      <span class="app-badge">Sistema Experto · Inferencia basada en reglas</span>
      <h1>✈️ DestinoIQ — Sugerencia de Destino de Viajes</h1>
      <p>Responde tu perfil de viajero y el motor de inferencia elegirá el
      destino ideal para ti.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 5. FORMULARIO DE PERFIL
# =========================================================
_section("Tu perfil de viajero", "Pulsa la opción que mejor te describa")

hechos_temp = {p["id"]: st.session_state.get(f"p_{p['id']}") for p in PREGUNTAS}
respondidas = sum(1 for v in hechos_temp.values() if v)
porcentaje = int(100 * respondidas / len(PREGUNTAS))

st.markdown(
    f"""
    <div class="progress-wrap">
      <div class="progress-head">
        <span>Perfil completado</span>
        <span><b>{respondidas}</b> / {len(PREGUNTAS)} preguntas</span>
      </div>
      <div class="progress-track">
        <div class="progress-fill" style="width:{porcentaje}%;"></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

for fila in range(0, len(PREGUNTAS), 2):
    columnas = st.columns(2, gap="medium")
    for desplazamiento, columna in enumerate(columnas):
        indice = fila + desplazamiento
        if indice >= len(PREGUNTAS):
            continue
        pregunta = PREGUNTAS[indice]
        with columna, st.container(border=True):
            st.radio(
                pregunta["pregunta"],
                pregunta["opciones"],
                key=f"p_{pregunta['id']}",
                index=None,  # arranca sin responder
            )

hechos = _obtener_hechos()

# Si el usuario cambió alguna respuesta después de ver un resultado,
# descartamos la recomendación obsoleta para que no parezca "estancada".
if st.session_state["resultado"] is not None and st.session_state.get("firma_resultado") != _firma(hechos):
    st.session_state["resultado"] = None
    st.session_state.pop("firma_resultado", None)
    st.caption(
        "↺ Tus respuestas cambiaron: pulsa **Recomendar mi destino** para obtener "
        "la nueva recomendación."
    )

# =========================================================
# 6. BOTONES DE ACCIÓN (CTA + secundario)
# =========================================================
col_cta, col_reset = st.columns(2, gap="medium")

with col_cta:
    st.markdown('<span class="cta-tag"></span>', unsafe_allow_html=True)
    if st.button("Recomendar mi destino", type="primary"):
        if respondidas < 3:
            st.warning("Responde al menos 3 preguntas para que el motor pueda razonar.")
        else:
            _realizar_inferencia(hechos)

with col_reset:
    st.markdown('<span class="reset-tag"></span>', unsafe_allow_html=True)
    if st.button("↺  Empezar de nuevo"):
        for clave in list(st.session_state.keys()):
            if clave.startswith("p_") or clave.startswith("firma_") or clave == "resultado":
                del st.session_state[clave]
        st.rerun()

# =========================================================
# 7. RESULTADO — Hero Card + tarjetas de alternativas
# =========================================================
resultado = st.session_state["resultado"]

if resultado:
    _section("Recomendación")

    if resultado["es_fallback"]:
        st.markdown(
            f"""
            <div class="hero-card hero-warn">
              <div class="glow"></div>
              <span class="kicker">Perfil sin regla exacta</span>
              <h2>{html.escape(resultado["principal"].split(".")[0])}.</h2>
              <p>{".".join(resultado["principal"].split(".")[1:]).strip()}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(
            "Ninguna regla se activó al 100 % con tus respuestas. Abre el "
            "razonamiento para ver qué reglas estuvieron más cerca."
        )
    else:
        # Separa el título de la descripción en el primer punto de la conclusión
        partes = resultado["principal"].split(". ", 1)
        titulo = partes[0] if not partes[0].endswith(".") else partes[0][:-1]
        descripcion = partes[1] if len(partes) > 1 else ""
        st.markdown(
            f"""
            <div class="hero-card">
              <div class="glow"></div>
              <span class="kicker">Recomendación para ti</span>
              <h2>{html.escape(titulo)}</h2>
              <p>{html.escape(descripcion)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if resultado["alternativas"]:
        _section("Otras opciones que también encajan contigo")
        tarjetas = "".join(
            f"""
            <div class="alt-card">
              <div class="alt-num">{numero}</div>
              <div class="alt-txt">{html.escape(opcion)}</div>
            </div>
            """
            for numero, opcion in enumerate(resultado["alternativas"], start=2)
        )
        st.markdown(f'<div class="alt-grid">{tarjetas}</div>', unsafe_allow_html=True)

    # ---- Explicable: qué pasó dentro del motor ----
    with st.expander("🧠 Ver el razonamiento del sistema"):
        ganadora = resultado["ganadora"]
        if ganadora and not resultado["es_fallback"]:
            st.markdown(
                '<div class="trace-title">Regla ganadora</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="rule-line"><b>{ganadora["nombre"]}</b> — '
                f'{len(ganadora["cumplidas"])}/{ganadora["condiciones_totales"]} '
                "condiciones cumplidas</div>",
                unsafe_allow_html=True,
            )
            st.markdown(_chips(ganadora["cumplidas"], "auto"), unsafe_allow_html=True)

        if resultado["activadas"]:
            st.markdown(
                '<div class="trace-title">Otras reglas activadas '
                "(perdieron por especificidad)</div>",
                unsafe_allow_html=True,
            )
            for regla in resultado["activadas"]:
                st.markdown(
                    f'<div class="rule-line">➖ <b>{regla["nombre"]}</b></div>'
                    f'<div class="rule-sub">{html.escape(regla["conclusion"])}</div>',
                    unsafe_allow_html=True,
                )

        if resultado["casi_ganadoras"]:
            st.markdown(
                '<div class="trace-title">Reglas que estuvieron cerca '
                "(lo que faltó)</div>",
                unsafe_allow_html=True,
            )
            for regla in resultado["casi_ganadoras"]:
                st.markdown(
                    f'<div class="rule-line">🔸 <b>{regla["nombre"]}</b> — cumplió '
                    f'{regla["porcentaje"]} %</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    _chips(regla["faltantes"], "chip-miss"), unsafe_allow_html=True
                )

        st.markdown(
            f"""
            <div class="rule-sub" style="margin-top:1rem;">
              Se evaluaron <b>{resultado["reglas_evaluadas"]}</b> reglas contra tus
              hechos. Emparejamiento: igualdad exacta de condiciones (una respuesta
              “Me da igual” satisface cualquier valor de ese atributo); conflicto:
              gana la regla más específica y, en empate, la primera de la base.
            </div>
            """,
            unsafe_allow_html=True,
        )
