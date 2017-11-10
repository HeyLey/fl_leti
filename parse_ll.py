import sys

from grammar import read_grammar, is_terminal
from ll import remove_left_recursion, make_first, make_follow, make_table
from tree import Tree


def main(file, string):
    grammar = read_grammar(file)

    grammar = remove_left_recursion(grammar)

    first = make_first(grammar)
    follow = make_follow(grammar, first)

    table = make_table(grammar, first, follow)

    string = string + "$"

    stack = ["E"]
    main_tree = Tree("E")
    tree_stack = [main_tree]

    while len(stack) > 0:
        print("Строчка {}".format(string))
        print("   Стек {}".format(stack))
        print()
        first = stack[0]
        if is_terminal(first):
            if string[0] == first:
                stack = stack[1:]
                tree_stack = tree_stack[1:]
                string = string[1:]
            else:
                print("Ошибка парсинга")
                return
        else:
            if string[0] not in table[first]:
                print("Ошибка парсинга")
                return
            next = table[first][string[0]]
            if next[0] == "ε":
                tree = tree_stack[0]
                tree.children = ["ε"]
                stack = stack[1:]
                tree_stack = tree_stack[1:]
            else:
                tree = tree_stack[0]
                tree_children = [v if is_terminal(v) else Tree(v) for v in next]
                tree.children = tree_children
                stack = next + stack[1:]
                tree_stack = tree_children + tree_stack[1:]

    print("\nTree")
    main_tree.do_print()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
