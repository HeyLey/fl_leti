
class Tree:
    def __init__(self, v):
        self.v = v
        self.children = None

    def do_print(self, prefix=""):
        if self.children is None:
            print(self.v)
        else:
            if len(self.children) > 1:
                print(self.v + "━┳╸", end="")
            else:
                print(self.v + "━━╸", end="")

            first = True

            for c in self.children:
                if not first:
                    print(prefix, end="")
                    if c == self.children[-1]:
                        print("  ┗╸", end="")
                    else:
                        print("  ┣╸", end="")

                if isinstance(c, Tree):
                    if c == self.children[-1]:
                        c.do_print(prefix + "    ")
                    else:
                        c.do_print(prefix + "  ┃ ")
                else:
                    print(c)

                if c != self.children[-1]:
                    print(prefix + "  ┃ ")
                first = False
