import string

def is_palindrome(s):
    s = s.replace(" ", "") # removes spaces
    s = s.lower() # convert to lower case

    reversed_s = s[::-1] #reverses the string

    return s == reversed_s # if they are equal, it's a palindrome


print(is_palindrome("racecar")) # true
print(is_palindrome("hello"))   # false
print(is_palindrome("A man a plan a canal Panama")) # true
