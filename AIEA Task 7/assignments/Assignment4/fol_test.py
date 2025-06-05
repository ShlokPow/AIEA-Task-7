from fol_bc import KnowledgeBase
from fol_bc import parse_literal, resolve_value

def format_result(query, subst):
    qname, qargs = parse_literal(query)
    resolved = [resolve_value(subst.get(arg, arg), subst) for arg in qargs]
    return f"{qname}({', '.join(resolved)})"

def main():
    kb = KnowledgeBase()

    kb.add_fact("Parent(John, Mary)")
    kb.add_fact("Parent(Mary, Sam)")
    kb.add_fact("Parent(Susan, John)")
    kb.add_fact("Female(Susan)")
    kb.add_fact("Female(Mary)")

    kb.add_rule("Grandparent(X, Z)", ["Parent(X, Y)", "Parent(Y, Z)"])
    kb.add_rule("Grandmother(X, Z)", ["Grandparent(X, Z)", "Female(X)"])

    kb.add_fact("Manager(Alice, Bob)")
    kb.add_fact("Manager(Bob, Carol)")
    kb.add_fact("Department(Bob, HR)")

    kb.add_rule("SeniorManager(X, Z)", ["Manager(X, Y)", "Manager(Y, Z)"])
    kb.add_rule("HRManager(X)", ["Manager(X, Y)", "Department(Y, HR)"])

    kb.add_fact("Mammal(Dog)")
    kb.add_fact("HasFur(Dog)")
    kb.add_fact("HasFur(Cat)")
    kb.add_fact("LaysEggs(Duck)")

    kb.add_rule("WarmBlooded(X)", ["Mammal(X)"])
    kb.add_rule("Animal(X)", ["Mammal(X)"])
    kb.add_rule("Animal(X)", ["LaysEggs(X)"])

    queries = [
        # Constant queries
        "Grandparent(Susan, Sam)",
        "Grandmother(Susan, Sam)",
        "Grandmother(Mary, Sam)",

        "SeniorManager(Alice, Carol)",
        "HRManager(Alice)",
        "HRManager(Bob)",

        "WarmBlooded(Dog)",
        "Animal(Cat)",
        "Animal(Duck)",
        "WarmBlooded(Duck)",

        # Examples with variables using ? notation
        "Grandparent(Susan, ?Who)",
        "Grandparent(?X, Sam)",
        "HRManager(?Mgr)",
    ]

    for query in queries:
        results = kb.backward_chain(query)
        print(f"\nQuery: {query}")
        if results:
            seen = set()
            for res in results:
                output = format_result(query, res)
                if output not in seen:
                    print("Yes:", output)
                    seen.add(output)
        else:
            print("No.")

if __name__ == "__main__":
    main()
