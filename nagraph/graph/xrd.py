import math
import re
from pathlib import Path

import originpro as op
import pandas as pd
from openpyxl.descriptors import String
from openpyxl.pivot.fields import Boolean

from util import save_project_with_suffix, open_files_of_types, assert_file_is_hkl_peaks


def xrd(verbose=False) -> int:

    input_paths = open_files_of_types(["xyd"], 10, True)

    output_path = save_project_with_suffix("xrd", True)

    if verbose:
        print("Importing data...")
    df = pd.DataFrame()
    i = 0
    for path in input_paths:
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
    if verbose:
        print("Import successful")

    if verbose:
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

    if verbose:
        print("Saving project...")
    graph.save_fig(str(output_path.with_suffix(".png")))
    op.save(str(output_path.with_suffix(".opju")))
    op.exit()
    if verbose:
        print("Saved project at " + (str(output_path.with_suffix(".opju"))))
    return 0


def rietveld(verbose=False) -> int:

    input_paths = open_files_of_types(["prf", "txt", "inp", "cif"], 5, verbose)

    output_path = save_project_with_suffix("rietveld", verbose)

    if verbose:
        print("Importing data...")

    if len(input_paths) == 1:
        hkl_data, xrd_data = input_paths.read_text()[26:-6].split("\n 999\n")

    h_vals, k_vals, l_vals, ph_vals, th_vals = ([] for _ in range(5))

    if len(input_paths) == 1:
        for line in hkl_data.split("\n"):
            h, k, l, _, ph, th, *_ = line.split()
            h_vals.append(int(h))
            k_vals.append(int(k))
            l_vals.append(int(l))
            ph_vals.append(int(ph))
            th_vals.append(float(th))
    else:
        for line in input_paths[0].read_text().split("\n"):
            h, k, l, _, ph, th, *_ = [0, 0, 0, 0, 0] + line.split()
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
            pd.DataFrame([-0.03 for _ in range(len(h_vals))], columns=["hkl"]),
        ],
        axis=1,
    )

    th_vals, obs_i_vals, calc_i_vals, bckg_vals, dif_vals = ([] for _ in range(5))

    if len(input_paths) == 1:
        for line in xrd_data.split("\n"):
            th, obs_i, calc_i, _, _, _, _, _, bckg, *_ = line.split()
            th_vals.append(float(th))
            obs_i_vals.append(float(obs_i))
            calc_i_vals.append(float(calc_i))
            bckg_vals.append(float(bckg))
    else:
        

    obs_i_vals_max = max(obs_i_vals)
    obs_i_vals = [val / obs_i_vals_max for val in obs_i_vals]
    calc_i_vals = [val / obs_i_vals_max for val in calc_i_vals]
    bckg_vals = [val / obs_i_vals_max for val in bckg_vals]
    dif_vals = [obs_i - calc_i - 0.05 for obs_i, calc_i in zip(obs_i_vals, calc_i_vals)]
    dif_min_y, dif_max_y = min(dif_vals), max(dif_vals)
    dif_vals = [val - (dif_max_y - dif_min_y) for val in dif_vals]

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

    if verbose:
        print("Import successful")

    if verbose:
        print("Starting OriginPro...")
    op.set_show()
    hkl_worksheet = op.new_sheet("w", "hkl")
    xrd_worksheet = op.new_sheet("w", "XRD")
    hkl_worksheet.from_df(hkl_df)
    xrd_worksheet.from_df(xrd_df)
    graph = op.new_graph()
    graph.set_int("aa", 1)
    layer_1 = graph[0]

    min_x, max_x = math.floor(xrd_df["2θ"].min()), math.ceil(xrd_df["2θ"].max())
    i_min_y, i_max_y = xrd_df.iloc[:, 1].min() - (dif_max_y - dif_min_y) - 0.15, 1.05
    layer_1.xlim = (min_x, max_x, 10)
    layer_1.ylim = (i_min_y, i_max_y)

    obs_i_plot = layer_1.add_plot(xrd_worksheet, 1, 0, type="s")
    calc_i_plot = layer_1.add_plot(xrd_worksheet, 2, 0, type="l")
    bckg_i_plot = layer_1.add_plot(xrd_worksheet, 3, 0, type="l")
    dif_i_plot = layer_1.add_plot(xrd_worksheet, 4, 0, type="l")
    hkl_plot = layer_1.add_plot(hkl_worksheet, 5, 4, type="s")

    obs_i_plot.color = "Black"
    calc_i_plot.color = "Red"
    bckg_i_plot.color = "Orange"
    dif_i_plot.color = "Wine"
    hkl_plot.color = "Black"

    obs_i_plot.set_int("symbol.kind", 2)
    obs_i_plot.set_int("symbol.interior", 1)
    obs_i_plot.set_int("symbol.size", 6)
    calc_i_plot.set_int("line.width", 2)
    bckg_i_plot.set_int("line.width", 2)
    dif_i_plot.set_int("line.width", 2)
    hkl_plot.set_int("symbol.kind", 10)
    hkl_plot.set_int("symbol.interior", 0)
    hkl_plot.set_int("symbol.size", 9)

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

    if verbose:
        print("Saving project...")
    graph.save_fig(str(output_path.with_suffix(".png")))
    op.save(str(output_path.with_suffix(".opju")))
    op.exit()
    if verbose:
        print("Saved project at " + (str(output_path.with_suffix(".opju"))))
    return 0
