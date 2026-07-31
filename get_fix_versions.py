import subprocess
import json
from packaging.version import Version

try:
    result = subprocess.run(
        ['pip-audit', '--format', 'json', '--timeout', '120'],
        capture_output=True, text=True, timeout=180
    )
except subprocess.TimeoutExpired:
    print("pip-audit timed out")
    exit(1)

if result.returncode != 0:
    print(f"pip-audit failed: {result.stderr}")
    exit(1)

data = json.loads(result.stdout)
deps = data.get('dependencies', [])
vulns = [p for p in deps if p.get('vulns')]

if not vulns:
    print("No vulnerabilities found.")
    exit(0)

print("Recommended upgrades:")
for p in vulns:
    fix_versions = set()
    for v in p['vulns']:
        for fv in v.get('fix_versions', []):
            fix_versions.add(fv)
    if fix_versions:
        best = sorted(fix_versions, key=Version)[-1]  # correct version sort
        print(f"  {p['name']}=={p['version']} -> {best}")
    else:
        print(f"  {p['name']}=={p['version']} -> no fix available yet")