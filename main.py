from nagraph.graph import xrd, cycling
from nagraph import interface
import tkinter as tk


def main():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root_width = 300
    root_height = 250
    root.title("NaGraph")
    root.resizable(False, False)
    root.geometry('%sx%s+%s+%s' % (root_width, root_height, int((screen_width-root_width)/2), int((screen_height-root_height)/2)))

    lbl_xrd = tk.Label(root, text="XRD")
    lbl_gc = tk.Label(root, text="GC")
    lbl_unknown = tk.Label(root, text="???")
    btn_simple = tk.Button(root, text="Simple", command=interface.xrd_simple)
    btn_refined = tk.Button(root, text="Refined", command=interface.xrd_refined)
    btn_rates = tk.Button(root, text="Rates", command=interface.gc_rates)
    btn_long = tk.Button(root, text="Long", command=interface.gc_long)
    btn_unknown1 = tk.Button(root, text="???", command=interface.test1)
    btn_unknown2 = tk.Button(root, text="???", command=interface.test2)
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
    lbl_unknown.grid(column=4, row=0, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)
    btn_simple.grid(column=0, row=1, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)
    btn_refined.grid(column=0, row=2, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)
    btn_rates.grid(column=2, row=1, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)
    btn_long.grid(column=2, row=2, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)
    btn_unknown1.grid(column=4, row=1, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)
    btn_unknown2.grid(column=4, row=2, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)
    lbl_source.grid(column=0, row=3, ipadx=1, ipady=1, padx=1, pady=1)
    lbl_issues.grid(column=1, row=3, ipadx=1, ipady=1, padx=1, pady=1)
    lbl_license.grid(column=2, row=3, ipadx=1, ipady=1, padx=1, pady=1)
    lbl_about.grid(column=3, row=3, ipadx=1, ipady=1, padx=1, pady=1)
    btn_exit.grid(column=4, row=3, columnspan=2, ipadx=1, ipady=1, padx=1, pady=1)

    root.mainloop()
    return
    while True:
        print("What do you want to do?\n0. Exit."
              "\n1. Graph XRD."
              "\n2. Graph Rietveld."
              "\n3. Cycling steps."
              "\n4. Cycling long.")
        mode = input()
        if mode.isdigit() & len(mode) == 1:
            if mode == "0":
                break
            elif mode == "1":
                xrd.xrd(verbose=True)
            elif mode == "2":
                xrd.rietveld(verbose=True)
            elif mode == "3":
                cycling.steps(verbose=True)
            elif mode == "4":
                cycling.long(verbose=True)
        else:
            print("Invalid input")
    input("Press Enter to continue...")


if __name__ == "__main__":
    main()
