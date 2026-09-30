#!/usr/bin/env python3
"""Converte palavras da transcrição (tempo de mídia) em tempo de timeline.

uso: mapa_palavras.py transcricao.json mapa.json [--clipe NOME]
  transcricao.json: qualquer JSON com objetos {t0, t1?, w|texto|palavra|text}
  mapa.json: [{"inicio": s_timeline, "in": s_midia, "dur": s}]  (um por clipe da V1)
Saída: "tempo_timeline  palavra", uma por linha (só palavras que estão na timeline).
"""
import json, sys

def palavras(o):
    if isinstance(o, dict):
        if "t0" in o and any(k in o for k in ("w", "texto", "palavra", "text")):
            yield o
        for v in o.values():
            yield from palavras(v)
    elif isinstance(o, list):
        for v in o:
            yield from palavras(v)

trans = json.load(open(sys.argv[1]))
mapa = json.load(open(sys.argv[2]))
for w in palavras(trans):
    t = w["t0"]; txt = w.get("w") or w.get("texto") or w.get("palavra") or w.get("text")
    for c in mapa:
        if c["in"] <= t < c["in"] + c["dur"]:
            print(f"{c['inicio'] + t - c['in']:8.3f}  {txt}")
