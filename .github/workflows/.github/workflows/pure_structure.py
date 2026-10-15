import subprocess

def deploy_lattice_pipeline():
    """Stages the core structural layer, CI workflow, and test suite, then pushes to GitHub."""
    commands = [
        ["git", "add", "pure_structure.py", ".github/workflows/lattice_ci.yml", "tests/test_lattice.py"],
        ["git", "commit", "-m", "feat(lattice): integrate PureStructuralLayer CI pipeline and test suite [provenance: true, gate: E>0]"],
        ["git", "push", "origin", "main"]
    ]
    
    for cmd in commands:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Execution error on {' '.join(cmd)}: {result.stderr.strip()}")
            return False
        print(f"Success: {' '.join(cmd)}")
    
    print("Repository workflow successfully synchronized and deployed.")
    return True

if __name__ == "__main__":
    deploy_lattice_pipeline()
