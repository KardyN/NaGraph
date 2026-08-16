import tkinter

import originpro as op

from graph.cycling import rates, long
from graph.xrd import xrd, rietveld


class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self_width = 600
        self_height = 350
        self.title("NaGraph")
        self.resizable(False, False)
        self.geometry(
            "%sx%s+%s+%s"
            % (
                self_width,
                self_height,
                int((screen_width - self_width) / 2),
                int((screen_height - self_height) / 2),
            )
        )

        lbl_xrd = tkinter.Label(self, text="XRD")
        lbl_gc = tkinter.Label(self, text="GC")
        lbl_unknown = tkinter.Label(self, text="???")
        btn_simple = tkinter.Button(self, text="Simple", command=xrd)
        btn_refined = tkinter.Button(self, text="Refined", command=rietveld)
        btn_rates = tkinter.Button(self, text="Rates", command=rates)
        btn_long = tkinter.Button(self, text="Long", command=long)
        btn_unknown1 = tkinter.Button(self, text="???")
        btn_unknown2 = tkinter.Button(self, text="???")
        lbl_source = tkinter.Label(self, text="Source")
        lbl_issues = tkinter.Label(self, text="Issues")
        lbl_license = tkinter.Label(self, text="License")
        lbl_about = tkinter.Label(self, text="About")
        btn_exit = tkinter.Button(self, text="Exit", command=self.destroy)

        self.rowconfigure(index=0, weight=1, minsize=20)
        self.rowconfigure(index=1, weight=1, minsize=20)
        self.rowconfigure(index=2, weight=1, minsize=20)
        self.rowconfigure(index=3, weight=1, minsize=20)

        self.columnconfigure(index=0, weight=1, minsize=40)
        self.columnconfigure(index=1, weight=1, minsize=40)
        self.columnconfigure(index=2, weight=1, minsize=40)
        self.columnconfigure(index=3, weight=1, minsize=40)
        self.columnconfigure(index=4, weight=2, minsize=80)

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
