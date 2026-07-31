#!/usr/bin/env python3
"""Dependency validation script.
DEF-029: Identify and reject invalid transitive version specifiers.
DEF-042: Validate pinned versions.
"""
from pathlib import Path


def validate_requirements(req_path: str) -> list:
    """Validate requirements.txt for issues."""
    issues = []
    
    with open(req_path) as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # DEF-029: Check for invalid version specifiers
        # Invalid: >=3.6.* (transitive wildcard)
        if '>=' in line and '.*' in line:
            issues.append({
                "line": i,
                "package": line,
                "issue": "Invalid transitive version specifier with wildcard",
                "severity": "HIGH",
            })
        
        # Check for unpinned packages (no version constraint)
        if not any(c in line for c in ['>=', '<=', '==', '!=', '~=']):
            issues.append({
                "line": i,
                "package": line,
                "issue": "Unpinned dependency (no version constraint)",
                "severity": "MEDIUM",
            })
        
        # Check for exact version pins (should use ranges for flexibility)
        if '==' in line:
            issues.append({
                "line": i,
                "package": line,
                "issue": "Exact version pin (consider using range)",
                "severity": "LOW",
            })
    
    return issues


def main() -> int:
    """Validate requirements.txt."""
    req_path = Path(__file__).resolve().parents[1] / "requirements.txt"
    
    if not req_path.exists():
        print(f"requirements.txt not found at {req_path}")
        return 1
    
    print(f"Validating {req_path}...")
    issues = validate_requirements(str(req_path))
    
    if issues:
        print(f"\nFound {len(issues)} issues:")
        for issue in issues:
            print(f"  Line {issue['line']}: [{issue['severity']}] {issue['package']}")
            print(f"    Issue: {issue['issue']}")
    else:
        print("No issues found.")
    
    return 1 if any(i['severity'] == 'HIGH' for i in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
