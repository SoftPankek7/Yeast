from pathlib import Path
import platform
import shutil
import os


def copy_directory(src, dst):
    src_path = Path(src).expanduser().resolve()
    dst_path = Path(dst).expanduser().resolve()

    if not src_path.is_dir():
        raise FileNotFoundError(f"Source directory '{src}' does not exist or is not a directory.")

    for root, _, files in os.walk(src_path):
        root = Path(root)
        rel_path = root.relative_to(src_path)
        target_dir = dst_path / rel_path

        target_dir.mkdir(parents=True, exist_ok=True)

        for file in files:
            src_file = root / file
            dst_file = target_dir / file

            if not dst_file.exists():
                shutil.copy2(src_file, dst_file)
            else:
                print(f"Skipping existing file: {dst_file}")


def get_sublime_packages_path():
    system = platform.system()

    if system == "Windows":
        return Path(os.environ["APPDATA"]) / "Sublime Text" / "Packages"
    elif system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Sublime Text" / "Packages"
    elif system == "Linux":
        return Path.home() / ".config" / "sublime-text" / "Packages"
    else:
        raise RuntimeError("Unsupported OS")


# ---- run ----
packages_path = get_sublime_packages_path()
SCRIPT_DIR = Path(__file__).parent
SOURCE_DIR = SCRIPT_DIR / "yeast-highlight"

copy_directory(SOURCE_DIR, packages_path / "yeast-highlight")