import sys

from grammar import *


def remove_left_recursion(grammar):
    terms = set()
    for rule in grammar:
        if rule.lhs == rule.rhs[0]:
            terms.add(rule.lhs)

    result = []

    nonterminals = get_free_nonterminals(grammar)

    for rule in grammar:
        if rule.lhs not in terms:
            result.append(rule)

    for t in terms:
        new_t = next(nonterminals)

        for rule in grammar:
            if rule.lhs != t:
                continue

            if rule.rhs[0] == t:
                result.append(Rule(new_t, ["ε"]))
                result.append(Rule(new_t, rule.rhs[1:] + [new_t]))
            else:
                result.append(Rule(rule.lhs, rule.rhs + [new_t]))

    return result


def left_factorisation(grammar):
    d = OrderedDict()

    nonterminals = get_free_nonterminals(grammar)

    for r in grammar:
        if r.lhs not in d:
            d[r.lhs] = []
        d[r.lhs].append(r.rhs)

    result = []

    for lhs, rhss in d.items():
        d = {}

        for rhs in rhss:
            if rhs[0] not in d:
                d[rhs[0]] = []
            d[rhs[0]].append(rhs)

        for values in d.values():
            if len(values) == 1:
                for v in values:
                    result.append(Rule(lhs, v))
                continue
            common_prefix = 0

            while True:
                value = values[0]

                good = True
                for v in values:
                    if common_prefix == len(value):
                        good = False
                        break
                    if value[common_prefix] != v[common_prefix]:
                        good = False

                if not good:
                    break

                common_prefix += 1

            print(values)
            print(common_prefix)

    return result


def find_first(first, rhs):
    i = 0

    if rhs[0] == "ε":
        return {"ε"}

    current_rhs = set()

    while i < len(rhs):
        if is_terminal(rhs[i]):
            current_rhs.add(rhs[i])
            return current_rhs

        f_rhs = first[rhs[i]]

        for f in f_rhs:
            if f != "ε":
                current_rhs.add(f)

        if "ε" not in f_rhs:
            break

        i += 1

    if i == len(rhs):
        current_rhs.add("ε")

    return current_rhs


def make_first(grammar):
    first = {}

    non_term = set()
    for rule in grammar:
        non_term.add(rule.lhs)

    for t in non_term:
        first[t] = set()

    other_rules = []

    for rule in grammar:
        if rule.rhs[0] == "ε":
            first[rule.lhs].add("ε")
            continue

        if is_terminal(rule.rhs[0]):
            first[rule.lhs].add(rule.rhs[0])
            continue

        other_rules.append(rule)

    changed = True

    while changed:
        changed = False

        for rule in other_rules:
            for f in find_first(first, rule.rhs):
                if f not in first[rule.lhs]:
                    changed = True
                    first[rule.lhs].add(f)

    return first


def make_follow(grammar, first):
    follow = {}

    non_term = set()
    for rule in grammar:
        non_term.add(rule.lhs)

    for t in non_term:
        follow[t] = set()

    follow["E"].add("$")

    for rule in grammar:
        for i in range(0, len(rule.rhs) - 1):
            if is_terminal(rule.rhs[i]):
                continue

            if is_terminal(rule.rhs[i + 1]):
                follow[rule.rhs[i]].add(rule.rhs[i + 1])
            else:
                for v in first[rule.rhs[i + 1]]:
                    if v != "ε":
                        follow[rule.rhs[i]].add(v)

    changed = True

    while changed:
        changed = False

        for rule in grammar:
            i = len(rule.rhs) - 1
            while i >= 0:
                if is_terminal(rule.rhs[i]) or "ε" == rule.rhs[i]:
                    break

                for f in follow[rule.lhs]:
                    if f not in follow[rule.rhs[i]]:
                        changed = True
                        follow[rule.rhs[i]].add(f)

                if "ε" not in first[rule.rhs[i]]:
                    break

                i -= 1

    return follow


def make_table(grammar, first, follow):
    non_term = set()
    for r in grammar:
        non_term.add(r.lhs)

    term = set()

    for r in grammar:
        for v in r.rhs:
            if is_terminal(v):
                term.add(v)

    non_term = sorted(non_term)

    term = sorted(term) + ["$"]

    table = {}

    for nt in non_term:

        row = {}

        for t in term:
            rule = None
            for rule_i, r in enumerate(grammar):
                if r.lhs != nt:
                    continue

                f = find_first(first, r.rhs)

                if t in f:
                    rule = rule_i
                elif "ε" in f and t in follow[r.lhs]:
                    rule = rule_i

            if rule is not None:
                row[t] = rule

        table[nt] = row

    return table


def main(file):
    grammar = read_grammar(file)

    print_grammar(grammar)

    print("Удалим левую рекурсию")

    grammar = remove_left_recursion(grammar)

    print_grammar(grammar)

    print("Левая факторизация не нужна")

    first = make_first(grammar)
    follow = make_follow(grammar, first)

    print("\nFirst")
    for k, v in first.items():
        print(k, v)

    print("\nFollow")
    for k, v in follow.items():
        print(k, v)

    print("\nTable")
    table = make_table(grammar, first, follow)

    non_term = set()
    for r in grammar:
        non_term.add(r.lhs)

    term = set()

    for r in grammar:
        for v in r.rhs:
            if is_terminal(v):
                term.add(v)

    term = sorted(term) + ["$"]

    for i, r in enumerate(grammar):
        print("{} {} := {}".format(i+1, r.lhs, " ".join(r.rhs)))

    print("\\begin{tabular}{ l || c | c || " + " | ".join(["c"] * len(term))+ " }")
    print("N & FIRST & FOLLOW & " +  " & ".join(term) + " \\\\ \hline")

    for nt in non_term:
        print(nt + " & " + " ".join(sorted(first[nt])) + " & " + " ".join(sorted(follow[nt])), end="")

        for i, t in enumerate(term):
            if t in table[nt]:
                print(" & " + str(table[nt][t] + 1), end="")
            else:
                print(" & ", end="")

        print("\\\\")

    print("\end{tabular}")


if __name__ == '__main__':
    main(sys.argv[1])
