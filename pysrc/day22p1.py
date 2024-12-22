
def mix_into_secret(secret, value):
    return secret ^ value

def prune_secret(secret):
    return secret % 16777216

def evolve_secret(secret):
    temp1 = secret * 64
    secret = mix_into_secret(secret, temp1)
    secret = prune_secret(secret)

    temp2 = secret // 32
    secret = mix_into_secret(secret, temp2)
    secret = prune_secret(secret)

    temp3 = secret * 2048
    secret = mix_into_secret(secret, temp3)
    secret = prune_secret(secret)

    return secret

with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

secrets = [int(i) for i in lines]

STEP = 2000

sum_after_step = 0

for secret in secrets:
    for i in range(STEP):
        secret = evolve_secret(secret)

    print(secret)
    sum_after_step += secret

print(sum_after_step)

