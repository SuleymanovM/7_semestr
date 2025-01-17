import random
from math import sqrt


class Solution:
    sequence: list
    k: float = 1.82138636

    def __init__(self, sequence: list = None, length: int = 10000):
        self.sequence = self.gen_sequence(length) if sequence is None else sequence

    def gen_sequence(self, length: int) -> list:
        self.sequence = [random.randint(0, 1) for _ in range(length)]
        return self.sequence

    def frequency_test(self) -> bool:
        new_sequence = list(map(lambda x: -1 if x == 0 else 1, self.sequence))
        stat = abs(sum(new_sequence)) / sqrt(len(new_sequence))
        return True if stat <= self.k else False

    def get_v(self):
        res = []
        for i in range(len(self.sequence) - 1):
            if self.sequence[i] == self.sequence[i + 1]:
                res.append(0)
            else:
                res.append(1)
        return sum(res) + 1

    def identical_bits_test(self) -> bool:
        freq = (1 / len(self.sequence)) * self.sequence.count(1)
        try:
            stat = ((abs(self.get_v() - 2 * len(self.sequence) * freq * (1 - freq))) /
                    (2 * sqrt(2 * len(self.sequence)) * freq * (1 - freq)))
        except ZeroDivisionError:
            return False
        return True if stat <= self.k else False

    def extended_test(self):
        new_sequence = list(map(lambda x: -1 if x == 0 else 1, self.sequence))
        sums = []
        for i in range(1, len(new_sequence) + 1):
            sums.append(sum(new_sequence[:i]))
        sums.insert(0, 0)
        sums.append(0)
        states = {}
        L = None
        for i in range(-9, 10):
            if i != 0:
                states[i] = (sums.count(i))
            else:
                L = sums.count(i) - 1
        for i in states:
            if abs(states[i] - L) / (sqrt(2 * L * (4 * abs(i) - 2))) > self.k:
                break
        else:
            return True
        return False

    def check(self) -> bool:
        return self.frequency_test() and self.identical_bits_test() and self.extended_test()

if __name__ == '__main__':
    # solution = Solution(sequence=[1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,0,0,0,1,1,0,1,1,1,0,0,1,0,1,1,0,1,1,0,1,1,0,0,0,1,0,1,0,1,0,0,1,1,1,0,1,0,1,1,0,0,1,0,1,0,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1])
    solution = Solution()
    print(solution.frequency_test())
    print(solution.identical_bits_test())
    print(solution.extended_test())
