function fatorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * fatorial(n-1);
}

print("Fatorial de 5: " + fatorial(5));

