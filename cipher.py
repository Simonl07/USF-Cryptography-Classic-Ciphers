import argparse

base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="Either 'encrypt' or 'decrypt' the given fiel")
    parser.add_argument("text", help="the input file to be encrypted")
    parser.add_argument("algorithm", help="caesar/vigenere")
    parser.add_argument("key", help="The key for the corresponded algorithm")
    args = parser.parse_args()

    algo_map = {
        'caesar': Caesar,
        'vigenere': Vigenere,
        'wolseley': Wolseley
    }
    cipher = algo_map[args.algorithm]()

    print(getattr(cipher, args.mode)(args.text, args.key))



class SubstitutionCipher:
    base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self):
        self.permutation = SubstitutionCipher.base

    def encrypt(self, c):
        if c in base:
            return self.permutation[SubstitutionCipher.base.index(c)]
        else:
            return c

    def decrypt(self, c):
        if c in self.permutation:
            return SubstitutionCipher.base[self.permutation.index(c)]
        else:
            return c

    def rotateLeft(string, offset):
        return string[offset:] + string[:offset]

    def rotateRight(string, offset):
        return string[len(string) - offset:] + string[:len(string) - offset]

class Caesar(SubstitutionCipher):
    def __init__(self):
        self.permutation = SubstitutionCipher.rotateLeft(SubstitutionCipher.base, 3)

    def encrypt(self, text, key):
        output = ""
        for c in text:
            output += SubstitutionCipher.encrypt(self, c)
        return output

    def decrypt(self, text, key):
        output = ""
        for c in text:
            output += SubstitutionCipher.decrypt(self, c)
        return output

class Vigenere(SubstitutionCipher):

    def encrypt(self, text, key):
        output = ""
        index = 0
        for c in text:
            rotate_amount = SubstitutionCipher.base.index(key[index])
            index = (index + 1) % len(key)
            self.permutation = SubstitutionCipher.rotateLeft(SubstitutionCipher.base, rotate_amount)
            output += SubstitutionCipher.encrypt(self, c)
        return output

    def decrypt(self, text, key):
        output = ""
        index = 0
        for c in text:
            rotate_amount = SubstitutionCipher.base.index(key[index])
            index = (index + 1) % len(key)
            self.permutation = SubstitutionCipher.rotateLeft(SubstitutionCipher.base, rotate_amount)
            output += SubstitutionCipher.decrypt(self, c)
        return output

class Wolseley(SubstitutionCipher):

    def setup_permutation(key):
        grid = []
        rest = SubstitutionCipher.base
        for c in key:
            grid.append(c)
            rest = rest.replace(c, "")
            if c == 'I' or c == 'J':
                rest = rest.replace("I", "")
                rest = rest.replace("J", "")
        grid += rest

        permutation = ""
        for alpha in SubstitutionCipher.base:
            if alpha == "I" or alpha == "J":
                if "I" in grid:
                    permutation += (grid[24 - grid.index("I")])
                else:
                    permutation += (grid[24 - grid.index("J")])
            else:
                permutation += (grid[24 - grid.index(alpha)])

        return permutation

    def encrypt(self, text, key):
        self.permutation = Wolseley.setup_permutation(key)
        output = ""
        for c in text:
            output += SubstitutionCipher.encrypt(self, c)
        return output


    def decrypt(self, text, key):
        self.permutation = Wolseley.setup_permutation(key)
        output = ""
        for c in text:
            output += SubstitutionCipher.decrypt(self, c)
        return output



if __name__ == "__main__":
    main()
