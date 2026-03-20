from nagraph.graph import xrd, rietveld


def main():
    while True:
        print("What do you want to do?\n0. Exit."
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
