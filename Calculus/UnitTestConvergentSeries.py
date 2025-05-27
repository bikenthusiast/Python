import unittest
from ConvergentSeries import sequence_converges, series_converges


# Unit Tests
class TestConvergence(unittest.TestCase):

    def test_sequence_converges(self):
        # Konvergente Sequenz: a_n = 1 / (n + 1)
        self.assertTrue(sequence_converges(lambda n: 1 / (n + 1)))

        # Konvergente Sequenz: a_n = 1 / (n^2)
        self.assertTrue(sequence_converges(lambda n: 1 / ((n + 1) ** 2)))

        # Divergente Sequenz: a_n = (-1)^n (oszilliert)
        self.assertFalse(sequence_converges(lambda n: (-1) ** n))

        # Divergente Sequenz: a_n = n (wächst unbegrenzt)
        self.assertFalse(sequence_converges(lambda n: n))

    def test_series_converges_root(self):
        # Konvergente Reihe: 1 / n^2
        self.assertTrue(series_converges(lambda n: 1 / ((n + 1) ** 2), criterion="root"))

        # Divergente Reihe: 1
        self.assertFalse(series_converges(lambda n: 1, criterion="root"))
        # Divergente Reihe:
        self.assertTrue(series_converges(lambda n: 1 / (n ** 2), criterion="root"))

        # print("Divergente Reihe: 1 / (n + 1) (harmonische Reihe)")
        # self.assertFalse(series_converges(lambda n: 1 / (n + 1), criterion="root"))

        # Konvergente Reihe: a_n = 1 / (2^n)
        self.assertTrue(series_converges(lambda n: 1 / (2 ** n), criterion="root"))

        # Grenzfall (konvergiert, aber langsam): 1 / (n * log(n)^2)
        import math
        self.assertTrue(series_converges(lambda n: 1 / ((n + 2) * math.log(n + 2) ** 2), criterion="root"))


if __name__ == '__main__':
    unittest.main()
