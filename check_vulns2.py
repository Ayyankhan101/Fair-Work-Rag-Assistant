import subprocess
import json

try:
    result = subprocess.run(
        ['pip-audit', '--format', 'json', '--timeout', '120'],
        capture_output=True, text=True, timeout=180
    )
except subprocess.TimeoutExpired:
    print("pip-audit timed out after 180 seconds")
    exit(1)

if result.returncode != 0:
    print(f"pip-audit failed:\n{result.stderr}")
    exit(1)

data = json.loads(result.stdout)
deps = data.get('dependencies', [])
vulns = [p for p in deps if p.get('vulns')]
no_fix = [p for p in vulns if all(not v.get('fix_versions') for v in p['vulns'])]
has_fix = [p for p in vulns if any(v.get('fix_versions') for v in p['vulns'])]

print(f"Total with vulns: {len(vulns)}")
print(f"Has fix: {len(has_fix)}")
print(f"No fix available: {len(no_fix)}")

print("\n--- Packages WITH a fix ---")
for p in has_fix:
    print(f"  {p['name']} {p['version']}")
    for v in p['vulns']:
        fixes = ', '.join(v.get('fix_versions') or [])
        print(f"    - {v.get('id', 'unknown')} -> upgrade to: {fixes}")

print("\n--- Packages with NO fix ---")
for p in no_fix:
    print(f"  {p['name']} {p['version']}")
    for v in p['vulns']:
        print(f"    - {v.get('id', 'unknown')}: {v.get('description', '')[:120]}")