

try:
    # when executed as module: python -m src.main
    from .menu import run
except Exception:
    # when executed as script: python src/main.py
    from menu import run

if __name__ == "__main__":
    run()
