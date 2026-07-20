import re
from functools import cache, wraps
from pathlib import Path
from threading import Thread
from tkinter.filedialog import asksaveasfilename, askopenfilenames
from typing import List


@cache
def is_jana2006_folder(folder: Path) -> bool:
    return True if folder.is_dir() and len(list(folder.glob("*.prf"))) else False


def open_files_of_types(
    suffixes: List[str], max_files: int = 0, verbose: bool = False
) -> List[Path]:
    if verbose:
        print("Open ", end="")
        for suffix in suffixes:
            print(suffix, end=", ")
        print("etc files: ", end="")
    loaded_paths = askopenfilenames(
        filetypes=[("All files", ["*." + suffix for suffix in suffixes])]
        + [(suffix.upper(), "*." + suffix) for suffix in suffixes],
        title="Open files",
    )
    if not loaded_paths:
        raise Exception("Cancelled file selection")
    if (not max_files) and len(loaded_paths) > max_files:
        raise Exception("Too many files chosen")
    loaded_paths = [Path(path) for path in loaded_paths]
    for path in loaded_paths:
        if not path.exists() or not path.is_file():
            raise Exception("Invalid path:" + str(path))
    if verbose:
        print(", ".join([path.stem for path in loaded_paths]))
    return loaded_paths


def save_project_with_suffix(suffix: str, verbose=False) -> Path:
    if verbose:
        print("Save project as ", end="")
    save_path = asksaveasfilename(
        filetypes=[("opju", ".opju")],
        title="Save project as",
        defaultextension=".opju",
        confirmoverwrite=True,
    )
    if not save_path:
        raise Exception("Cancelled save path selection")
    save_path = Path(save_path + "_" + suffix)
    if verbose:
        print(save_path.stem + ".opju")
    return save_path


def match_file_type_list(file: Path, pattern_ids: list[str]) -> str | None:
    for pattern_id in pattern_ids:
        if match_file_type(file, pattern_id):
            return pattern_id
    return None


def match_file_type(file: Path, pattern_id: str) -> bool:
    pattern = re.compile(PATTERNS[pattern_id])
    return True if pattern.match(file.read_text().split("\n")[0]) else None


PATTERNS = {
    "*.prf": "^(( )+[0-9]){5}$",
    "*.inp": "^'Input file for Simple Rietveld or Pawley refinement$",
    "2Th_I.txt": "^(( )+[0-9.]+){2}$",
    "data.txt": "^'y-axis saved as y$",
    "*.cif": "^\n$",
    "*.xyd": "^(( )+[0-9.]+){2}$",
}


def threaded(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_thread = Thread(target=func, args=args, kwargs=kwargs)
        func_thread.daemon = True
        func_thread.start()
        return func_thread
    return wrapper
