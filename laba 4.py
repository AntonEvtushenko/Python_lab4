import time
import threading
# Декоратор для ограничения времени выполнения функции
def timeout(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = [None]
            def inner():
                result[0] = func(*args, **kwargs)
            thread = threading.Thread(target=inner)
            thread.start()
            thread.join(timeout=seconds)
            if thread.is_alive():
                print(f"Функция {func.__name__} превысила время выполнения в {seconds} секунд.")
                return None
            return result[0]
        return wrapper
    return decorator
# Замыкание для получения простых чисел
def prime_generator():
    primes = []
    def is_prime(n):
        if n < 2:
            return False
        for p in primes:
            if p * p > n:
                break
            if n % p == 0:
                return False
        return True

    def get_next_prime():
        num = 2
        while True:
            if is_prime(num):
                primes.append(num)
                yield num
            num += 1

    return get_next_prime()
@timeout(1)  # ограничение по времени выполнения
def generate_primes(n):
    prime_gen = prime_generator()
    primes = []
    for _ in range(n):
        primes.append(next(prime_gen))
    return primes

if __name__ == "__main__":
    n = 100 # Количество простых чисел
    primes = generate_primes(n)
    if primes is not None:
        print(f"Первые {n} простых чисел: {primes}")