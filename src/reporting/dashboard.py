
from __future__ import annotations
from pathlib import Path

def generate_dashboard(nodes, ranking, comparison, out_path="reports/dashboard.html"):
    out_path = Path(out_path)
    out_path.parent.mkdir(exist_ok=True)
    top = ranking.iloc[0]
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Supply Chain Digital Twin v3</title>
<style>
body{{font-family:Arial,sans-serif;background:#f5f5f5;margin:0;color:#222}}
.header{{background:white;padding:28px 40px;border-bottom:1px solid #ddd}}
.container{{padding:24px 40px}}
.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:22px}}
.card{{background:white;border:1px solid #ddd;border-radius:12px;padding:16px}}
.label{{font-size:12px;text-transform:uppercase;color:#666;letter-spacing:.05em}}
.value{{font-size:24px;font-weight:bold;margin-top:7px}}
.section{{background:white;border:1px solid #ddd;border-radius:12px;padding:20px;margin-bottom:20px}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(320px,1fr));gap:16px}}
img{{width:100%;height:auto;border:1px solid #ddd;border-radius:8px;background:white}}
</style></head>
<body>
<div class="header"><h1>Supply Chain Digital Twin v3</h1><p>Inventory dynamics, lead times, backorders, shocks and near-critical intervention policy.</p></div>
<div class="container">
<div class="cards">
<div class="card"><div class="label">Nodes</div><div class="value">{len(nodes)}</div></div>
<div class="card"><div class="label">Operational Nodes</div><div class="value">{len(nodes[nodes.node_type!='customer_region'])}</div></div>
<div class="card"><div class="label">Critical / Overloaded</div><div class="value">{int(nodes['regime'].isin(['critical','overloaded']).sum())}</div></div>
<div class="card"><div class="label">Top Node</div><div class="value">{top['node_id']}</div></div>
</div>
<div class="section"><h2>Core Recommendation</h2><p>Prioritize <b>{top['node_id']}</b> because it combines near-critical fragility, economic severity and network centrality.</p></div>
<div class="grid">
<div class="section"><h3>Resilience per Dollar</h3><img src="../figures/resilience_per_dollar.png"></div>
<div class="section"><h3>Policy Cost Comparison</h3><img src="../figures/policy_cost_comparison.png"></div>
<div class="section"><h3>Service Level</h3><img src="../figures/service_level_comparison.png"></div>
<div class="section"><h3>Fragility</h3><img src="../figures/fragility.png"></div>
<div class="section"><h3>Network Criticality</h3><img src="../figures/network_criticality.png"></div>
</div></div></body></html>"""
    out_path.write_text(html, encoding="utf-8")
