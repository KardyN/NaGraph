import re
from pathlib import Path
from tkinter.filedialog import asksaveasfilename, askopenfilenames
from typing import List


def is_jana2006_folder(folder: Path) -> bool:
    return True if folder.is_dir() and len(list(folder.glob("*.prf"))) else False


def open_files_of_types(suffixes: List[str], max_files=1, verbose=False) -> List[Path] | Path:
    if verbose:
        print("Open ", end="")
        for suffix in suffixes:
            print(suffix, end=", ")
        print("files: ", end="")
    loaded_paths = askopenfilenames(
        filetypes=[("All files", ["*." + suffix for suffix in suffixes])] + [(suffix.upper(), "*." + suffix) for suffix in suffixes], title="Open files"
    )
    if not loaded_paths:
        raise Exception("Cancelled file selection")
    if len(loaded_paths) > max_files:
        raise Exception("Too many files chosen")
    loaded_paths = [Path(path) for path in loaded_paths]
    for path in loaded_paths:
        if not path.exists() or not path.is_file():
            raise Exception("Invalid path:" + str(path))
    if verbose:
        print(", ".join([path.stem for path in loaded_paths]))
    return loaded_paths if max_files > 1 else loaded_paths[0]


def save_project_with_suffix(suffix: str, verbose=False) -> Path:
    if verbose:
        print("Save project as ", end="")
    save_path = (
        asksaveasfilename(
            filetypes=[("opju", ".opju")],
            title="Save project as",
            defaultextension=".opju",
            confirmoverwrite=True,
        )
    )
    if not save_path:
        raise Exception("Cancelled save path selection")
    save_path = Path(save_path + "_" + suffix)
    if verbose:
        print(save_path.stem + ".opju")
    return save_path


def assert_file_is_hkl_peaks(file: Path) -> bool:
    pattern = re.compile("^( )*[0-9.]*( )*[0-9.]*( )*$")
    if pattern.match(file.read_text().split("\n")[0]):
        print("THATS A MATCH")
    return True if pattern.match(file.read_text().split("\n")[0]) else False

PATTERNS = [
    ".prf"
]