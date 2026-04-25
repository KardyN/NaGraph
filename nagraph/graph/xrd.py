from tkinter.filedialog import askopenfilenames, asksaveasfilename
import originpro as op
from pathlib import Path
import pandas as pd


def xrd() -> str:

    print("Open XRD files: ", end="")
    load_paths = askopenfilenames(filetypes=[("xyd", "*.xyd")], title="Open XRD files")
    if not load_paths:
        return "Cancelled"
    load_paths = [Path(path) for path in load_paths]
    for path in load_paths:
        if not path.exists() or not path.is_file():
            return "Invalid file path: " + str(path)
    print(", ".join([path.stem for path in load_paths]))

    print("Save project as ", end="")
    save_path = asksaveasfilename(
        filetypes=[("opju", ".opju")],
        title="Save project as",
        defaultextension=".opju",
        confirmoverwrite=True,
    )
    if not save_path:
        return "Cancelled"
    save_path = Path(save_path)
    print(save_path.stem + ".opju")

    print("Importing data...")
    df = pd.DataFrame()
    i = 0
    for path in load_paths:
        data = path.read_text()[:-1]  # Avg. xrd file size - 320kB
        th_vals = []
        i_vals = []
        for line in data.split("\n"):
            x, y = line.strip().split()
            th_vals.append(float(x))
            i_vals.append(float(y))
        i_vals_max = max(i_vals)
        i_vals = [val / i_vals_max + i * 0.1 for val in i_vals]
        df = pd.concat(
            [
                df,
                pd.DataFrame(th_vals, columns=["2θ"]),
                pd.DataFrame(i_vals, columns=[path.stem]),
            ],
            axis=1,
        )
        i += 1
    df = df.loc[:, ~df.columns.duplicated()].copy()
    min_x, max_x = df["2θ"].min(), df["2θ"].max()
    min_y, max_y = round(min(df.iloc[:, 1:].min()), 3) - 0.045, 1.045 + i * 0.1
    print("Import successful")

    print("Starting OriginPro...")
    op.set_show()
    worksheet = op.new_sheet("w", "XRD")
    worksheet.from_df(df)
    graph = op.new_graph()
    graph.set_int("aa", 1)
    layer_1 = graph[0]
    for column in range(1, worksheet.cols):
        layer_1.add_plot(worksheet, column, 0)
    layer_1.xlim = (min_x, max_x, 10)
    layer_1.ylim = (min_y, max_y)
    layer_1.group()  # doesn't work for single plot
    layer_1.plot_list()[0].colormap = "Fire"  # doesn't work for single plot
    layer_1.plot_list()[0].set_int("line.width", 1)
    layer_1.axis("x").title = "2Θ, [deg.]"
    layer_1.axis("y").title = "I, [r.u.]"
    layer_1.set_int("x.opposite", 1)
    layer_1.set_int("y.opposite", 1)
    layer_1.set_int("x.ticks", 5)
    layer_1.set_int("y.ticks", 0)
    layer_1.set_int("y.showlabel", 0)
    legend = layer_1.label("Legend")
    xto = layer_1.get_float("x.to")
    yto = layer_1.get_float("y.to")
    legend.set_int("showframe", 0)
    legend.set_float("x", xto - legend.get_float("dx") / 2)
    legend.set_float("y", yto - legend.get_float("dy") / 2)

    print("Saving project...")
    graph.save_fig(str(save_path.with_suffix(".png")))
    op.save(str(save_path.with_suffix(".opju")))
    op.exit()
    return "Saved project at " + (str(save_path.with_suffix(".opju")))
