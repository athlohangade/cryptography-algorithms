from SDES import SDES
import time

if __name__ == "__main__":

    # Input the plaintext
    print("Enter the plaintext ; ")
    plaintext = input().rstrip()
    # Input the key 
    print("Enter the key. Value should be in range 0 to {} as the key size is {}".format(2 ** SDES.key_size - 1, SDES.key_size))
    key = int(input())
    if (key < 0) or (key > (2 ** SDES.key_size - 1)) :
        print("Follow the rules for the key")
        exit(1)

    print("Length of Text : ", len(plaintext))
    print("Encrypting...")
    start_time = time.time()
    # Generate all the subkeys
    ciphertext_hex = []
    subkeys = SDES.generate_subkeys(key)
    ciphertext = SDES.encrypt(plaintext, subkeys)
    for i in ciphertext :
        ciphertext_hex.append("{:02x}".format(int(i, 2)))
    ciphertext_hex = " ".join(ciphertext_hex)
    time_required = time.time() - start_time
    print("Ciphertext : ", ciphertext_hex)
    print("Time required for encryption :", time_required)
    ciphertext = "".join(ciphertext)
    print(ciphertext)

    print("Decrypting...")
    start_time = time.time()
    subkeys = SDES.generate_subkeys(key)
    subkeys.reverse()
    plaintext = SDES.decrypt(ciphertext, subkeys)
    plaintext = "".join(plaintext)
    time_required = time.time() - start_time
    print("Plaintext : ", plaintext)
    print("Time required for decryption :", time_required)
