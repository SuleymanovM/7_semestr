# Large Prime Generation for RSA
import random


class BigPrimes:
    size_of_num: int  # Размер числа в битах
    #Это список заранее сгенерированных простых чисел.
    first_primes_list: list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                               31, 37, 41, 43, 47, 53, 59, 61, 67,
                               71, 73, 79, 83, 89, 97, 101, 103,
                               107, 109, 113, 127, 131, 137, 139,
                               149, 151, 157, 163, 167, 173, 179,
                               181, 191, 193, 197, 199, 211, 223,
                               227, 229, 233, 239, 241, 251, 257,
                               263, 269, 271, 277, 281, 283, 293,
                               307, 311, 313, 317, 331, 337, 347, 349]  # Pre generated primes

    def generate(self, size):
        self.size_of_num = size
        while True:
            prime_candidate = self.get_low_level_prime()
            if not self.is_miller_rabin_passed(prime_candidate):
                continue
            else:
                return prime_candidate

    def n_bit_random(self):
        return random.randrange(2 ** (self.size_of_num - 1) + 1, 2 ** self.size_of_num - 1)

    def get_low_level_prime(self):
        '''Generate a prime candidate divisible
        by first primes'''
        while True:
            # Obtain a random number
            pc = self.n_bit_random()

            # Test divisibility by pre-generated
            # primes
            for divisor in self.first_primes_list:
                if pc % divisor == 0 and divisor ** 2 <= pc:
                    break
            else:
                return pc

    @staticmethod
    def is_miller_rabin_passed(mrc):
        '''Run 20 iterations of Rabin Miller Primality test'''
        max_divisions_by_two = 0
        ec = mrc - 1
        while ec % 2 == 0:
            ec >>= 1
            max_divisions_by_two += 1
        assert (2 ** max_divisions_by_two * ec == mrc - 1)

        def trial_composite(round_tester):
            if pow(round_tester, ec, mrc) == 1:
                return False
            for i in range(max_divisions_by_two):
                if pow(round_tester, 2 ** i * ec, mrc) == mrc - 1:
                    return False
            return True

        # Set number of trials here
        number_of_rabin_trials = 20
        for i in range(number_of_rabin_trials):
            round_test = random.randrange(2, mrc)
            if trial_composite(round_test):
                return False
        return True


if __name__ == '__main__':
    big_prime = BigPrimes().generate(160)
    print(big_prime)
