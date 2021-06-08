import time


if __name__ == "__main__":

    print("CAESAR CIPHER")
    print("Decryption")
    print("Enter the cipher-text (Cipher-text should contain only capital alphabets without any spaces) :")

    while True :
        cipher_text = input().strip()
        if cipher_text.isalpha() and cipher_text.isupper() :
            break
        else :
            print("Follow the rules. Cipher-text should contain only capital alphabets without any spaces :")
            print("Enter the cipher-text :")

    print("Enter the n (amount of shift) for generating the key :")
    n = int(input())

    key = "".join([chr(ord('A') + ((i + n) % 26)) for i in range(26)])
    print("Key is :", end = ' ')
    print(key)

    time_required = [0] * 10

    for j in range(10) :
        start_time = time.time()
        plain_text = []
        for i in cipher_text :
            plain_text.append(chr(ord('A') + (ord(i) - ord('A') - n) % 26))
        end_time = time.time()
        time_required[j] = end_time - start_time

    average_time = sum(time_required) / 10
    print("Plain-text is :", end = ' ')
    print("".join(plain_text))
    print("Time required for decryption = %.10f" % (average_time))
