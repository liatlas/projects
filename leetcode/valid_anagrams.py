def valid_anagram(s, t):

    if len(s) != len(t):

        return False

    count_t = [0] * 26
    count_s = [0] * 26
    for i in range(len(s)):

        count_t[ord(t[i]) - ord('a')] += 1
        count_s[ord(s[i]) - ord('a')] += 1

    return count_t == count_s


s1 = "car"
s2 = "rat"

e1 = "race"
e2 = "crae"
print(valid_anagram(s1, s2))
print(valid_anagram(e1, e2))
