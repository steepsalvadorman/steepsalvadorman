#!/usr/bin/env python3
"""Generates the cyberpunk SVG assets used by README.md / README.es.md.

Edit the data below (projects, sections, taglines) and run:

    python3 scripts/generate_assets.py

Everything is written to ./assets. The SVGs are self-contained (no external
fonts, scripts or images) so GitHub can render them inside the README.
"""
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# ── palette ──────────────────────────────────────────────────────────────
BG0 = "#07060f"
BG1 = "#0d0221"
CYAN = "#00f0ff"
MAGENTA = "#ff2a6d"
YELLOW = "#fcee0a"
GREEN = "#05ffa1"
VIOLET = "#b967ff"
TEXT = "#e6f1ff"
MUTED = "#8b93b5"

MONO = "ui-monospace,SFMono-Regular,'JetBrains Mono','Fira Code',Menlo,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace"
DISPLAY = "'Segoe UI','Helvetica Neue',Helvetica,Arial,'Liberation Sans',sans-serif"

REDUCED_MOTION = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"

# ── content ──────────────────────────────────────────────────────────────
HEADER = {
    "en": {
        "role": "SYSTEMS ENGINEER // FULL STACK & BACKEND DEVELOPER",
        "typed": "> building reliable software for industrial ops, labs & real-time systems",
        "label": "Steep Salvador — Systems Engineer, Full Stack & Backend Developer — Lima, Peru",
    },
    "es": {
        "role": "INGENIERO DE SISTEMAS // DESARROLLADOR FULL STACK Y BACKEND",
        "typed": "> software confiable para operaciones industriales, laboratorios y tiempo real",
        "label": "Steep Salvador — Ingeniero de Sistemas, Desarrollador Full Stack y Backend — Lima, Perú",
    },
}

# (slug, right-hand tag, english title, spanish title)
SECTIONS = [
    ("profile", "SYS.PROFILE", "Professional profile", "Perfil profesional"),
    ("experience", "LOG.EXPERIENCE", "Experience highlights", "Experiencia destacada"),
    ("projects", "DATA.PROJECTS", "Featured projects", "Proyectos destacados"),
    ("toolkit", "LOADOUT", "Core toolkit", "Herramientas principales"),
    ("direction", "VECTOR.NEXT", "Current direction", "Enfoque actual"),
    ("education", "ARCHIVE.EDU", "Education", "Formación"),
    ("contact", "COMMS.OPEN", "Contact", "Contacto"),
]

# (slug, name, stack, english focus, spanish focus)
PROJECTS = [
    ("daibot", "DaiBot", ["Rust", "Axum", "PostgreSQL", "Docker"],
     "Multi-tenant streaming bot: OAuth 2.0 PKCE, EventSub webhooks, WebSockets, TTS, OBS overlay and 43 unit tests.",
     "Bot de streaming multi-tenant: OAuth 2.0 PKCE, webhooks EventSub, WebSockets, TTS, overlay para OBS y 43 pruebas unitarias."),
    ("miningsmartscale", "MiningSmartScale", ["Rust"],
     "Smart-scale integration and data capture for mining operations.",
     "Integración de balanzas inteligentes y captura de datos para operaciones mineras."),
    ("newposture-detector", "newposture_detector", ["Python", "MediaPipe"],
     "Real-time posture detection from video.",
     "Detección de postura en tiempo real a partir de video."),
    ("microservices-java", "microservices_java", ["Java", "Spring Boot"],
     "Microservice architecture and distributed backend experiments.",
     "Arquitectura de microservicios y experimentos de backend distribuido."),
    ("spring-security-complete", "spring-security-complete", ["Java", "Spring Security"],
     "Authentication and authorization patterns for Spring applications.",
     "Patrones de autenticación y autorización para aplicaciones Spring."),
    ("portfolio", "Portfolio", ["Astro"],
     "Personal portfolio and professional presence.",
     "Portafolio personal y presencia profesional."),
    ("steepskynetdotfiles", "steepskynetdotfiles", ["Shell", "JavaScript"],
     "Reproducible Arch Linux and Hyprland development environment.",
     "Entorno reproducible de desarrollo con Arch Linux y Hyprland."),
    ("all-repositories", "ALL REPOSITORIES", ["github.com/steepsalvadorman"],
     "Browse everything else: experiments, tooling and work in progress.",
     "Explora todo lo demás: experimentos, herramientas y trabajo en curso."),
]
ACCENTS = [CYAN, MAGENTA, YELLOW, GREEN]


