from flask import Flask, render_template, request

# Import functions explicitly (removes yellow warnings)

from grammar_logic import (
    parse_input,
    remove_left_recursion,
    format_grammar,
    detect_ambiguity,
    compute_first,
    compute_follow,
    format_set
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    original = ""
    transformed = ""
    ambiguity = ""
    first = ""
    follow = ""
    explanation = ""

    if request.method == "POST":

        original = request.form.get("grammar", "")

        grammar = parse_input(original)

        # Remove left recursion
        new_grammar, explanation = remove_left_recursion(grammar)

        transformed = format_grammar(new_grammar)

        # Detect ambiguity
        ambiguity = detect_ambiguity(grammar)

        # Compute FIRST
        first_sets = compute_first(grammar)

        # Compute FOLLOW
        follow_sets = compute_follow(grammar, first_sets)

        # Format output
        first = format_set(first_sets)

        follow = format_set(follow_sets)

    return render_template(
        "index.html",
        original=original,
        transformed=transformed,
        ambiguity=ambiguity,
        first=first,
        follow=follow,
        explanation=explanation
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)