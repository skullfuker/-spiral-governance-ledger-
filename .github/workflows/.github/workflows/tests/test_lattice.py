import runpy
from pathlib import Path

def test_script_entrypoint(capsys):
    module_path = Path(__file__).resolve().parents[1] / "lattice_ledger.py"
    runpy.run_path(str(module_path), run_name="__main__")

    output = capsys.readouterr().out
    assert "New Update Block Initialized Successfully:" in output
    assert "Second Update Block Initialized Successfully:" in output
    assert "Chain Integrity Check: ✓ VALID" in output