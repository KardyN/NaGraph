import logging

import originpro as op

import pylightxl as xl

from util.deco import threaded
from util.help import save_project_with_suffix, open_files_of_types

log = logging.getLogger(f"nagraph.{__name__}")


@threaded
def rates():
    input_paths = open_files_of_types(["xlsx"], 42)

    output_path = save_project_with_suffix("cycling")

    log.info("Importing data...")

    data = {}

    for path in input_paths:
        try:
            db = xl.readxl(fn=path, ws="record")
        except UserWarning:
            log.warning(
                "[WARN] Skipped '" + path.stem + "', 'record' worksheet was not found"
            )
            continue
        spec_cap_vals, voltage_vals = ([] for _ in range(2))
        for col in db.ws(ws="record").cols:
            col_name = col[0]
            col_data = col[1:]
            if col_name == "Spec. Cap.":
                spec_cap_vals += col_data
            elif col_name == "Voltage":
                voltage_vals += col_data
        if not voltage_vals or not spec_cap_vals:
            log.warning(
                "[WARN] Skipped '"
                + path.stem
                + "', 'Voltage' or 'Spec. Cap.' columns were not found"
            )
        data[path.stem] = (spec_cap_vals, voltage_vals)

    log.info("Import successful")

    log.info("Preparing data...")

    for key, (spec_cap_vals, voltage_vals) in data.items():
        new_spec_cap_vals, new_voltage_vals = ([] for _ in range(2))
        prev_spec_cap = 1
        for spec_cap, voltage in zip(spec_cap_vals, voltage_vals):
            if not prev_spec_cap + spec_cap == 0:
                new_spec_cap_vals.append(spec_cap)
                new_voltage_vals.append(voltage)
            prev_spec_cap = spec_cap
        data[key] = (new_spec_cap_vals, new_voltage_vals)

        data[key] = {}
        i = 0
        sub_spec_cap_vals, sub_voltage_vals = ([] for _ in range(2))
        for spec_cap, voltage in zip(new_spec_cap_vals, new_voltage_vals):
            if spec_cap == 0:
                if not i == 0:
                    data[key][i] = (sub_spec_cap_vals, sub_voltage_vals)
                sub_spec_cap_vals, sub_voltage_vals = ([] for _ in range(2))
                i += 1
            sub_spec_cap_vals.append(spec_cap)
            sub_voltage_vals.append(voltage)

    log.info("Preparation complete")

    log.info("Starting OriginPro...")

    op.set_show()

    worksheets, graphs = ([] for _ in range(2))
    for key, values in data.items():
        worksheet = op.new_sheet("w", key)
        for i, (current, (spec_cap_vals, voltage_vals)) in enumerate(values.items()):
            worksheet.from_list(
                col=i * 2,
                data=spec_cap_vals,
                lname="Spec. Cap.",
                units="mAh/g",
                axis="X",
                comments=str(current),
            )
            worksheet.from_list(
                col=i * 2 + 1,
                data=voltage_vals,
                lname="Voltage",
                units="V",
                axis="Y",
                comments=str(current),
            )
        worksheets.append(worksheet)
        graph = op.new_graph(lname=key)
        graph.set_int("aa", 1)
        graphs.append(graph)
        layer_1 = graph[0]
        layer_1.add_plot(worksheet, 1, 0)
        # layer_1.xlim = (min(spec_cap_vals), max(spec_cap_vals))
        # layer_1.ylim = (min(voltage_vals), max(voltage_vals))

    log.info("Saving project...")
    for graph in graphs:
        graph.save_fig(str(output_path.with_suffix(".png")))
    op.save(str(output_path.with_suffix(".opju")))
    op.exit()
    log.info("Saved project at " + (str(output_path.with_suffix(".opju"))))
    pass


@threaded
def long():
    input_paths = open_files_of_types(["xlsx"], 10)

    output_path = save_project_with_suffix("cycling")

    log.info("Importing data...")

    # Cycle Worksheet
    cell_id_vals, chg_spec_cap_vals, dchg_spec_cap_vals, chg_dchg_eff_vals = (
        [] for _ in range(4)
    )

    # TODO
    # The order of files is important.
    # Maybe we should auto sort them in case input files aren't sorted alphabetically
    # TODO also add check for file type
    for path in input_paths:
        try:
            db = xl.readxl(fn=path, ws="Cycle")
        except UserWarning:
            log.warning(
                "[WARN] Skipped '" + path.stem + "', 'Cycle' worksheet was not found"
            )
            continue
        for col in db.ws(ws="Cycle").cols:
            col_name = col[0]
            col_data = col[1:]
            if col_name == "":
                cell_id_vals += col_data
            elif col_name == "Chg. Spec. Cap.(mAh/g)":
                chg_spec_cap_vals += col_data
            elif col_name == "DChg. Spec. Cap.(mAh/g)":
                dchg_spec_cap_vals += col_data
            elif col_name == "Chg.-DChg. Eff":
                chg_dchg_eff_vals += col_data
            else:
                pass

    # TODO split cell_data according to the cell column into different sheets

    log.info("Import successful")

    log.info("Starting OriginPro...")

    op.set_show()

    worksheet = op.new_sheet("w", "Cycle")
    # TODO fill ws

    graph = op.new_graph()
    graph.set_int("aa", 1)
    layer_1 = graph[0]
    # TODO make pretty graph

    log.info("Saving project...")
    graph.save_fig(str(output_path.with_suffix(".png")))
    op.save(str(output_path.with_suffix(".opju")))
    op.exit()
    log.info("Saved project at " + (str(output_path.with_suffix(".opju"))))
