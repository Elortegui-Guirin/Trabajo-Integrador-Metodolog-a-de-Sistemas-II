"""Genera el HTML del informe a partir de docs/informe-completo.md."""

import pathlib

import markdown

BASE = pathlib.Path(__file__).parent
ORIGEN = BASE / "informe-completo.md"
DESTINO = BASE / "informe-v3.html"

CSS = """
body {
    font-family: Calibri, Arial, sans-serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #1a1a1a;
    max-width: 17cm;
    margin: 0 auto;
    padding: 2cm 1.5cm;
}
h1 {
    font-size: 26pt;
    text-align: center;
    color: #1f4e79;
    margin-bottom: 0.3cm;
}
h1 + h2 { text-align: center; color: #2e74b5; }
h1 + h2 + h3 { text-align: center; color: #595959; font-weight: normal; }
h2 {
    font-size: 16pt;
    color: #1f4e79;
    margin-top: 0.9cm;
    margin-bottom: 0.3cm;
}
h3 { font-size: 13pt; color: #2e74b5; margin-top: 0.7cm; }
h4 { font-size: 12pt; color: #404040; }
table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.5cm 0;
    font-size: 10.5pt;
}
th, td {
    border: 1px solid #808080;
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
}
th { background: #dce6f1; font-weight: bold; }
tr:nth-child(even) td { background: #f5f8fc; }
code {
    font-family: Consolas, monospace;
    background: #f0f0f0;
    padding: 1px 4px;
    font-size: 10pt;
}
pre {
    background: #f5f5f5;
    border: 1px solid #d0d0d0;
    border-left: 4px solid #2e74b5;
    padding: 10px;
    font-size: 9.5pt;
    overflow-x: auto;
    page-break-inside: avoid;
}
pre code { background: none; padding: 0; }
blockquote {
    border-left: 4px solid #2e74b5;
    margin-left: 0;
    padding: 4px 12px;
    color: #404040;
    background: #f5f8fc;
}
hr { display: none; }
strong { color: #1f4e79; }
"""

texto_md = ORIGEN.read_text(encoding="utf-8")
html_cuerpo = markdown.markdown(texto_md, extensions=["tables", "fenced_code", "toc"])

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>TPI - Metodologia de Sistemas II - Veronica Guirin</title>
<style>{CSS}</style>
</head>
<body>
{html_cuerpo}
</body>
</html>"""

DESTINO.write_text(html, encoding="utf-8")
print("HTML generado:", DESTINO)
print("Tamano:", DESTINO.stat().st_size, "bytes")


