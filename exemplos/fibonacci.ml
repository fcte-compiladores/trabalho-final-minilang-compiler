function fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n-1) + fibonacci(n-2);
}

int resultado = fibonacci(10);
print("Fibonacci de 10: " + resultado);

