
from itertools import product

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

# key = secret
# value = list of price changes
secret_to_price_changes = {}
secret_to_prices = {}

def get_all_possible_change_sequences(length=4):
    ranges = list(range(-9, 10, 1))
    return list(product(ranges, repeat=length))





def get_price_changes(initial_secret, change_count=2000):
    price_changes = []
    prices = []
    last_secret = initial_secret
    for i in range(change_count):
        current_secret = evolve_secret(last_secret)
        last_price = last_secret % 10
        current_price = current_secret % 10
        price_changes.append(current_price - last_price)
        prices.append(current_price)
        last_secret = current_secret
    return price_changes, prices


def try_match_change_sequence_to_price_idx(change_sequence, price_changes):
    for i in range(len(price_changes) - len(change_sequence)):

        if price_changes[i] == change_sequence[0] \
            and price_changes[i+1] == change_sequence[1] \
            and price_changes[i+2] == change_sequence[2] \
            and price_changes[i+3] == change_sequence[3]:
            return i+3

    return None


def get_buy_banana_count(change_sequence, price_changes, prices):
    idx = try_match_change_sequence_to_price_idx(change_sequence, price_changes)
    if idx is None:
        return 0
    return prices[idx]


# all_possible_change_sequences = get_all_possible_change_sequences()
# print("len of all_possible_change_sequences", len(all_possible_change_sequences))


all_appeared_change_sequences = set()



def add_appeared_change_sequence(price_changes, prices):
    for i in range(len(price_changes) - 1 - 3):
        change_sequence = tuple(price_changes[i:i+4])
        all_appeared_change_sequences.add(change_sequence)


# init the map
for secret in secrets:
    price_changes, prices = get_price_changes(secret, change_count=2000)
    secret_to_price_changes[secret] = price_changes
    secret_to_prices[secret] = prices
    add_appeared_change_sequence(price_changes, prices)

print("all appeared change sequences", len(all_appeared_change_sequences))

# try brute force

max_banana_count = 0
max_banana_change_sequences = []

# all_appeared_change_sequences = [(-2,1,-1,3), (-2,1,-1,4)]

for seq_idx, change_sequence in enumerate(all_appeared_change_sequences):
    banana_count = 0
    for secret in secrets:
        price_changes, prices = secret_to_price_changes[secret], secret_to_prices[secret]
        banana_count += get_buy_banana_count(change_sequence, price_changes, prices)
    if banana_count > max_banana_count:
        max_banana_count = banana_count
        max_banana_change_sequences = [change_sequence]
    elif banana_count == max_banana_count:
        max_banana_change_sequences.append(change_sequence)

    if True:
        print("seq idx", seq_idx, "seq", change_sequence, "banana count", banana_count)

print("max_banana_count", max_banana_count)
print("max_banana_change_sequences", max_banana_change_sequences)


# secret = 123
# price_changes, prices = get_price_changes(secret, change_count=10)
# print(price_changes)
# print(prices)
# idx = try_match_change_sequence_to_price_idx([-1,-1,0,2], price_changes)
# print("matched index", idx)
# print("matched price", prices[idx])

