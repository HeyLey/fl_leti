#!/usr/bin/python3
import sys

from grammar import *


def remove_start(grammar):
    return [Rule("S", "E")] + grammar


def remove_non_unit_terminals(grammar):
    d = {}

    nonterminals = get_free_nonterminals(grammar)

    result = []

    for r in grammar:
        if len(r.rhs) == 1:
            result.append(r)
            continue

        new_rhs = []

        for v in r.rhs:
            if is_terminal(v):
                if v not in d:
                    new_nonterminal = nonterminals.__next__()
                    d[v] = new_nonterminal
                    result.append(Rule(new_nonterminal, v))

                new_rhs.append(d[v])
            else:
                new_rhs.append(v)

        result.append(Rule(r.lhs, new_rhs))

    return result


def remove_long_rules(grammar):
    result = []

    nonterminals = get_free_nonterminals(grammar)

    for r in grammar:
        rhs = r.rhs
        if len(rhs) <= 2:
            result.append(r)
            continue

        current_lhs = r.lhs

        for i in range(len(rhs) - 2):
            new_nonterminal = nonterminals.__next__()
            result.append(Rule(current_lhs, [rhs[i], new_nonterminal]))
            current_lhs = new_nonterminal

        result.append(Rule(current_lhs, rhs[-2:]))

    return result


def remove_chain_rules(grammar):
    not_chain = []

    reverse_chain = {}

    for r in grammar:
        rhs = r.rhs
        if len(rhs) == 1 and not is_terminal(rhs[0]):
            if rhs[0] not in reverse_chain:
                reverse_chain[rhs[0]] = []

            reverse_chain[rhs[0]].append(r.lhs)
        else:
            not_chain.append(r)

    has_changed = True

    while has_changed:
        has_changed = False
        new_reverse_chain = {}
        for (r, lefts) in reverse_chain.items():
            new_lefts = set(lefts)
            for l in lefts:
                if l in reverse_chain:
                    new_lefts.update(reverse_chain[l])

            if len(new_lefts) == len(lefts):
                new_reverse_chain[r] = lefts
            else:
                new_reverse_chain[r] = list(new_lefts)
                has_changed = True

        reverse_chain = new_reverse_chain

    result = []

    for r in not_chain:
        result.append(r)
        for v in reverse_chain.get(r.lhs, []):
            result.append(Rule(v, r.rhs))

    return result


def remove_unused_symbols(grammar, start):
    used_symbol = {start}

    while True:
        new_used_symbol = set()
        for r in grammar:
            if r.lhs in used_symbol:
                for v in r.rhs:
                    if v not in used_symbol:
                        used_symbol.add(v)
                        new_used_symbol.add(v)
        if len(new_used_symbol) == 0:
            break

    return [r for r in grammar if r.lhs in used_symbol]

def chomsky(grammar):
    grammar = remove_start(grammar)
    grammar = remove_non_unit_terminals(grammar)
    grammar = remove_long_rules(grammar)
    grammar = remove_chain_rules(grammar)
    grammar = remove_unused_symbols(grammar, "S")
    return grammar


def main(file):
    grammar = read_grammar(file)

    print_grammar(grammar)

    print("\nУдалим стартовый нетерминал из правых частей правил:")
    grammar = remove_start(grammar)

    print_grammar(grammar)

    print("Избавимся от неодиночных терминалов в правых частях:")
    grammar = remove_non_unit_terminals(grammar)

    print_grammar(grammar)

    print("Удалим длинные правила (длины больше 2)")

    grammar = remove_long_rules(grammar)

    print_grammar(grammar)

    print("Удалим цепные правила")

    grammar = remove_chain_rules(grammar)
    print_grammar(grammar)

    print("Удалим бесполезные символы")

    grammar = remove_unused_symbols(grammar, "S")
    print_grammar(grammar)


if __name__ == '__main__':
    main(sys.argv[1])
