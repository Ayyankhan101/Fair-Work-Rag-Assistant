import json

with open("pip_audit_results.json", "r", encoding="utf-8-sig") as f:
    data = json.load(f)

deps = data.get("dependencies", [])
vulns = [p for p in deps if p.get("vulns")]

print(f"Total deps: {len(deps)}")
print(f"Deps with vulns: {len(vulns)}")

for p in vulns:
    print(f"  {p['name']} {p['version']}: {len(p['vulns'])} vulns")
    for v in p["vulns"]:
        fix = ', '.join(v.get('fix_versions') or ['no fix available'])
        print(f"    - {v.get('id', 'unknown')}: {v.get('description', '')[:120]}")
        print(f"      fix: {fix}")