def svg(w, h, label, body, css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{escape(label, {chr(34): "&quot;"})}">\n'
        f"<title>{escape(label)}</title>\n<style>{css}{REDUCED_MOTION}</style>\n{body}\n</svg>\n"
    )


# ── header ───────────────────────────────────────────────────────────────
def header(lang):
    c = HEADER[lang]
    W, H = 840, 330
    hy = 238  # horizon
    frame = f"22,2 {W-2},2 {W-2},{H-22} {W-22},{H-2} 2,{H-2} 2,22"

    rays = "".join(
        f'<line x1="420" y1="{hy}" x2="{x}" y2="{H}"/>' for x in range(-560, 1401, 98)
    )
    n = 7
    ys = [hy + (H - hy) * (i / n) ** 2 for i in range(n + 1)]
    floor = "".join(
        f'<line x1="0" x2="{W}" y1="{ys[i]:.1f}" y2="{ys[i]:.1f}">'
        f'<animate attributeName="y1" values="{ys[i]:.1f};{ys[i+1]:.1f}" dur="1.4s" repeatCount="indefinite"/>'
        f'<animate attributeName="y2" values="{ys[i]:.1f};{ys[i+1]:.1f}" dur="1.4s" repeatCount="indefinite"/></line>'
        for i in range(n)
    )

    typed = c["typed"]
    tw = round(len(typed) * 7.9)
    tx = (W - tw) / 2
    steps = len(typed)
    t_type, t_hold = 0.34, 0.92
    kt = [round(t_type * i / steps, 4) for i in range(steps + 1)] + [t_hold, 1]
    widths = [round(tw * i / steps, 1) for i in range(steps + 1)] + [0, 0]
    kt_s = ";".join(map(str, kt))
    w_s = ";".join(map(str, widths))
    cur_s = ";".join(str(round(tx + w + 3, 1)) for w in widths)

    bars = "".join(
        f'<rect x="{30 + i * 5}" y="{H - 44}" width="{2 if i % 3 else 3}" height="{10 + (i * 7) % 12}"/>'
        for i in range(14)
    )

    name = (
        f'<text x="420" y="150" text-anchor="middle" textLength="640" lengthAdjust="spacingAndGlyphs" '
        f'font-family="{DISPLAY}" font-size="80" font-weight="900">STEEP SALVADOR</text>'
    )

    css = f"""
.mono{{font-family:{MONO}}}
.gc{{animation:gc 4.5s steps(1) infinite}}
.gm{{animation:gm 4.5s steps(1) infinite}}
.sl{{animation:sl 4.5s steps(1) infinite}}
.blink{{animation:blink 1.1s steps(1) infinite}}
.dot{{animation:blink 1.8s steps(1) infinite}}
.scan{{animation:scan 6s linear infinite}}
.flick{{animation:flick 7s steps(1) infinite}}
@keyframes gc{{0%,100%{{transform:translate(-3px,0)}}86%{{transform:translate(-11px,2px)}}88%{{transform:translate(7px,-2px)}}90%{{transform:translate(-5px,1px)}}92%{{transform:translate(-3px,0)}}}}
@keyframes gm{{0%,100%{{transform:translate(3px,0)}}86%{{transform:translate(10px,-2px)}}88%{{transform:translate(-8px,2px)}}90%{{transform:translate(6px,-1px)}}92%{{transform:translate(3px,0)}}}}
@keyframes sl{{0%,100%{{opacity:0}}86%{{opacity:1;transform:translate(18px,0)}}88%{{opacity:1;transform:translate(-22px,0)}}90%{{opacity:1;transform:translate(9px,0)}}92%{{opacity:0}}}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0}}}}
@keyframes scan{{0%{{transform:translateY(-40px)}}100%{{transform:translateY({H + 40}px)}}}}
@keyframes flick{{0%,100%{{opacity:1}}47%{{opacity:.55}}48%{{opacity:1}}50%{{opacity:.7}}51%{{opacity:1}}}}
"""
    body = f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
