from SAES import SAES
import time

if __name__ == "__main__":

    # Input the plaintext
    print("Enter the plaintext :")
    plaintext = input().rstrip()
    # Input the key 
    print("Enter the key. Value should be in range 0 to {} as the key size is {}".format(
        2 ** SAES.key_size - 1, SAES.key_size))
    key = int(input())
    if (key < 0) or (key > (2 ** SAES.key_size - 1)) :
        print("Follow the rules for the key")
        exit(1)

    print("Length of Text : ", len(plaintext))
    print("Encrypting...")

    # Generate all the subkeys
    subkeys = SAES.generate_subkeys(key)

    encryption_time = [0] * 10
    for i in range(10) :
        encryption_time[i] = time.time()
        # Perform Encryption
        ciphertext = SAES.encrypt(plaintext, subkeys)
        encryption_time[i] = time.time() - encryption_time[i]
    avg_encryption_time = sum(encryption_time) / 10

    ciphertext_hex = []
    for i in ciphertext :
        ciphertext_hex.append("{:04X}".format(int(i, 2)))
    print("Ciphertext : ", " ".join(ciphertext_hex))
    print("Encryption time : ", avg_encryption_time)

    # Reverse the keys
    subkeys[0], subkeys[4] = subkeys[4], subkeys[0]
    subkeys[1], subkeys[5] = subkeys[5], subkeys[1]

    print("Decrypting ...")
    decryption_time = [0] * 10
    for i in range(10) :
        decryption_time[i] = time.time()
        # Perform Decryption
        plaintext_blocks = SAES.decrypt(ciphertext_hex, subkeys)
        decryption_time[i] = time.time() - decryption_time[i]
    avg_decryption_time = sum(decryption_time) / 10

    plaintext = []
    for i in plaintext_blocks :
        plaintext.append(chr(int(i[:8], 2)))
        plaintext.append(chr(int(i[8:], 2)))
    print("Plaintext : ", "".join(plaintext))
    print("Decryption time : ", avg_decryption_time)
