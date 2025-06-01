def set_difference_builtin(set1: set, set2: set) -> set:
            """
            Calculates the set difference (set1 - set2) using Python's built-in
            set difference operator.

            Args:
                set1: The first set.
                set2: The second set.

            Returns:
                A new set containing elements that are in set1 but not in set2.
            """
            return set1 - set2

def set_difference_method(set1: set, set2: set) -> set:
            """
            Calculates the set difference (set1 - set2) using Python's built-in
            difference() method.

            Args:
                set1: The first set.
                set2: The second set.

            Returns:
                A new set containing elements that are in set1 but not in set2.
            """
            return set1.difference(set2)

        # --- Examples ---
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}
set_c = {1, 2, 3}
set_d = {10, 11}

print(f"Set A: {set_a}")
print(f"Set B: {set_b}")
print(f"Set C: {set_c}")
print(f"Set D: {set_d}\n")

        # Using the '-' operator
diff1 = set_difference_builtin(set_a, set_b)
print(f"A - B (operator): {diff1} (Elements in A but not in B)") # Expected: {1, 2, 3}

diff2 = set_difference_builtin(set_b, set_a)
print(f"B - A (operator): {diff2} (Elements in B but not in A)") # Expected: {6, 7, 8}

diff3 = set_difference_builtin(set_a, set_c)
print(f"A - C (operator): {diff3} (C is a subset of A)")       # Expected: {4, 5}

diff4 = set_difference_builtin(set_a, set_d)
print(f"A - D (operator): {diff4} (No common elements)")    # Expected: {1, 2, 3, 4, 5}

        # Using the 'difference()' method
diff5 = set_difference_method(set_a, set_b)
print(f"A.difference(B) (method): {diff5}") # Expected: {1, 2, 3}
