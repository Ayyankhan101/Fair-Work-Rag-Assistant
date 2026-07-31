#!/usr/bin/env python3
"""Branch sync script to keep feature branches up to date with develop.
DEF-048: Sync QA branch with develop.
"""
import subprocess
import sys


def run_cmd(cmd: list) -> tuple:
    """Run a command and return (returncode, stdout, stderr)."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def sync_branch(branch_name: str = "develop") -> int:
    """Sync current branch with develop."""
    print(f"Syncing with {branch_name}...")
    
    # Fetch latest
    rc, stdout, stderr = run_cmd(["git", "fetch", "origin"])
    if rc != 0:
        print(f"Fetch failed: {stderr}")
        return 1
    
    # Check current branch
    rc, stdout, _ = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    current_branch = stdout.strip()
    print(f"Current branch: {current_branch}")
    
    # Stash any local changes
    rc, _, _ = run_cmd(["git", "stash"])
    
    # Merge or rebase
    rc, stdout, stderr = run_cmd(["git", "merge", f"origin/{branch_name}", "--no-edit"])
    if rc != 0:
        print(f"Merge failed: {stderr}")
        print("Resolve conflicts manually, then run: git merge --continue")
        return 1
    
    # Restore stashed changes
    rc, _, _ = run_cmd(["git", "stash", "pop"])
    
    print(f"Synced {current_branch} with {branch_name}")
    return 0


def main() -> int:
    """Main entry point."""
    if len(sys.argv) > 1:
        branch = sys.argv[1]
    else:
        branch = "develop"
    
    return sync_branch(branch)


if __name__ == "__main__":
    raise SystemExit(main())
