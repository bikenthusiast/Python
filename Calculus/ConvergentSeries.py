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
        values = []
        for n in range(1, max_n):
            try:
                val = abs(seq(n))
                root = val ** (1 / n)
                values.append(root)
            except ZeroDivisionError:
                continue

        if not values or len(values) < 100:
            return None

        limsup = max(values[-100:])
        if abs(limsup - 1) < epsilon:
            return None  # Inconclusive
        return limsup < 1 - epsilon

    elif criterion == "ratio":
        values = []
        for n in range(1, max_n - 1):
            try:
                a_n = abs(seq(n))
                a_next = abs(seq(n + 1))
                if a_n == 0:
                    continue
                ratio = a_next / a_n
                values.append(ratio)
            except ZeroDivisionError:
                continue

        if not values or len(values) < 100:
            return None

        limsup = max(values[-100:])
        if abs(limsup - 1) < epsilon:
            return None  # Inconclusive
        return limsup < 1 - epsilon

    else:
        raise ValueError("Unknown criterion. Use 'root' or 'ratio'.")

