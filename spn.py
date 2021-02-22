def spn(a, b):
    a = tuple(map(float, a.split()))
    b = tuple(map(float, b.split()))
    return f"{abs(a[0] - b[0]):.{3}f},{abs(a[1] - b[1]):.{3}f}"
