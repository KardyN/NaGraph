import pandas as pd

from nagraph.helpers import save_project_with_suffix, open_files_of_types


def steps():
    
    input_paths = open_files_of_types(["xlsx"], 10, True)

    output_path = save_project_with_suffix("cycling", True)

    print("Importing data...")
    df = pd.DataFrame()
    for path in input_paths:
        stem = path.stem
        df = df.append(pd.read_excel(path, sheet_name="Cycle", header=0))
        df = df.append(pd.read_excel(path, sheet_name="Record", header=0))

    print("Import successful")
    return True
    #
    # print("Starting OriginPro...")
    #
    # print("Saving project...")
    # graph.save_fig(str(output_path.with_suffix(".png")))
    # op.save(str(output_path.with_suffix(".opju")))
    # op.exit()
    # return "Saved project at " + (str(output_path.with_suffix(".opju")))    return True


def long():
    return True
