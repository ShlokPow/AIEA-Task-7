# Assignment 4 - FOL Backward Chaining

This assignment implements a simple backward chaining system for reasoning in First Order Logic.

## Running the example

Execute `fol_test.py` to see sample queries evaluated against the knowledge base:

```bash
python3 fol_test.py
```

Example output:

```
Query: SeniorManager(Alice, Carol)
Yes: SeniorManager(Alice, Carol)

Query: HRManager(Bob)
No.

Query: Grandparent(Susan, ?Who)
Yes: Grandparent(Susan, Mary)
```

Each query prints `Yes` followed by the resolved atom when the goal can be proven. The final example shows that variables written with ``?`` are allowed in queries to ask for all matching results. A ``No.`` line indicates the query could not be proven.