<linearGradient id="neon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAGENTA}"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG1}" stop-opacity="0"/></linearGradient>
<linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".1"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{MAGENTA}" stop-opacity=".34"/><stop offset=".6" stop-color="#7a04eb" stop-opacity=".12"/><stop offset="1" stop-color="{BG0}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="{CYAN}" stroke-opacity=".06"/></pattern>
<pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" fill-opacity=".28"/></pattern>
<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="frame"><polygon points="{frame}"/></clipPath>
<clipPath id="slice"><rect x="0" y="104" width="{W}" height="16"/><rect x="0" y="134" width="{W}" height="9"/></clipPath>
<clipPath id="type"><rect x="{tx:.1f}" y="196" height="24" width="{tw}"><animate attributeName="width" calcMode="discrete" dur="10s" repeatCount="indefinite" keyTimes="{kt_s}" values="{w_s}"/></rect></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{hy}" fill="url(#grid)"/>
<ellipse cx="420" cy="130" rx="400" ry="140" fill="url(#halo)"/>
<g stroke="{MAGENTA}" stroke-opacity=".55" stroke-width="1">{rays}{floor}</g>
<rect y="{hy}" width="{W}" height="46" fill="url(#fade)"/>
<line x1="0" x2="{W}" y1="{hy}" y2="{hy}" stroke="url(#neon)" stroke-width="1.5" filter="url(#glow)"/>

<g class="mono" font-size="11" letter-spacing="2">
<text x="30" y="34" fill="{CYAN}">◢ NET://STEEP.SALVADOR</text>
<text x="{W-48}" y="34" text-anchor="end" fill="{TEXT}">SYS.STATUS <tspan fill="{GREEN}">ONLINE</tspan></text>
<circle class="dot" cx="{W-34}" cy="30" r="4" fill="{GREEN}" filter="url(#glow)"/>
<text x="110" y="{H-24}" fill="{YELLOW}" stroke="{BG1}" stroke-width="4" paint-order="stroke">ID STEEP-01</text>
<text x="{W-48}" y="{H-24}" text-anchor="end" fill="{YELLOW}" stroke="{BG1}" stroke-width="4" paint-order="stroke">12.0464°S 77.0428°W // LIMA.PE</text>
</g>
<g fill="{YELLOW}">{bars}</g>
<path d="M30 46H190M{W-30} 46H{W-250}" stroke="{CYAN}" stroke-opacity=".5"/>

<g transform="skewX(-8) translate(21,0)" class="flick">
<g class="gc" fill="{CYAN}" opacity=".9">{name}</g>
<g class="gm" fill="{MAGENTA}" opacity=".9">{name}</g>
<g fill="#fff" filter="url(#glow)">{name}</g>
<g clip-path="url(#slice)"><g class="sl" fill="{CYAN}">{name}</g></g>
</g>

<text class="mono" x="420" y="186" text-anchor="middle" font-size="13.5" font-weight="700" letter-spacing="2" fill="{CYAN}">{escape(c["role"])}</text>
<g clip-path="url(#type)"><text class="mono" x="{tx:.1f}" y="213" font-size="13" textLength="{tw}" lengthAdjust="spacingAndGlyphs" fill="{TEXT}">{escape(typed)}</text></g>
<rect class="blink" y="201" width="8" height="15" fill="{MAGENTA}"><animate attributeName="x" calcMode="discrete" dur="10s" repeatCount="indefinite" keyTimes="{kt_s}" values="{cur_s}"/></rect>

<rect width="{W}" height="{H}" fill="url(#lines)"/>
<rect class="scan" width="{W}" height="40" fill="url(#band)"/>
</g>
<polygon points="{frame}" fill="none" stroke="url(#neon)" stroke-width="2"/>
<path d="M2 22 22 2H70M{W-2} {H-22} {W-22} {H-2}H{W-70}" fill="none" stroke="{YELLOW}" stroke-width="4"/>"""
    return svg(W, H, c["label"], body, css)


# ── section headers ──────────────────────────────────────────────────────
def section(idx, tag, title):
    W, H = 840, 58
    frame = f"0,0 {W-16},0 {W},16 {W},{H} 16,{H} 0,{H-16}"
    css = f"""
.p{{animation:p 3.6s linear infinite}}
@keyframes p{{0%{{transform:translateX(-140px)}}100%{{transform:translateX({W}px)}}}}
"""
    body = f"""<defs>
<linearGradient id="n" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".6" stop-color="{MAGENTA}"/><stop offset="1" stop-color="{MAGENTA}" stop-opacity="0"/></linearGradient>
<linearGradient id="pl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
<pattern id="l" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" fill-opacity=".25"/></pattern>
<clipPath id="f"><polygon points="{frame}"/></clipPath>
</defs>
<g clip-path="url(#f)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<polygon points="0,0 74,0 58,{H} 0,{H}" fill="{YELLOW}"/>
<text x="31" y="38" text-anchor="middle" font-family="{MONO}" font-size="24" font-weight="800" fill="{BG0}">{idx:02d}</text>
<path d="M82 0 66 {H}M90 0 74 {H}" stroke="{YELLOW}" stroke-width="3"/>
<text x="108" y="37" font-family="{DISPLAY}" font-size="23" font-weight="800" letter-spacing="3.5" fill="{TEXT}">{escape(title.upper())}</text>
<text x="{W-26}" y="35" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{MAGENTA}">// {escape(tag)}</text>
<rect x="60" y="{H-3}" width="{W}" height="3" fill="url(#n)"/>
<rect class="p" y="{H-3}" width="140" height="3" fill="url(#pl)"/>
<rect width="{W}" height="{H}" fill="url(#l)"/>
</g>"""
    return svg(W, H, title, body, css)


# ── project cards ────────────────────────────────────────────────────────
def card(idx, name, stack, focus, accent, lang, is_all):
    W, H = 410, 200
    frame = f"1,1 {W-21},1 {W-1},21 {W-1},{H-1} 21,{H-1} 1,{H-21}"
    lines = wrap(focus, 50)[:4]
    desc = "".join(
        f'<text x="24" y="{98 + i * 17}" font-size="11.5" fill="{TEXT}" fill-opacity=".86">{escape(l)}</text>'
        for i, l in enumerate(lines)
    )
    chips, x = "", 24
    for s in stack:
        tl = round(len(s) * 6.4)
        w = tl + 18
        chips += (
            f'<rect x="{x}" y="{H-42}" width="{w}" height="20" fill="{accent}" fill-opacity=".12" stroke="{accent}" stroke-opacity=".8"/>'
            f'<text x="{x + 9}" y="{H-28}" font-size="10.5" font-weight="700" textLength="{tl}" lengthAdjust="spacingAndGlyphs" fill="{accent}">{escape(s)}</text>'
        )
        x += w + 8
    code = "IDX_ALL" if is_all else f"PRJ_{idx:02d}"
    cta = {"en": "OPEN REPO ↗", "es": "VER REPO ↗"}[lang] if not is_all else {"en": "BROWSE ↗", "es": "EXPLORAR ↗"}[lang]
    if is_all and lang == "es":
        name = "TODOS LOS REPOSITORIOS"
    nsize = 22 if len(name) <= 22 else 19
    css = f"""
text{{font-family:{MONO}}}
.s{{animation:s 4s linear infinite;animation-delay:-{idx * 0.55:.2f}s}}
@keyframes s{{0%{{transform:translateX(-120px)}}60%,100%{{transform:translateX({W}px)}}}}
"""
    body = f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{accent}" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>
<radialGradient id="h" cx="1" cy="0" r="1"><stop offset="0" stop-color="{accent}" stop-opacity=".22"/><stop offset=".7" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="{accent}" stroke-opacity=".06"/></pattern>
<pattern id="l" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" fill-opacity=".22"/></pattern>
<filter id="gl" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="f"><polygon points="{frame}"/></clipPath>
</defs>
<g clip-path="url(#f)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#g)"/>
<rect width="{W}" height="{H}" fill="url(#h)"/>
<rect x="24" y="22" width="{len(code) * 7 + 14}" height="18" fill="{accent}"/>
<text x="31" y="35" font-size="11" font-weight="800" fill="{BG0}">{code}</text>
<text x="{W-34}" y="35" text-anchor="end" font-size="10.5" letter-spacing="1.5" fill="{accent}">{cta}</text>
<text x="24" y="70" font-size="{nsize}" font-weight="800" fill="#fff" filter="url(#gl)">{escape(name)}</text>
<rect x="24" y="78" width="46" height="2" fill="{accent}"/>
{desc}
{chips}
<rect width="{W}" height="{H}" fill="url(#l)"/>
<rect class="s" y="1" width="120" height="2" fill="url(#sw)"/>
</g>
<polygon points="{frame}" fill="none" stroke="{accent}" stroke-opacity=".75" stroke-width="1.5"/>
<path d="M{W-1} {H-34}V{H-1}H{W-34}" fill="none" stroke="{accent}" stroke-width="3"/>"""
    return svg(W, H, f"{name} — {focus} [{' · '.join(stack)}]", body, css)


# ── footer ───────────────────────────────────────────────────────────────
def footer():
    W, H = 840, 70
    eq = "".join(
        f'<rect x="{30 + i * 9}" y="20" width="5" height="30" transform-origin="{32 + i * 9}px 35px" '
        f'style="animation:e {0.7 + (i * 37 % 9) / 10:.1f}s ease-in-out {-(i * 0.13):.2f}s infinite alternate"/>'
        for i in range(12)
    )
    # mirror the equaliser on the right-hand side
    eq_right = f'<g transform="translate({W},0) scale(-1,1)">{eq}</g>'
    css = "@keyframes e{0%{transform:scaleY(.15)}100%{transform:scaleY(1)}}.b{animation:b 1.2s steps(1) infinite}@keyframes b{0%,100%{opacity:1}50%{opacity:0}}"
    frame = f"16,1 {W-1},1 {W-1},{H-17} {W-17},{H-1} 1,{H-1} 1,17"
    body = f"""<defs>
<linearGradient id="n" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAGENTA}"/></linearGradient>
<pattern id="l" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" fill-opacity=".25"/></pattern>
<clipPath id="f"><polygon points="{frame}"/></clipPath>
</defs>
<g clip-path="url(#f)">
<rect width="{W}" height="{H}" fill="{BG1}"/>
<g fill="{CYAN}">{eq}</g><g fill="{MAGENTA}">{eq_right}</g>
<text x="420" y="32" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="4" fill="{TEXT}">STEEP.SALVADOR <tspan fill="{MAGENTA}">//</tspan> LIMA.PE</text>
<text x="420" y="52" text-anchor="middle" font-family="{MONO}" font-size="10.5" letter-spacing="3" fill="{YELLOW}">END OF TRANSMISSION <tspan class="b">█</tspan></text>
<rect width="{W}" height="{H}" fill="url(#l)"/>
</g>
<polygon points="{frame}" fill="none" stroke="url(#n)" stroke-width="1.5"/>"""
    return svg(W, H, "Steep Salvador — Lima, Peru", body, css)


def main():
    for lang in ("en", "es"):
        d = OUT / lang
        (d / "projects").mkdir(parents=True, exist_ok=True)
        (d / "header.svg").write_text(header(lang), encoding="utf-8")
        for i, (slug, tag, en, es) in enumerate(SECTIONS, 1):
            (d / f"section-{i:02d}-{slug}.svg").write_text(
                section(i, tag, en if lang == "en" else es), encoding="utf-8")
        for i, (slug, name, stack, en, es) in enumerate(PROJECTS, 1):
            (d / "projects" / f"{i:02d}-{slug}.svg").write_text(
                card(i, name, stack, en if lang == "en" else es,
                     ACCENTS[(i - 1) % len(ACCENTS)], lang, slug == "all-repositories"),
                encoding="utf-8")
    (OUT / "footer.svg").write_text(footer(), encoding="utf-8")
    print(f"assets written to {OUT}")


if __name__ == "__main__":
    main()
