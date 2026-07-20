import math

import originpro as op

from util.util import (
    save_project_with_suffix,
    open_files_of_types,
    match_file_type,
    match_text_type,
    get_last_word, format_uncertain_float,
)
from util.deco import threaded


@threaded
def xrd(verbose=False) -> int:

    input_paths = open_files_of_types(["xyd"], True)

    output_path = save_project_with_suffix("xrd", True)

    if verbose:
        print("Importing data...")

    xrd_data = []

    for i, path in enumerate(input_paths):
        if not match_file_type(path, "*.xyd"):
            raise Exception("Invalid internal file structure")

        th_vals, i_vals = ([] for _ in range(2))

        for line in path.read_text()[:-1].splitlines():
            x, y = line.strip().split()
            th_vals.append(float(x))
            i_vals.append(float(y))

        i_vals_max = max(i_vals)
        i_vals_min = min(i_vals)
        i_vals = [
            (val - i_vals_min) / (i_vals_max - i_vals_min) + 0.1 * i for val in i_vals
        ]
        xrd_data.append((th_vals, i_vals))

    min_x, max_x = 180, 0
    for data in xrd_data:
        new_min_x = min(data[0])
        new_max_x = max(data[0])
        min_x = new_min_x if new_min_x < min_x else min_x
        max_x = new_max_x if new_max_x > max_x else max_x
    assert min_x <= max_x

    min_y, max_y = -0.05, 1.05 + (len(xrd_data)) * 0.1

    if verbose:
        print("Import successful")

    if verbose:
        print("Starting OriginPro...")
    op.set_show()

    worksheet = op.new_sheet("w", "XRD")
    for i, data in enumerate(xrd_data):
        print("accessing columns " + str((i - 1) * 2) + " and " + str((i * 2) - 1))
        worksheet.from_list(col=i * 2, data=data[0], lname="2θ", units="deg.", axis="X")
        worksheet.from_list(
            col=i * 2 + 1,
            data=data[1],
            lname=input_paths[i].stem,
            units="r.u.",
            axis="Y",
        )

    graph = op.new_graph()
    graph.set_int("aa", 1)
    layer_1 = graph[0]
    for column in range(0, worksheet.cols):
        layer_1.add_plot(worksheet, column * 2 + 1, column * 2)
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

    input_paths = open_files_of_types(["prf", "txt", "inp", "cif"], verbose)

    output_path = save_project_with_suffix("rietveld", verbose)

    if verbose:
        print("Importing data...")

    # HKL Worksheet
    h_vals, k_vals, l_vals, ph_vals, peak_vals = ([] for _ in range(5))
    # XRD Worksheet
    th_vals, obs_i_vals, calc_i_vals, bckg_i_vals, dif_vals = ([] for _ in range(5))
    # Meta & Cell
    prec_data = {}
    cell_data = {}

    # Chek file type and fill "vals" accordingly
    for path in input_paths:
        text = path.read_text()
        if match_text_type(text, "*.prf"):
            hkl_data, xrd_data = text[26:-6].split("\n 999\n")
            for line in hkl_data.splitlines():
                h, k, l, _, ph, peak, *_ = line.split()
                h_vals.append(int(h))
                k_vals.append(int(k))
                l_vals.append(int(l))
                ph_vals.append(int(ph))
                peak_vals.append(float(peak))
            for line in xrd_data.splitlines():
                th, obs_i, calc_i, _, _, _, _, _, bckg, *_ = line.split()
                if not ((obs_i == "0") or (calc_i == "0") or (bckg == "0")):
                    th_vals.append(float(th))
                    obs_i_vals.append(float(obs_i))
                    calc_i_vals.append(float(calc_i))
                    bckg_i_vals.append(float(bckg))
        elif match_text_type(text, "2Th_I.txt"):
            for line in text[:-1].splitlines():
                h, k, l, _, ph, th, *_ = [0, 0, 0, 0, 0] + line.split()
                h_vals.append(int(h))
                k_vals.append(int(k))
                l_vals.append(int(l))
                ph_vals.append(int(ph))
                peak_vals.append(float(th))
        elif match_text_type(text, "data.txt"):
            for line in text[58:-1].splitlines():
                th, obs_i, bckg, calc_i, dif_i = line.split(",")
                if not ((obs_i == "0") or (calc_i == "0") or (bckg == "0")):
                    th_vals.append(float(th))
                    obs_i_vals.append(float(obs_i))
                    calc_i_vals.append(float(calc_i))
                    bckg_i_vals.append(float(bckg))
                    dif_vals.append(float(dif_i))
        elif match_text_type(text, "*.inp"):
            (
                prec_data["r_wp"],
                prec_data["r_exp"],
                prec_data["r_p"],
                _,
                prec_data["gof"],
            ) = map(float, text.splitlines()[2].split()[1::2])
            for key, value in prec_data.items():
                prec_data[key] = round(value, 2)
            (
                cell_data["a"],
                cell_data["b"],
                cell_data["c"],
                cell_data["alpha"],
                cell_data["beta"],
                cell_data["gamma"],
                cell_data["volume"],
                cell_data["space_group"],
                *_
            ) = map(get_last_word, text[1048:1219].splitlines())
            cell_data["space_group"] = cell_data["space_group"].strip("\"")
            for key, value in cell_data.items():
                cell_data[key] = format_uncertain_float(value)
        elif match_file_type(path, "*.cif"):
            pass

    # Normalization
    obs_i_vals_max = max(obs_i_vals)
    obs_i_vals_min = min(obs_i_vals)
    obs_i_vals = [
        (val - obs_i_vals_min) / (obs_i_vals_max - obs_i_vals_min) for val in obs_i_vals
    ]
    calc_i_vals = [
        (val - obs_i_vals_min) / (obs_i_vals_max - obs_i_vals_min)
        for val in calc_i_vals
    ]
    bckg_i_vals = [
        (val - obs_i_vals_min) / (obs_i_vals_max - obs_i_vals_min)
        for val in bckg_i_vals
    ]

    # Calculating dif values
    dif_vals = [obs_i - calc_i for obs_i, calc_i in zip(obs_i_vals, calc_i_vals)]
    delta_dif_vals = min(dif_vals) - max(dif_vals)
    dif_vals = [val + delta_dif_vals for val in dif_vals]

    if verbose:
        print("Import successful")

    if verbose:
        print("Starting OriginPro...")

    op.set_show()

    hkl_worksheet = op.new_sheet("w", "hkl")
    xrd_worksheet = op.new_sheet("w", "XRD")
    hkl_worksheet.from_list(col=0, data=h_vals, lname="h", units="", axis="")
    hkl_worksheet.from_list(col=1, data=k_vals, lname="k", units="", axis="")
    hkl_worksheet.from_list(col=2, data=l_vals, lname="l", units="", axis="")
    hkl_worksheet.from_list(col=3, data=ph_vals, lname="Phase", units="", axis="")
    hkl_worksheet.from_list(col=4, data=peak_vals, lname="2θ", units="deg.", axis="X")
    hkl_worksheet.from_list(
        col=5, data=[-0.03 for _ in h_vals], lname="hkl", units="", axis="Y"
    )
    xrd_worksheet.from_list(col=0, data=th_vals, lname="2θ", units="deg.", axis="X")
    xrd_worksheet.from_list(
        col=1, data=obs_i_vals, lname="I obs", units="r.u.", axis="Y"
    )
    xrd_worksheet.from_list(
        col=2, data=calc_i_vals, lname="I calc", units="r.u.", axis="Y"
    )
    xrd_worksheet.from_list(
        col=3, data=bckg_i_vals, lname="I bckg", units="r.u.", axis="Y"
    )
    xrd_worksheet.from_list(col=4, data=dif_vals, lname="I dif", units="r.u.", axis="Y")

    graph = op.new_graph()
    graph.set_int("aa", 1)
    layer_1 = graph[0]

    min_x, max_x = math.floor(min(th_vals)), math.ceil(max(th_vals))
    i_min_y, i_max_y = delta_dif_vals - 0.15, 1.05
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
