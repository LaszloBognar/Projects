def is_isomorphic(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    s_to_t = {}
    t_to_s = {}

    for i in range(len(s)):
        char_s = s[i]
        char_t = t[i]

        if char_s in s_to_t:
            if s_to_t[char_s] != char_t:
                return False
        elif char_t in t_to_s:
            return False
        else:
            s_to_t[char_s] = char_t
            t_to_s[char_t] = char_s

    return True


# ✅ Quick Tests
print(is_isomorphic("egg", "add"))     # True
print(is_isomorphic("foo", "bar"))     # False
print(is_isomorphic("paper", "title")) # True