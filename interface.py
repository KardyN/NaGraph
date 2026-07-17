from nagraph.graph import xrd
import tkinter as tk


class Interface:
    def __init__(self, root):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root_width = 1200
        root_height = 700
        root.title("NaGraph")
        root.resizable(False, False)
        root.geometry(
            "%sx%s+%s+%s"
            % (
                root_width,
                root_height,
                int((screen_width - root_width) / 2),
                int((screen_height - root_height) / 2),
            )
        )

        lbl_xrd = tk.Label(root, text="XRD")
        lbl_gc = tk.Label(root, text="GC")
        lbl_unknown = tk.Label(root, text="???")
        btn_simple = tk.Button(root, text="Simple", command=graph_xrd)
        btn_refined = tk.Button(root, text="Refined", command=graph_rietveld)
        btn_rates = tk.Button(root, text="Rates", command=graph_gc_rates)
        btn_long = tk.Button(root, text="Long", command=graph_gc_long)
        btn_unknown1 = tk.Button(root, text="???", command=test1)
        btn_unknown2 = tk.Button(root, text="???", command=test2)
        lbl_source = tk.Label(root, text="Source")
        lbl_issues = tk.Label(root, text="Issues")
        lbl_license = tk.Label(root, text="License")
        lbl_about = tk.Label(root, text="About")
        btn_exit = tk.Button(root, text="Exit", command=root.destroy)

        root.rowconfigure(index=0, weight=1, minsize=20)
        root.rowconfigure(index=1, weight=1, minsize=20)
        root.rowconfigure(index=2, weight=1, minsize=20)
        root.rowconfigure(index=3, weight=1, minsize=20)

        root.columnconfigure(index=0, weight=1, minsize=40)
        root.columnconfigure(index=1, weight=1, minsize=40)
        root.columnconfigure(index=2, weight=1, minsize=40)
        root.columnconfigure(index=3, weight=1, minsize=40)
        root.columnconfigure(index=4, weight=2, minsize=80)

        lbl_xrd.grid(column=0, row=0, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)
        lbl_gc.grid(column=2, row=0, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)
        lbl_unknown.grid(
            column=4, row=0, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1
        )
        btn_simple.grid(column=0, row=1, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)
        btn_refined.grid(
            column=0, row=2, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1
        )
        btn_rates.grid(column=2, row=1, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)
        btn_long.grid(column=2, row=2, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)
        btn_unknown1.grid(
            column=4, row=1, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1
        )
        btn_unknown2.grid(
            column=4, row=2, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1
        )
        lbl_source.grid(column=0, row=3, ipadx=1, ipady=1, padx=1, pady=1)
        lbl_issues.grid(column=1, row=3, ipadx=1, ipady=1, padx=1, pady=1)
        lbl_license.grid(column=2, row=3, ipadx=1, ipady=1, padx=1, pady=1)
        lbl_about.grid(column=3, row=3, ipadx=1, ipady=1, padx=1, pady=1)
        btn_exit.grid(column=4, row=3, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)


def graph_xrd():
    xrd.xrd(verbose=True)
    return None


def graph_rietveld():
    xrd.rietveld(verbose=True)
    return None


def graph_gc_rates():
    return None


def graph_gc_long():
    return None


def test1():
    return None


def test2():
    return None
