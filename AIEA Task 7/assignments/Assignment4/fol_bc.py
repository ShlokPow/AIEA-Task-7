import re
from collections import defaultdict

def parse_literal(literal):
    """Parse a predicate string into a (name, args) tuple.

    This parser accepts optional whitespace and variables that may be
    written either as single upper-case letters or with a leading
    question mark, e.g. ``?X``.
    """
    match = re.match(r"\s*(\w+)\s*\((.*)\)\s*", literal)
    if not match:
        raise ValueError(f"Invalid literal: {literal}")
    name, args = match.groups()
    arg_list = []
    for arg in re.split(r"\s*,\s*", args):
        if arg:
            arg_list.append(arg.strip())
    return (name, arg_list)

def stringify_literal(lit):
    name, args = lit
    return f"{name}({', '.join(args)})"

def is_variable(token):
    """Return True if the token represents a logic variable."""

    # Either a token beginning with '?' (e.g. ``?X``) or a single upper-case
    # letter is treated as a variable.  This allows expressive variable names
    # while still supporting the simpler ``X`` style used previously.
    return token.startswith('?') or (len(token) == 1 and token.isupper())

def unify(x, y, theta):
    if theta is None:
        return None
    if x == y:
        return theta
    if isinstance(x, str) and is_variable(x):
        return unify_var(x, y, theta)
    if isinstance(y, str) and is_variable(y):
        return unify_var(y, x, theta)
    if isinstance(x, tuple) and isinstance(y, tuple):
        if x[0] != y[0] or len(x[1]) != len(y[1]):
            return None
        for a, b in zip(x[1], y[1]):
            theta = unify(a, b, theta)
            if theta is None:
                return None
        return theta
    return None

def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif x in theta:
        return unify(var, theta[x], theta)
    else:
        theta[var] = x
        return theta

def resolve_value(val, theta):
    """Recursively resolve ``val`` through the substitution ``theta``."""
    while isinstance(val, str) and val in theta:
        val = theta[val]
    return val


def apply_substitution(literal, theta):
    name, args = literal
    new_args = [resolve_value(arg, theta) for arg in args]
    return (name, new_args)


class KnowledgeBase:
    def __init__(self):
        self.facts = []
        self.rules = []

    def add_fact(self, fact):
        self.facts.append(parse_literal(fact))

    def add_rule(self, head, body):
        head = parse_literal(head)
        body = [parse_literal(b) for b in body]
        self.rules.append((head, body))

    def backward_chain(self, goal, theta=None, visited=None):
        if theta is None:
            theta = {}
        if visited is None:
            visited = set()

        goal_parsed = parse_literal(goal)
        goal_key = apply_substitution(goal_parsed, theta)
        visited_key = repr(goal_key)

        if visited_key in visited:
            return []
        visited.add(visited_key)

        answers = []

        for fact in self.facts:
            unify_theta = unify(goal_key, fact, theta.copy())
            if unify_theta is not None:
                answers.append(unify_theta)

        for head, body in self.rules:
            unify_theta = unify(goal_key, head, theta.copy())
            if unify_theta is not None:
                sub_answers = [unify_theta]
                for b in body:
                    new_sub_answers = []
                    for sub in sub_answers:
                        results = self.backward_chain(stringify_literal(b), sub.copy(), visited.copy())
                        new_sub_answers.extend(results)
                    sub_answers = new_sub_answers
                answers.extend(sub_answers)

        return answers