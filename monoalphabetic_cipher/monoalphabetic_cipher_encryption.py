import time

if __name__ == "__main__":

    print("MONOALPHABETIC CIPHER")
    print("Encryption")
    print("Enter the plain-text (Plain-text should contain only alphabets and spaces) :")

    while True :
        plain_text = input().strip()
        plain_text = plain_text.replace(" ", "")
        if plain_text.isalpha() :
            break
        else :
            print("Follow the rules. Plain-text should contain only alphabets")
            print("Enter the plain-text :")

    print("Enter the key (key must be in capital alphabets with all unique letters and length should be 26) :")
    while True :
        key = input().strip()
        if len(set(key)) == 26 and key.isupper() :
            break
        else :
            print("Follow the rules. Key must be in capital alphabets with all unique letters and length should be 26 :")
            print("Enter a valid key:")

    time_required = [0] * 10

    for j in range(10) :
        start_time = time.time()
        cipher_text = []
        for i in plain_text.upper() :
            cipher_text.append(key[ord(i) - ord('A')])
        end_time = time.time()
        time_required[j] = end_time - start_time

    average_time = sum(time_required) / 10
    print("Cipher-text is :", end = ' ')
    print("".join(cipher_text))
    print("Time required for encryption = %.10f" % (average_time))