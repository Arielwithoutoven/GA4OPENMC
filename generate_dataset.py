from GA.Individual import Individual
import random
from GA.constants import *

test_size = 5


def random_param():
    r1 = int(random.uniform(*RANGES[1]))
    r2 = int(random.uniform(r1 + 5, 170))
    r3 = int(175)
    r4 = int(180)
    z4 = int(random.uniform(-400, -200))
    z1 = int(random.uniform(-1000, z4 - 225))
    z2 = int(random.uniform(z1 + 200, z4 - 25))
    z3 = int(random.uniform(z2 + 20, z4 - 5))
    z5 = int(random.uniform(z4 + 500, 400))
    z6 = int(random.uniform(z5 + 30, z5 + 100))
    z7 = int(random.uniform(z6 + 1500, 2600))
    z8 = int(random.uniform(z7 + 600, 3200))
    z9 = int(3600)
    return [r1, r2, r3, r4, z1, z2, z3, z4, z5, z6, z7, z8, z9]


def generate_dataset(num=test_size):
    for _ in range(num):
        ind = Individual(random_param())
        ind.run_model()


if __name__ == "__main__":
    generate_dataset()
