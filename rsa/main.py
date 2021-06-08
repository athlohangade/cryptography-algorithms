from RSA import RSA
import time

if __name__ == "__main__":

    print("RSA Algorithm")
    print("Enter the plaintext string : ", end="")
    plaintext = input().rstrip()
    print("Length of plaintext : ", len(plaintext))

    print("\n", "Enter the numbers p and q such that both are prime numbers and their \
product should be equal to or greater than 256", sep="")
    while 1 : 
        print("Enter the number 'p' such that it should be a prime number : ", end="")
        p = int(input())
        if RSA.is_prime(p) :
            break
        else :
            print("Follow the rules. 'p' should be prime")
    while 1 : 
        print("Enter the number 'q' such that it should be a prime number and is not equal to 'p' : ",end="")
        q = int(input())
        if RSA.is_prime(q) and p != q:
            break
        else :
            print("Follow the rules. 'q' should be prime")

    if (p * q) < 256 :
        print("The product of 'p' and 'q' should be atleast 256")
        exit(1)

    print("\n", "Encryption...", sep="")
    time_required = []
    start_time = time.time()
    for i in range(10) :
        ciphertext = RSA.rsa_encryption(plaintext, p, q)
        time_required.append(time.time() - start_time)
    avg_time = sum(time_required) / 10
    print("Ciphertext : ", " ".join([str(i) for i in ciphertext]))
    print("Encryption Time : ", avg_time)

    print("\n", "Decryption...", sep="")
    time_required = []
    start_time = time.time()
    for i in range(10) :
        plaintext = RSA.rsa_decryption(ciphertext, p, q)
        time_required.append(time.time() - start_time)
    avg_time = sum(time_required) / 10
    print("Plaintext : ", "".join(plaintext))
    print("Decryption Time : ", avg_time)
