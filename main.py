from nagraph.graph import simple_xrd, refined_xrd
from nagraph import interface
import tkinter as tk


def main():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root_width = 640
    root_height = 360
    root.title("NaGraph")
    root.resizable(False, False)
    root.geometry('%sx%s+%s+%s' % (root_width, root_height, int((screen_width-root_width)/2), int((screen_height-root_height)/2)))

    lbl_xrd = tk.Label(root, text="XRD")
    lbl_gc = tk.Label(root, text="GC")
    lbl_unknown = tk.Label(root, text="???")
    btn_simple = tk.Button(root, text="Simple", command=interface.graph_xrd)
    btn_refined = tk.Button(root, text="Refined", command=interface.graph_rietveld)
    btn_rates = tk.Button(root, text="Rates", command=interface.graph_rietveld)
    btn_long = tk.Button(root, text="Long", command=interface.graph_rietveld)
    btn_unknown1 = tk.Button(root, text="???", command=interface.graph_rietveld)
    btn_unknown2 = tk.Button(root, text="???", command=interface.graph_rietveld)
    lbl_source = tk.Label(root, text="Source")
    lbl_issues = tk.Label(root, text="Issues")
    lbl_license = tk.Label(root, text="License")
    lbl_about = tk.Label(root, text="About")
    btn_exit = tk.Button(root, text="Exit", command=root.destroy)

    lbl_xrd.grid(column=0, row=0, columnspan=2, ipadx=5, ipady=5, padx=10, pady=10)
    lbl_gc.grid(column=2, row=0, columnspan=2, ipadx=5, ipady=5, padx=10, pady=10)
    lbl_unknown.grid(column=4, row=0, columnspan=2, ipadx=5, ipady=5, padx=10, pady=10)
    btn_simple.grid(column=0, row=1, columnspan=2, ipadx=5, ipady=5, padx=10, pady=10)
    btn_refined.grid(column=0, row=2, columnspan=2, ipadx=5, ipady=5, padx=10, pady=10)
    btn_rates.grid(column=2, row=1, columnspan=2, ipadx=5, ipady=5, padx=10, pady=10)
    btn_long.grid(column=2, row=2, columnspan=2, ipadx=5, ipady=5, padx=10, pady=10)
    btn_unknown1.grid(column=4, row=1, columnspan=2, ipadx=5, ipady=5, padx=10, pady=10)
    btn_unknown2.grid(column=4, row=2, columnspan=2, ipadx=5, ipady=5, padx=10, pady=10)
    lbl_source.grid(column=0, row=3, ipadx=1, ipady=5, padx=1, pady=10)
    lbl_issues.grid(column=1, row=3, ipadx=1, ipady=5, padx=1, pady=10)
    lbl_license.grid(column=2, row=3, ipadx=1, ipady=5, padx=1, pady=10)
    lbl_about.grid(column=3, row=3, ipadx=1, ipady=5, padx=1, pady=10)
    btn_exit.grid(column=4, row=3, columnspan=2, ipadx=5, ipady=5, padx=10, pady=10)

    root.mainloop()
    return
    while True:
        print("What do you want to do?"
              "\n0. Exit."
              "\n1. Graph XRD."
              "\n2. Graph Rietveld refinement (Jana2006)")
        mode = input()
        if mode.isdigit() & len(mode) == 1:
            if mode == "0":
                break
            elif mode == "1":
                print(xrd.xrd())
            elif mode == "2":
                print(rietveld.rietveld())
        else:
            print("Invalid input")
    input("Press Enter to continue...")


if __name__ == "__main__":
    main()
