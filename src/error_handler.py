import sys

def handle_error(exception):
    print(f"ERROR: {exception}", file=sys.stderr)
    sys.exit(2)
