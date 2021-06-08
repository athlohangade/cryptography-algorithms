import time


if __name__ == "__main__":

    print("MONOALPHABETIC CIPHER")
    print("Decryption")
    print("Enter the cipher-text (Cipher-text should contain only capital alphabets without any spaces) :")

    while True :
        cipher_text = input().strip()
        if cipher_text.isalpha() and cipher_text.isupper() :
            break
        else :
            print("Follow the rules. Cipher-text should contain only capital alphabets without any spaces :")
            print("Enter the cipher-text :")

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
        plain_text = []
        for i in cipher_text :
            plain_text.append(chr(ord('A') + key.index(i)))
        end_time = time.time()
        time_required[j] = end_time - start_time

    average_time = sum(time_required) / 10
    print("Plain-text is :", end = ' ')
    print("".join(plain_text))
    print("Time required for decryption = %.10f" % (average_time))