# https://en.wikipedia.org/wiki/Convergent_series

def sequence_converges(seq, epsilon=1e-5, max_n=1000):
    if max_n < 100:
    raise ValueError("max_n must be at least 100 to check convergence")

    # Evaluate the last 100 terms
    tail = [seq(n) for n in range(max_n - 100, max_n)]

    max_diff = max(abs(a - b) for i, a in enumerate(tail) for b in tail[i + 1:])

    return max_diff < epsilon


def series_converges(seq, criterion="root", epsilon=1e-5, max_n=1000):
    if criterion == "root":
        # Apply the root test: limsup |a_n|^{1/n} < 1
        values = [abs(seq(n)) ** (1 / n) if n != 0 else 0 for n in range(1, max_n)]
        limsup = max(values[-100:])  # approximate limsup with the last 100 values
        return limsup < 1 - epsilon
