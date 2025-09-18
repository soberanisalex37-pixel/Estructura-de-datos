def fibonacci_recursiva(n):
    if n == 0:
        return [0]
    elif n == 1:
        return [0, 1]
    else:
        seq = fibonacci_recursiva(n-1)
        seq.append(seq[-1] + seq[-2])
        return seq


resultado = fibonacci_recursiva(20)
print(resultado)

