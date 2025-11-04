def contains_duplicates(nums):
    """
    given an array of numbers return true if there are duplicates
    """
    s1 = set(nums)
    if len(s1) != len(nums):
        return True
    return False


n1 = [1, 2, 3, 1]
n2 = [1, 2, 3, 4]
n3 = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]

print(contains_duplicates(n1))

print(contains_duplicates(n2))

print(contains_duplicates(n3))
