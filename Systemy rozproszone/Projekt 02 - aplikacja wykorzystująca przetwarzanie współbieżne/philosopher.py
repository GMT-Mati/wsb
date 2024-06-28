import threading
import time
import random


class Philosopher(threading.Thread):
    def __init__(self, name, left_fork, right_fork):
        threading.Thread.__init__(self)
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        while True:
            print(f"{self.name} myśli.")
            time.sleep(random.uniform(1, 3))
            print(f"{self.name} jest głodny.")
            self.dine()

    def dine(self):
        fork1, fork2 = self.left_fork, self.right_fork

        while True:
            fork1.acquire(True)
            locked = fork2.acquire(False)
            if locked: break
            fork1.release()
            print(f"{self.name} zmienia widelec.")
            fork1, fork2 = fork2, fork1
            time.sleep(random.uniform(1, 3))

        print(f"{self.name} je.")
        time.sleep(random.uniform(1, 3))
        fork2.release()
        fork1.release()


if __name__ == "__main__":
    forks = [threading.Lock() for _ in range(5)]
    philosophers = [Philosopher(f"Filozof {i + 1}", forks[i], forks[(i + 1) % 5]) for i in range(5)]

    for philosopher in philosophers:
        philosopher.start()

    for philosopher in philosophers:
        philosopher.join()
