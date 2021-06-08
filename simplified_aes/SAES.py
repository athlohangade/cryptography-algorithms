from Operations import Operations
class SAES :

    plaintext_block_size = 16
    key_size = 16
    no_of_rounds = 2
    substitution_box = {
        '0000': '1001', 
        '0001': '0100',
        '0010': '1010',
        '0011': '1011',
        '0100': '1101',
        '0101': '0001',
        '0110': '1000',
        '0111': '0101',
        '1000': '0110',
        '1001': '0010',
        '1010': '0000',
        '1011': '0011',
        '1100': '1100',
        '1101': '1110',
        '1110': '1111',
        '1111': '0111',
    }
    inv_substitution_box = {
        '1001': '0000', 
        '0100': '0001',
        '1010': '0010',
        '1011': '0011',
        '1101': '0100',
        '0001': '0101',
        '1000': '0110',
        '0101': '0111',
        '0110': '1000',
        '0010': '1001',
        '0000': '1010',
        '0011': '1011',
        '1100': '1100',
        '1110': '1101',
        '1111': '1110',
        '0111': '1111',
    }

    mix_column_table = {
        '2': '02468ACE3175B9FD',
        '4': '048C37BF62EA51D9',
        '9': '09182B3A4D5C6F7E'
    }
    mix_column_matrix = [[1, 4], [4, 1]]
    inv_mix_column_matrix = [[9, 2], [2, 9]]
    round_constants = ['80', '30']
    is_padded = False

    @classmethod
    def __perform_substitution(cls, data, substitution_box) :
        binary_rep = "{:08b}".format(data)
        ans = cls.substitution_box[binary_rep[:4]] + cls.substitution_box[binary_rep[4:]]
        return int(ans, 2)

    @classmethod
    def generate_subkeys(cls, key) :
        binary_rep = "{:016b}".format(key)
        subkeys = []
        subkeys.append(int(binary_rep[:8], 2))
        subkeys.append(int(binary_rep[8:], 2))

        for i in range(cls.no_of_rounds) :
            temp = Operations.circular_left_shift(subkeys[-1], 4, 8)
            temp = cls.__perform_substitution(temp, cls.substitution_box)
            temp = Operations.xor_operation(temp, int(cls.round_constants[i], 16))
            key1 = Operations.xor_operation(temp, subkeys[-2])
            subkeys.append(key1)
            key2 = Operations.xor_operation(subkeys[-2], subkeys[-1])
            subkeys.append(key2)
            
        return subkeys
            

    @classmethod
    def __initial_round(cls, plaintext_blocks, keys) :
        joint_key = int("{:08b}".format(keys[0]) + "{:08b}".format(keys[1]), 2)
        result_blocks = []
        for i in plaintext_blocks :
            xored = Operations.xor_operation(int(i, 2), joint_key)
            xored = "{:016b}".format(xored)
            result_blocks.append(xored)
        
        return result_blocks

    @classmethod
    def __convert_into_matrix(cls, plaintext_blocks) :
        plaintext_matrix = []
        for i in range(len(plaintext_blocks)) :
            plaintext_matrix.append([[0, 0], [0, 0]])

        for i in range(len(plaintext_blocks)) :
            plaintext_matrix[i][0][0] = plaintext_blocks[i][:4]
            plaintext_matrix[i][1][0] = plaintext_blocks[i][4:8]
            plaintext_matrix[i][0][1] = plaintext_blocks[i][8:12]
            plaintext_matrix[i][1][1] = plaintext_blocks[i][12:]
        return plaintext_matrix

    @classmethod
    def __perform_encryption_round(cls, plaintext_blocks, keys, round_number) :

        b0 = (keys[0] & 0xF0) >> 4
        b1 = keys[0] & 0x0F
        b2 = (keys[1] & 0xF0) >> 4
        b3 = keys[1] & 0x0F

        # Subsitution
        for i in range(len(plaintext_blocks)) :
            plaintext_blocks[i][0][0] = int(cls.substitution_box[plaintext_blocks[i][0][0]], 2)
            plaintext_blocks[i][1][0] = int(cls.substitution_box[plaintext_blocks[i][1][0]], 2)
            plaintext_blocks[i][0][1] = int(cls.substitution_box[plaintext_blocks[i][0][1]], 2)
            plaintext_blocks[i][1][1] = int(cls.substitution_box[plaintext_blocks[i][1][1]], 2)

        # Shift Rows
        for i in range(len(plaintext_blocks)) :
            plaintext_blocks[i][1][0], plaintext_blocks[i][1][1] = \
                plaintext_blocks[i][1][1], plaintext_blocks[i][1][0]

        # Mix columns
        if round_number == 1 :
            for i in range(len(plaintext_blocks)) :
                first_operand = plaintext_blocks[i][0][0]
                second_operand = int(cls.mix_column_table['4'][plaintext_blocks[i][1][0]], 16)
                val1 = Operations.xor_operation(first_operand, second_operand)

                first_operand = plaintext_blocks[i][0][1]
                second_operand = int(cls.mix_column_table['4'][plaintext_blocks[i][1][1]], 16)
                val2 = Operations.xor_operation(first_operand, second_operand)

                first_operand = int(cls.mix_column_table['4'][plaintext_blocks[i][0][0]], 16)
                second_operand = plaintext_blocks[i][1][0]
                val3 = Operations.xor_operation(first_operand, second_operand)

                first_operand = int(cls.mix_column_table['4'][plaintext_blocks[i][0][1]], 16)
                second_operand = plaintext_blocks[i][1][1]
                val4 = Operations.xor_operation(first_operand, second_operand)
    
                plaintext_blocks[i][0][0] = val1
                plaintext_blocks[i][0][1] = val2
                plaintext_blocks[i][1][0] = val3
                plaintext_blocks[i][1][1] = val4

        # Add round key
        for i in range(len(plaintext_blocks)) :
            plaintext_blocks[i][0][0] = "{:04b}".format(Operations.xor_operation( \
                plaintext_blocks[i][0][0], b0))
            plaintext_blocks[i][1][0] = "{:04b}".format(Operations.xor_operation( \
                plaintext_blocks[i][1][0], b1))
            plaintext_blocks[i][0][1] = "{:04b}".format(Operations.xor_operation( \
                plaintext_blocks[i][0][1], b2))
            plaintext_blocks[i][1][1] = "{:04b}".format(Operations.xor_operation( \
                plaintext_blocks[i][1][1], b3))

        return plaintext_blocks

    @classmethod
    def encrypt(cls, plaintext, keys) :
        if len(plaintext) % 2 :
            plaintext = plaintext + '0'
            cls.is_padded = True
        
        plaintext_blocks = []
        for i in range(0, len(plaintext), 2) :
            temp = "{:08b}".format(ord(plaintext[i])) + "{:08b}".format(ord(plaintext[i + 1]))
            plaintext_blocks.append(temp)

        plaintext_blocks = cls.__initial_round(plaintext_blocks, keys[0:2])
        plaintext_matrix = cls.__convert_into_matrix(plaintext_blocks)
        plaintext_matrix = cls.__perform_encryption_round(plaintext_matrix, keys[2:4], 1)
        plaintext_matrix = cls.__perform_encryption_round(plaintext_matrix, keys[4:], 2)
        
        ciphertext = []
        for i in plaintext_matrix :
            x = i[0][0]+ i[1][0] + i[0][1] + i[1][1]
            ciphertext.append(x)
        return ciphertext

        
    @classmethod
    def __perform_decryption_round(cls, ciphertext_matrix, keys, round_number) :
        b0 = (keys[0] & 0xF0) >> 4
        b1 = keys[0] & 0x0F
        b2 = (keys[1] & 0xF0) >> 4
        b3 = keys[1] & 0x0F

        # Inverse shift rows
        for i in range(len(ciphertext_matrix)) :
            ciphertext_matrix[i][1][0], ciphertext_matrix[i][1][1] = \
                ciphertext_matrix[i][1][1], ciphertext_matrix[i][1][0]

        # Inverse Substitution
        for i in range(len(ciphertext_matrix)) :
            ciphertext_matrix[i][0][0] = int(cls.inv_substitution_box[ciphertext_matrix[i][0][0]], 2)
            ciphertext_matrix[i][1][0] = int(cls.inv_substitution_box[ciphertext_matrix[i][1][0]], 2)
            ciphertext_matrix[i][0][1] = int(cls.inv_substitution_box[ciphertext_matrix[i][0][1]], 2)
            ciphertext_matrix[i][1][1] = int(cls.inv_substitution_box[ciphertext_matrix[i][1][1]], 2)

        # Add round key
        for i in range(len(ciphertext_matrix)) :
            ciphertext_matrix[i][0][0] = Operations.xor_operation(ciphertext_matrix[i][0][0], b0)
            ciphertext_matrix[i][1][0] = Operations.xor_operation(ciphertext_matrix[i][1][0], b1)
            ciphertext_matrix[i][0][1] = Operations.xor_operation(ciphertext_matrix[i][0][1], b2)
            ciphertext_matrix[i][1][1] = Operations.xor_operation(ciphertext_matrix[i][1][1], b3)

        # Inverse mix columns
        if round_number == 1 :
            for i in range(len(ciphertext_matrix)) :
                first_operand = int(cls.mix_column_table['9'][ciphertext_matrix[i][0][0]], 16)
                second_operand = int(cls.mix_column_table['2'][ciphertext_matrix[i][1][0]], 16)
                val1 = Operations.xor_operation(first_operand, second_operand)

                first_operand = int(cls.mix_column_table['9'][ciphertext_matrix[i][0][1]], 16)
                second_operand = int(cls.mix_column_table['2'][ciphertext_matrix[i][1][1]], 16)
                val2 = Operations.xor_operation(first_operand, second_operand)

                first_operand = int(cls.mix_column_table['2'][ciphertext_matrix[i][0][0]], 16)
                second_operand = int(cls.mix_column_table['9'][ciphertext_matrix[i][1][0]], 16)
                val3 = Operations.xor_operation(first_operand, second_operand)

                first_operand = int(cls.mix_column_table['2'][ciphertext_matrix[i][0][1]], 16)
                second_operand = int(cls.mix_column_table['9'][ciphertext_matrix[i][1][1]], 16)
                val4 = Operations.xor_operation(first_operand, second_operand)
    
                ciphertext_matrix[i][0][0] = val1
                ciphertext_matrix[i][0][1] = val2
                ciphertext_matrix[i][1][0] = val3
                ciphertext_matrix[i][1][1] = val4

        for i in range(len(ciphertext_matrix)) :
            ciphertext_matrix[i][0][0] = "{:04b}".format(ciphertext_matrix[i][0][0])
            ciphertext_matrix[i][1][0] = "{:04b}".format(ciphertext_matrix[i][1][0])
            ciphertext_matrix[i][0][1] = "{:04b}".format(ciphertext_matrix[i][0][1])
            ciphertext_matrix[i][1][1] = "{:04b}".format(ciphertext_matrix[i][1][1])

        return ciphertext_matrix


    @classmethod
    def decrypt(cls, ciphertext, keys) :
        ciphertext_blocks = []
        for i in ciphertext :
            ciphertext_blocks.append("{:016b}".format(int(i, 16)))

        ciphertext_blocks = SAES.__initial_round(ciphertext_blocks, keys[0:2])
        ciphertext_matrix = SAES.__convert_into_matrix(ciphertext_blocks)
        ciphertext_matrix = SAES.__perform_decryption_round(ciphertext_matrix, keys[2:4], 1)
        plaintext_matrix = SAES.__perform_decryption_round(ciphertext_matrix, keys[4:], 2)

        plaintext = []
        for i in plaintext_matrix :
            x = i[0][0]+ i[1][0] + i[0][1] + i[1][1]
            plaintext.append(x)

        if cls.is_padded :
            plaintext[-1] = plaintext[-1][:-7]

        return plaintext