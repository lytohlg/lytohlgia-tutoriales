#!/usr/bin/env python3
"""Lee la respuesta JSON del router por stdin y la resume en una tabla."""
import json, sys

d = json.load(sys.stdin)
tarea = (sys.argv[1] if len(sys.argv) > 1 else "").strip()
cat = d.get("category") or {}
dif = d.get("difficulty") or {}
print(f"TAREA      {tarea[:64]}")
print(f"PERFIL     {cat.get('label')} ({cat.get('p', 0):.0%}) · dificultad {dif.get('level')}/10")
print(f"{'modelo':<22}{'p(ok)':>7}{'coste $':>10}{'latencia':>10}  origen")
for r in d.get("ranking", []):
    print(f"{r['model_id']:<22}{r['p_success']:>7.2f}{r['est_cost_usd']:>10.6f}"
          f"{r['est_latency_ms']/1000:>8.1f}s  {r['p_source']}")
ch = d.get("choice") or {}
print(f"DECISION   {ch.get('model_id')}  ({ch.get('decided_by')})")
esc = " -> ".join(x["model_id"] for x in d.get("escalation_ladder", []))
print(f"ESCALERA   {esc or '-'}")
fil = d.get("filtered_out") or []
if fil:
    print(f"FILTRADOS  {len(fil)}: " + ", ".join(f"{f['model_id']} ({f['reason']})" for f in fil))
fb = d.get("fallback") or {}
if fb.get("low_confidence"):
    print(f"CONFIANZA  baja: la probabilidad elegida no llega al suelo {fb.get('floor')}")
print(f"TIEMPO     {d['router']['latency_ms']:.1f} ms · trace {d['trace_id']}")
