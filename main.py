from nagraph.graph import xrd, rietveld, cycling


def main():
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
                cycling.steps()
            elif mode == "4":
                cycling.long()
        else:
            print("Invalid input")
    input("Press Enter to continue...")


if __name__ == "__main__":
    main()
