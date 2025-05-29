from ConvergentSeries import sequence_converges, series_converges
import unittest

class TestConvergence(unittest.TestCase):

    # === Tests for sequence_converges ===

    def test_sequence_converges_to_zero(self):
        self.assertTrue(sequence_converges(lambda n: 1 / (n + 1), epsilon=1e-3))

    def test_sequence_converges_to_nonzero(self):
        self.assertTrue(sequence_converges(lambda n: 1 + 1 / (n + 1), epsilon=1e-3))

    def test_sequence_divergent(self):
        self.assertFalse(sequence_converges(lambda n: n, epsilon=1e-3))

    def test_sequence_converges_edge_case(self):
        self.assertTrue(sequence_converges(lambda n: 1 / (n ** 2), epsilon=1e-6))

    def test_sequence_small_max_n(self):
        with self.assertRaises(ValueError):
            sequence_converges(lambda n: 1 / (n + 1), max_n=50)

    # === Tests for series_converges with root test ===

    def test_series_root_geometric(self):
        self.assertTrue(series_converges(lambda n: 1 / (2 ** n), criterion="root"))

    def test_series_root_harmonic(self):
        self.assertFalse(series_converges(lambda n: 1 / (n + 1), criterion="root"))

    def test_series_root_polynomial_decay(self):
        self.assertTrue(series_converges(lambda n: 1 / (n ** 2), criterion="root"))

    def test_series_root_alternating(self):
        self.assertTrue(series_converges(lambda n: (-1) ** n / (n + 1), criterion="root"))

    # === Tests for series_converges with ratio test ===

    def test_series_ratio_geometric(self):
        self.assertTrue(series_converges(lambda n: 1 / (2 ** n), criterion="ratio"))

    def test_series_ratio_harmonic(self):
        self.assertFalse(series_converges(lambda n: 1 / (n + 1), criterion="ratio"))

    def test_series_ratio_divergent(self):
        self.assertFalse(series_converges(lambda n: n, criterion="ratio"))

    def test_series_invalid_criterion(self):
        with self.assertRaises(ValueError):
            series_converges(lambda n: 1 / (n + 1), criterion="unknown")


if __name__ == "__main__":
    unittest.main()

https://aistudio.google.com/apikey

export GOOGLE_GENERATIVE_AI_API_KEY="AIzaSyAHi8bLmUNyjs_NEhtU6-DSijMVfeRmIYo"