from tkinter.filedialog import askopenfilenames, asksaveasfilename, askopenfilename
import originpro as op
from pathlib import Path
import pandas as pd


def rietveld() -> str:

    print("Open .prf file: ", end="")
    load_path = askopenfilename(filetypes=[("prf", "*.prf")], title="Open .prf file")
    if not load_path:
        return "Cancelled"
    print(Path(load_path).stem + ".prf")

    print("Save project as ", end="")
    save_path = asksaveasfilename(
        filetypes=[("opju", ".opju")],
        title="Save project as",
        defaultextension=".opju",
        confirmoverwrite=True,
    ) + "_rietveld"
    if not save_path:
        return "Cancelled"
    save_path = Path(save_path)
    print(save_path.stem + ".opju")

    print("Importing data...")
    path = Path(load_path)
    if not path.exists() or not path.is_file():
        return "Invalid file path: " + str(path)
    data = path.read_text()[26:-6]
    hkl_data, xrd_data = data.split("\n 999\n")
    h_vals, k_vals, l_vals, ph_vals, th_vals = ([] for _ in range(5))
    for line in hkl_data.split("\n"):
        h, k, l, _, ph, th, *_ = line.split()
        h_vals.append(int(h))
        k_vals.append(int(k))
        l_vals.append(int(l))
        ph_vals.append(int(ph))
        th_vals.append(float(th))
    hkl_df = pd.concat(
        [
            pd.DataFrame(h_vals, columns=["h"]),
            pd.DataFrame(k_vals, columns=["k"]),
            pd.DataFrame(l_vals, columns=["l"]),
            pd.DataFrame(ph_vals, columns=["Phase"]),
            pd.DataFrame(th_vals, columns=["2θ"]),
            pd.DataFrame([-0.45 for _ in range(len(h_vals))], columns=["Shift"])
        ],
        axis=1,
    )
    th_vals, obs_i_vals, calc_i_vals, bckg_vals, dif_vals = ([] for _ in range(5))
    for line in xrd_data.split("\n"):
        th, obs_i, calc_i, _, _, _, _, _, bckg, *_ = line.split()
        th_vals.append(float(th))
        obs_i_vals.append(float(obs_i))
        calc_i_vals.append(float(calc_i))
        bckg_vals.append(float(bckg))
    obs_i_vals_max = max(obs_i_vals)
    obs_i_vals = [val / obs_i_vals_max for val in obs_i_vals]
    calc_i_vals = [val / obs_i_vals_max for val in calc_i_vals]
    bckg_vals = [val / obs_i_vals_max for val in bckg_vals]
    dif_vals = [obs_i - calc_i - 0.15 for obs_i, calc_i in zip(obs_i_vals, calc_i_vals)]
    xrd_df = pd.concat(
        [
            pd.DataFrame(th_vals, columns=["2θ"]),
            pd.DataFrame(obs_i_vals, columns=["I obs"]),
            pd.DataFrame(calc_i_vals, columns=["I calc"]),
            pd.DataFrame(bckg_vals, columns=["I bckg"]),
            pd.DataFrame(dif_vals, columns=["I dif"]),
        ],
        axis=1,
    )
    min_x, max_x = xrd_df["2θ"].min(), xrd_df["2θ"].max()
    min_y, max_y = -0.25, 1.045
    print("Import successful")

    print("Starting OriginPro...")
    op.set_show()
    hkl_worksheet = op.new_sheet("w", "hkl")
    xrd_worksheet = op.new_sheet("w", "XRD")
    hkl_worksheet.from_df(hkl_df)
    xrd_worksheet.from_df(xrd_df)
    graph = op.new_graph()
    graph.set_int("aa", 1)
    layer_1 = graph[0]

    layer_1.xlim = (min_x, max_x, 10)
    layer_1.ylim = (min_y, max_y)

    obs_i_plot = layer_1.add_plot(xrd_worksheet, 1, 0, type="s")
    calc_i_plot = layer_1.add_plot(xrd_worksheet, 2, 0, type="l")
    bckg_i_plot = layer_1.add_plot(xrd_worksheet, 3, 0, type="l")
    dif_i_plot = layer_1.add_plot(xrd_worksheet, 4, 0, type="l")
    hkl_plot = layer_1.add_plot(hkl_worksheet, 5, 4, type="s")

    obs_i_plot.color = "Black"
    calc_i_plot.color = "Red"
    bckg_i_plot.color = "Orange"
    dif_i_plot.color = "Red"
    hkl_plot.color = "Navy"

    obs_i_plot.set_int("symbol.kind", 2)
    obs_i_plot.set_int("symbol.interior", 1)
    obs_i_plot.set_int("symbol.size", 5)
    calc_i_plot.set_int("line.width", 2)
    bckg_i_plot.set_int("line.width", 2)
    dif_i_plot.set_int("line.width", 2)
    hkl_plot.set_int("symbol.kind", 10)
    hkl_plot.set_int("symbol.interior", 0)
    hkl_plot.set_int("symbol.size", 8)

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
