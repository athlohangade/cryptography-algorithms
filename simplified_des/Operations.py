class Operations :

    @classmethod
    def modulo_operation(cls, a, b) :
        return a % b

    @classmethod
    def xor_operation(cls, a, b) :
        return a ^ b

    @classmethod
    def shift_operation(cls, a, b, direction = 'left') :
        if direction == "left" :
            return a << b
        elif direction == "right" :
            return a >> b
        else :
            print("Mention the direction as either 'left' or 'right' !!")
            return a

    @classmethod
    def gcd_using_euclidean(cls, a, b) :
        a, b = abs(a), abs(b)
        if a < b :
            a, b = b, a

        remainder = gcd = b
        while (remainder != 0) :
            gcd = remainder
            remainder = a % b
            a = b
            b = remainder

        return gcd

    @classmethod
    def circular_left_shift(cls, num, shift_amount, size_of_shift_register) :
        binary_rep = "{0:0{1}b}".format(num, size_of_shift_register)
        shift_amount = shift_amount % size_of_shift_register
        ans = binary_rep[shift_amount:] + binary_rep[:shift_amount]
        return int(ans, 2)