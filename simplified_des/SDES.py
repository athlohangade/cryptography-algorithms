from Operations import Operations

class SDES :
    plaintext_block_size = 8
    key_size = 10
    no_of_rounds = 2
    subkey_initial_permutation = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
    subkey_compression_permutation = (6, 3, 7, 4, 8, 5, 10, 9)
    plaintext_initial_permutation = (2, 6, 3, 1, 4, 8, 5, 7)
    plaintext_expansion_permutation = (4, 1, 2, 3, 2, 3, 4, 1)
    key_shift_values = (1, 2)
    substitution_box_0 =[[1, 0, 3, 2],
                         [3, 2, 1, 0],
                         [0, 2, 1, 3],
                         [3, 1, 3, 2]]
    substitution_box_1 =[[0, 1, 2, 3],
                         [2, 0, 1, 3],
                         [3, 0, 1, 0],
                         [2, 1, 0, 3]]
    right_half_permutation_box = (2, 4, 3, 1)
    inverse_initial_permutation = (4, 1, 3, 5, 7, 2, 8, 6)

    @classmethod
    def __get_permuted_value(cls, data, permutation) :
        permuted_value = []
        for i in permutation :
            permuted_value.append(data[i - 1])
        return("".join(permuted_value))

    @classmethod
    def generate_subkeys(cls, key) :

        # Get the fixed key-length binary represenation of the key
        key = format(key, "0{}b".format(cls.key_size))
        # Apply initial permutation
        permuted_key = cls.__get_permuted_value(key, cls.subkey_initial_permutation)

        # Generate all subkeys iteratively
        all_subkeys = []
        for i in range(cls.no_of_rounds) :

            # Get the left and right half
            left_half = permuted_key[:int(cls.key_size/2)]
            right_half = permuted_key[int(cls.key_size/2):]
            # Circularly shift the left half and the right half
            left_half = format(Operations.circular_left_shift(int(left_half, 2), cls.key_shift_values[i], int(cls.key_size/2)), \
                                "0{}b".format(int(cls.key_size/2)))
            right_half = format(Operations.circular_left_shift(int(right_half, 2), cls.key_shift_values[i], int(cls.key_size/2)), \
                                "0{}b".format(int(cls.key_size/2)))
            # Merge the left and right half
            merged_halfs = left_half + right_half
            # Apply compression permutation and add to list of subkeys
            all_subkeys.append(cls.__get_permuted_value(merged_halfs, cls.subkey_compression_permutation))
            # Use the uncompressed subkey of current round for next round
            permuted_key = merged_halfs

        return all_subkeys

    @classmethod
    def __perform_substitution(cls, data, sub_box) :
        row_number = int(data[0] + data[3], 2)
        column_number = int(data[1] + data[2], 2)
        return format(sub_box[row_number][column_number], "02b")

    @classmethod
    def encrypt(cls, plaintext, keys) :
        permuted_plaintext = []
        for i in plaintext :
            binary_plaintext = format(ord(i), "0{}b".format(cls.plaintext_block_size))
            permuted_plaintext.append(cls.__get_permuted_value(binary_plaintext, cls.plaintext_initial_permutation))

        k = 0
        for key in keys :
            i = 0
            for block in permuted_plaintext :
                left_half = block[:4]
                right_half = block[4:]
                new_left_half = right_half

                right_half = cls.__get_permuted_value(right_half, cls.plaintext_expansion_permutation)
                temp = Operations.xor_operation(int(right_half, 2), int(key, 2))
                right_half = format(temp, "0{}b".format(len(block)))

                right_half = cls.__perform_substitution(right_half[:4], cls.substitution_box_0) + \
                             cls.__perform_substitution(right_half[4:], cls.substitution_box_1)
                right_half = cls.__get_permuted_value(right_half, cls.right_half_permutation_box)

                temp = Operations.xor_operation(int(right_half, 2), int(left_half, 2))
                new_right_half = format(temp, "0{}b".format(int(len(block)/2)))
                if (k == len(keys) - 1) :
                    permuted_plaintext[i] = new_right_half + new_left_half
                else :
                    permuted_plaintext[i] = new_left_half + new_right_half
                i += 1
            k += 1

        ciphertext = []
        for block in permuted_plaintext :
            ciphertext.append(cls.__get_permuted_value(block, cls.inverse_initial_permutation))

        return ciphertext 

    @classmethod
    def decrypt(cls, ciphertext, keys) :
        ciphertext_blocks = []
        i = 0
        while (i < len(ciphertext)) :
            temp = ciphertext[i:i+cls.plaintext_block_size]
            ciphertext_blocks.append(cls.__get_permuted_value(temp, cls.plaintext_initial_permutation))
            i = i + 8

        k = 0
        for key in keys :
            i = 0
            for block in ciphertext_blocks :
                left_half = block[:4]
                right_half = block[4:]
                new_left_half = right_half

                right_half = cls.__get_permuted_value(right_half, cls.plaintext_expansion_permutation)
                temp = Operations.xor_operation(int(right_half, 2), int(key, 2))
                right_half = format(temp, "0{}b".format(len(block)))

                right_half = cls.__perform_substitution(right_half[:4], cls.substitution_box_0) + \
                             cls.__perform_substitution(right_half[4:], cls.substitution_box_1)
                right_half = cls.__get_permuted_value(right_half, cls.right_half_permutation_box)

                temp = Operations.xor_operation(int(right_half, 2), int(left_half, 2))
                new_right_half = format(temp, "0{}b".format(int(len(block)/2)))
                if (k == len(keys) - 1) :
                    ciphertext_blocks[i] = new_right_half + new_left_half
                else :
                    ciphertext_blocks[i] = new_left_half + new_right_half
                i += 1
            k += 1

        plaintext = []
        for block in ciphertext_blocks :
            temp = cls.__get_permuted_value(block, cls.inverse_initial_permutation)
            plaintext.append(chr(int(temp, 2)))
            # plaintext.append(temp)

        return plaintext