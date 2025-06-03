from collections import defaultdict

class KnowledgeBase:
    def __init__(self):
        self.facts = set()
        self.rules = defaultdict(list)

    def add_fact(self, fact):
        self.facts.add(fact)

    def add_rule(self, conclusion, premises):
        self.rules[conclusion].append(premises)

    def backward_chain(self, goal, visited=None):
        if visited is None:
            visited = set()
        if goal in self.facts:
            return True
        if goal in visited:
            return False
        visited.add(goal)
        for premises in self.rules.get(goal, []):
            if all(self.backward_chain(premise, visited) for premise in premises):
                self.facts.add(goal)
                return True
        return False
