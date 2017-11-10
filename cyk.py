import sys

from chomsky import read_grammar, chomsky
from tree import Tree


def make_tree(terminal_rules, nonterminal_rules, str, table, s, i1, i2):
    if i1 < i2:
        for m in range(i1, i2):
            for (lhs, r1, r2) in nonterminal_rules:
                if lhs == s and table[r1][i1][m] and table[r2][m + 1][i2]:
                    t1 = make_tree(terminal_rules, nonterminal_rules, str, table, r1, i1, m)
                    t2 = make_tree(terminal_rules, nonterminal_rules, str, table, r2, m + 1, i2)
                    tree = Tree(s)
                    tree.children = [t1, t2]
                    return tree
    else:
        tree = Tree(s)
        tree.children = [str[i1]]
        return tree

def cyk(grammar, string):
    symbols = set()

    terminal_rules = []
    nonterminal_rules = []

    for r in grammar:
        symbols.add(r.lhs)
        if len(r.rhs) == 1:
            terminal_rules.append((r.lhs, r.rhs[0]))
        else:
            nonterminal_rules.append((r.lhs, r.rhs[0], r.rhs[1]))

    table = {}

    for s in symbols:
        table[s] = [[False for s in string] for s in string]

    str_len = len(string)
    for i in range(str_len):
        for l, r in terminal_rules:
            if r == string[i]:
                table[l][i][i] = True

    for l in range(1, str_len):
        for offset in range(0, str_len - l):
            for m in range(l):
                for (lhs, r1, r2) in nonterminal_rules:
                    if table[r1][offset][offset + m] and table[r2][offset + m + 1][offset + l]:
                        print(lhs, offset, offset + l)
                        table[lhs][offset][offset + l] = True

    for s, t in table.items():
        print("Table for {}".format(s))
        print("  " + " ".join(string))
        for i1 in range(str_len):
            print(string[i1] + " " + " ".join(["+" if v else "-" for v in t[i1]]))

    if table["S"][0][len(string) - 1]:
        print("Tree")
        make_tree(terminal_rules, nonterminal_rules, string, table, "S", 0, len(string) - 1).do_print()
    else:
        print("Не удалось распарсить строчку")


def main(file, string):
    grammar = read_grammar(file)
    grammar = chomsky(grammar)

    cyk(grammar, string)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
