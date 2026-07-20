import re
from pathlib import Path
from tkinter.filedialog import asksaveasfilename, askopenfilenames

from util.deco import debug


def is_jana2006_folder(folder: Path) -> bool:
    return True if folder.is_dir() and list(folder.glob("*.prf")) else False


def get_last_word(line):
    return line.split()[-1]


def format_uncertain_float(unformatted: str) -> str:
    if match_text_type(unformatted, "precise_float"):
        return unformatted
    elif match_text_type(unformatted, "space_group"):
        return unformatted.strip("\'")
    elif match_text_type(unformatted, ".inp_uncertain_float"):
        number, significant = unformatted.split("`_")
        return unformatted
    elif match_text_type(unformatted, ".cif_uncertain_float"):
        number, significant = unformatted[:-1].split("(")
        significant = int(significant)
        if 9 < significant < 100:
            number = round(float(number), len(number.split('.')[1]) - 1)
            significant = int(round(significant, -1) / 10)
        elif 99 < int(significant) < 1:
            raise Exception("Invalid uncertainty type: >>" + unformatted + "<<")
        return "{}({})".format(number, significant)
    else:
        raise Exception("Invalid uncertainty type: >>" + unformatted + "<<")


def open_files_of_types(
    suffixes: list[str], max_files: int = 0, verbose: bool = False
) -> list[Path]:
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

def match_text_type_list(text: str, pattern_ids: list[str]) -> str | None:
    for pattern_id in pattern_ids:
        if match_text_type(text, pattern_id):
            return pattern_id
    return None


@debug()
def match_file_type(file: Path, pattern_id: str) -> bool:
    pattern = re.compile(PATTERNS[pattern_id])
    return True if pattern.match(file.read_text().split("\n")[0]) else None


@debug()
def match_text_type(text: str, pattern_id: str) -> bool:
    pattern = re.compile(PATTERNS[pattern_id])
    return True if pattern.match(text.split("\n")[0]) else None


PATTERNS = {
    "*.prf": r"^(( )+[0-9]){5}$",
    "*.inp": r"^'Input file for Simple Rietveld or Pawley refinement$",
    "2Th_I.txt": r"^(( )+[0-9.]+){2}$",
    "data.txt": r"^'y-axis saved as y$",
    "*.cif": r"^\n$",
    "*.xyd": r"^(( )+[0-9.]+){2}$",
    "precise_float": r"^[0-9.]+$",
    ".inp_uncertain_float": r"^[0-9.]+`_[0-9.]+$",
    ".cif_uncertain_float": r"^[0-9.]+\([0-9]+\)$",
    "space_group": r"^[a-zA-Z0-9-]+$",
}
