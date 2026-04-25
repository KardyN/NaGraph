import re
import warnings
from tkinter.filedialog import askopenfilenames, asksaveasfilename
from pathlib import Path
import pandas as pd
import originpro as op


def steps():
    print("Open cycling files: ", end="")
    load_paths = askopenfilenames(filetypes=[("XLSX", "*.xlsx")], title="Open cycling files")
    if not load_paths:
        return "Cancelled"
    load_paths = [Path(path) for path in load_paths]
    for path in load_paths:
        if not path.exists() or not path.is_file():
            return "Invalid file path: " + str(path)
    print(", ".join([path.stem for path in load_paths]))

    # print("Save project as ", end="")
    # save_path = asksaveasfilename(
    #     filetypes=[("opju", ".opju")],
    #     title="Save project as",
    #     defaultextension=".opju",
    #     confirmoverwrite=True,
    # )
    # if not save_path:
    #     return "Cancelled"
    # save_path = Path(save_path)
    # print(save_path.stem + ".opju")

    print("Importing data...")
    cycle_df = pd.DataFrame()
    record_df = pd.DataFrame()
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, module=re.escape('openpyxl.styles.stylesheet'))
        for path in load_paths:
            try:
                cycle_df = pd.concat([cycle_df, pd.read_excel(path, sheet_name="Cycle", header=0, verbose=True)])
            except ValueError:
                pass
            try:
                record_df = pd.concat([record_df, pd.read_excel(path, sheet_name="Record", header=0, verbose=True)])
            except ValueError:
                pass
    print(cycle_df.head())
    print(record_df.head())


    print("Import successful")
    return True
    #
    # print("Starting OriginPro...")
    #
    # print("Saving project...")
    # graph.save_fig(str(save_path.with_suffix(".png")))
    # op.save(str(save_path.with_suffix(".opju")))
    # op.exit()
    # return "Saved project at " + (str(save_path.with_suffix(".opju")))    return True

def long():
    return True