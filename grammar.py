import string
from collections import OrderedDict


class Rule:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs


def is_terminal(str):
    return not str[0].isalpha()


def parse_line(line):
    line = line.strip()
    parts = line.split(":=")
    lhs = parts[0].strip()
    rhs = parts[1].strip()

    result = []

    for t in rhs.split("|"):
        t = t.strip().split(" ")
        result.append(Rule(lhs, t))

    return result


def read_grammar(file):
    rules = []
    with open(file, "r") as f:
        for line in f:
            rules.extend(parse_line(line))

    return rules


def print_grammar(grammar):
    d = OrderedDict()

    for r in grammar:
        if r.lhs not in d:
            d[r.lhs] = []
        d[r.lhs].append(r.rhs)

    for lhs, rhss in d.items():
        right = [" ".join(rhs) for rhs in rhss]
        print("{} := {}".format(lhs, " | ".join(right)))


def get_all_nonterminals(grammar):
    result = set()
    for rule in grammar:
        result.add(rule.lhs)
        for s in rule.rhs:
            if not is_terminal(s):
                result.add(s)
    return result


def get_free_nonterminals(grammar):
    nonteminals = get_all_nonterminals(grammar)

    for l in string.ascii_uppercase:
        if l not in nonteminals:
            yield l

    for d in string.digits:
        for l in string.ascii_uppercase:
            v = l + d
            if v not in nonteminals:
                yield v


def get_free_nonterminal(grammar):
    return get_free_nonterminals(grammar).__next__()
