import random

from tools import BigPrimes
from math import gcd

from lab1 import Solution


#Этот класс является базовым классом для всех генераторов.
#Он содержит параметры длины генерируемой последовательности и размера случайных простых чисел в битах.

class BaseGenerator:
    length: int  # Длина генерируемой последовательности
    size: int  # Размер случайных простых чисел (в битах)

    def __init__(self, length: int, size: int = 160):
        self.length = length
        self.size = size

#Этот класс наследует от BaseGenerator и реализует генератор случайных чисел на основе алгоритма RSA.
class RSA(BaseGenerator):
    p: int = 0  # Случайное большое простое число p длинной RSA_SIZE бит
    q: int = 0  # Случайное большое простое число q длинной RSA_SIZE бит
    n: int  # Число n, равное p * q
    f: int  # Значение f(n), равное (p - 1) * (q - 1)
    k: int  # Случайное число, взаимно простое с f(n)
    u: int  # Случайное стартовое значение

    def __init__(self, length: int, size: int):
        super().__init__(length, size)
        self._p_q_n_f_generator()
        self._k_generator()
        self._u_generator()

#  Генерирует два разных простых числа p и q, после чего вычисляет значение n = p * q и f(n) = (p - 1) * (q - 1)
    def _p_q_n_f_generator(self):
        while self.p == self.q:
            self.p = BigPrimes().generate(self.size)
            self.q = BigPrimes().generate(self.size)
        self.n = self.p * self.q
        self.f = (self.p - 1) * (self.q - 1)

# Генерирует значение k, которое должно быть взаимно простым с f(n)
    def _k_generator(self):
        while True:
            self.k = BigPrimes().generate(self.size)
            if self.f > self.k > 1 == gcd(self.k, self.f):
                break

#Генерирует значение k, которое должно быть взаимно простым с f(n)
    def _u_generator(self):
        self.u = random.randint(1, self.n - 1)

#Генерирует последовательность битов, используя метод возведения в степень по модулю.
    def generate(self):
        res = []
        for i in range(self.length):
            self.u = pow(self.u, self.k, self.n)
            res.append(int(bin(self.u)[-1]))
        return res


class BBS(BaseGenerator):
    p: int = 0  #
    q: int = 0  #
    n: int  #
    s: int  #
    u: int  #

    def __init__(self, length: int, size: int):
        super().__init__(length, size)
        self._p_q_n_generator()
        self._s_u_generator()

#Генерирует p и q,  где оба числа должны быть равны 3 по модулю 4
    def _p_q_n_generator(self):
        while self.p % 4 != 3:
            self.p = BigPrimes().generate(self.size)
        while self.q % 4 != 3 or self.p == self.q:
            self.q = BigPrimes().generate(self.size)
        self.n = self.p * self.q

#Генерирует начальные значения s и u.  где u инициализируется как квадрат s по модулю n
    def _s_u_generator(self):
        self.s = self.n + 1
        while self.s > self.n - 1:
            self.s = BigPrimes().generate(self.size)
        self.u = pow(self.s, 2, self.n)

#Генерирует последовательность битов, используя квадрат по модулю. Каждое новое значение u вычисляется как u = u^2 mod n,
# и добавляется последний бит результата в список.
    def generate(self):
        res = []
        for i in range(self.length):
            self.u = pow(self.u, 2, self.n)
            res.append(int(bin(self.u)[-1]))
        return res

#Это генератор на основе линейного конгруэнтного метода.
class LinearCongruent(BaseGenerator):
    def __init__(self, length: int, size: int, a=16807, b=random.randint(0, 2147483647), m=2147483647):
        super().__init__(length, size)
        self.a = a
        self.b = b
        self.m = m
        self.x = BigPrimes().generate(self.size)

#Вычисляет новое x, используя линейную конгруэнтную формулу и добавляет каждый последний бит в результат.
    def generate(self):
        res = []
        for i in range(self.length):
            self.x = (self.a * self.x + self.b) % self.m
            res.append(int(bin(self.x)[-1]))
        return res


if __name__ == '__main__':
    sequence = RSA(100, 160).generate()
    print(sequence)

    test = Solution(sequence=sequence)
    print(test.frequency_test())
    print(test.identical_bits_test())
    print(test.extended_test())
    print(test.check())

    sequence = BBS(100, 160).generate()
    print(sequence)

    test = Solution(sequence=sequence)
    print(test.frequency_test())
    print(test.identical_bits_test())
    print(test.extended_test())
    print(test.check())

    sequence = LinearCongruent(length=100, size=160).generate()
    print(sequence)

    test = Solution(sequence=sequence)
    print(test.frequency_test())
    print(test.identical_bits_test())
    print(test.extended_test())
    print(test.check())
