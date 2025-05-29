def reverse_words(s: str) -> str:
    words = s.strip().split()

    reverse_sentence = ' '.join(words[::-1])
    print(reverse_sentence)

    return (reverse_sentence)
reverse_words("The sky is blue")