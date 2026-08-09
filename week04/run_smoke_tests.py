import subprocess
import sys
import importlib.util
from pathlib import Path

BASE = Path(__file__).resolve().parent

def run(cmd):
    print(f"Running: {cmd}")
    r = subprocess.run([sys.executable] + cmd.split(), cwd=BASE, capture_output=True, text=True)
    print(r.stdout)
    if r.stderr:
        print(r.stderr)
    return r

def main():
    # 1) Run main.py to populate DB and report
    r = run("main.py")
    if r.returncode != 0:
        raise SystemExit("main.py failed — see output above")

    # 2) Ensure DB exists
    db = BASE / "fintrust_analytics.db"
    if not db.exists():
        raise SystemExit("fintrust_analytics.db not created")

    # 3) Check pandas availability before running analyse.py
    if importlib.util.find_spec("pandas") is None:
        print("Skipping analyse.py: missing dependency 'pandas'.")
        print("To run full smoke tests, install dependencies: python -m pip install -r requirements.txt")
        print("Partial smoke test PASSED: main.py executed and produced report.")
        return

    # 4) Run analyse.py to produce enriched CSV
    r2 = run("analyse.py")
    if r2.returncode != 0:
        raise SystemExit("analyse.py failed — see output above")

    enriched = BASE / "transactions_enriched.csv"
    if not enriched.exists():
        raise SystemExit("transactions_enriched.csv not created")

    print("SMOKE TESTS PASSED: main.py and analyse.py executed and produced outputs.")

if __name__ == '__main__':
    main()
