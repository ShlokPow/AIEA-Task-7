from fol_bc import KnowledgeBase

def main():
    kb = KnowledgeBase()

    kb.add_fact('Parent(John, Mary)')
    kb.add_fact('Parent(Mary, Sam)')
    kb.add_fact('Parent(Susan, John)')
    kb.add_fact('Parent(John, Sam)')
    kb.add_fact('Female(Mary)')
    kb.add_fact('Female(Susan)')

    kb.add_rule('Grandparent(John, Sam)', ['Parent(John, Mary)', 'Parent(Mary, Sam)'])
    kb.add_rule('Grandparent(Susan, Mary)', ['Parent(Susan, John)', 'Parent(John, Mary)'])
    kb.add_rule('Grandparent(Susan, Sam)', ['Parent(Susan, John)', 'Parent(John, Sam)'])
    kb.add_rule('Grandmother(Susan, Sam)', ['Grandparent(Susan, Sam)', 'Female(Susan)'])

    queries = [
        'Grandparent(John, Sam)', 
        'Grandparent(Susan, Mary)',
        'Grandmother(Susan, Sam)',
        'Grandmother(Mary, Sam)',
    ]

    for query in queries:
        result = kb.backward_chain(query)
        print(f"Can we prove '{query}'? {'Yes' if result else 'No'}")

if __name__ == "__main__":
    main()