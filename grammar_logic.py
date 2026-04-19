def remove_left_recursion(grammar):

    new_grammar = {}

    explanation = ""

    for non_terminal in grammar:

        productions = grammar[non_terminal]

        alpha = []
        beta = []

        for prod in productions:

            if prod.startswith(non_terminal):

                alpha.append(
                    prod[len(non_terminal):].strip()
                )

            else:

                beta.append(prod)

        if alpha:

            new_nt = non_terminal + "'"

            explanation += (
                f"Left recursion detected in {non_terminal}\n"
            )

            new_grammar[non_terminal] = [
                b + " " + new_nt
                for b in beta
            ]

            new_grammar[new_nt] = [
                a + " " + new_nt
                for a in alpha
            ]

            new_grammar[new_nt].append("ε")

        else:

            new_grammar[non_terminal] = productions

    return new_grammar, explanation


def parse_input(text):

    grammar = {}

    lines = text.strip().split("\n")

    for line in lines:

        if "->" in line:

            left, right = line.split("->")

            left = left.strip()

            productions = [
                p.strip()
                for p in right.split("|")
            ]

            grammar[left] = productions

    return grammar


def format_grammar(grammar):

    result = ""

    for nt in grammar:

        result += nt + " -> "

        result += " | ".join(grammar[nt])

        result += "\n"

    return result


def detect_ambiguity(grammar):

    for nt in grammar:

        if len(grammar[nt]) > 2:

            return "⚠️ Possible ambiguity detected"

    return "✅ No obvious ambiguity detected"


def compute_first(grammar):

    first = {}

    for nt in grammar:

        first[nt] = set()

    changed = True

    while changed:

        changed = False

        for nt in grammar:

            for production in grammar[nt]:

                symbols = production.split()

                if not symbols:
                    continue

                first_symbol = symbols[0]

                # Terminal
                if first_symbol not in grammar:

                    if first_symbol not in first[nt]:

                        first[nt].add(first_symbol)

                        changed = True

                # Non-terminal
                else:

                    for sym in first[first_symbol]:

                        if sym not in first[nt]:

                            first[nt].add(sym)

                            changed = True

    return first


def compute_follow(grammar, first):

    follow = {}

    nts = list(grammar.keys())

    for nt in nts:

        follow[nt] = set()

    start_symbol = nts[0]

    follow[start_symbol].add("$")

    changed = True

    while changed:

        changed = False

        for nt in grammar:

            for production in grammar[nt]:

                symbols = production.split()

                for i in range(len(symbols)):

                    symbol = symbols[i]

                    if symbol in grammar:

                        if i + 1 < len(symbols):

                            next_symbol = symbols[i + 1]

                            # Terminal
                            if next_symbol not in grammar:

                                if next_symbol not in follow[symbol]:

                                    follow[symbol].add(next_symbol)

                                    changed = True

                            # Non-terminal
                            else:

                                for sym in first[next_symbol]:

                                    if sym not in follow[symbol]:

                                        follow[symbol].add(sym)

                                        changed = True

                        else:

                            for sym in follow[nt]:

                                if sym not in follow[symbol]:

                                    follow[symbol].add(sym)

                                    changed = True

    return follow


def format_set(data):

    text = ""

    for key in data:

        text += key + " : { "

        text += ", ".join(sorted(data[key]))

        text += " }\n"

    return text