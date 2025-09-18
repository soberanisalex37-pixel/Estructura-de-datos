def fibonacci_generador(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


print(list(fibonacci_generador(10)))
