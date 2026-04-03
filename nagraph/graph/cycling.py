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
    print(", ".join([Path(path).stem for path in load_paths]))

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
    df = pd.DataFrame()
    for path in load_paths:
        stem = path.stem
        df = df.append(pd.read_excel(path, sheet_name="Cycle", header=0))
        df = df.append(pd.read_excel(path, sheet_name="Record", header=0))


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