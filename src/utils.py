# Utilities

def print_header(title):

    print("="*60)
    print(title)
    print("="*60)

def separator():
    print("-"*60)

def file_size(path):
    return round(path.stat().st_size / 1024**2,2)

def check_exists(path):
    if not path.exists():
        raise FileNotFoundError(path)

def create_folder(path):
    path.mkdir(
        parents=True,
        exist_ok=True
    )