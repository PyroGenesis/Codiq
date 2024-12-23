import os

here = os.path.dirname(os.path.abspath(__file__))


# read input
def read_data(filename: str):
    global here

    filepath = os.path.join(here, filename)
    with open(filepath, mode="r", encoding="utf8") as f:
        return f.read()


def mix_and_prune(a, b):
    a ^= b
    return a % 16777216


def evolve(num):
    num = mix_and_prune(num, num * 64)
    num = mix_and_prune(num, num // 32)
    num = mix_and_prune(num, num * 2048)
    return num


def part1(filename: str):
    data = read_data(filename)
    buyers = [int(s) for s in data.splitlines()]
    nb = len(buyers)
    for _ in range(2000):
        for i in range(nb):
            buyers[i] = evolve(buyers[i])
    return sum(buyers)


assert part1("sample.txt") == 37327623
print("Part 1:", part1("input.txt"))

from collections import deque


def part2(filename: str):
    data = read_data(filename)
    buyers = [int(s) for s in data.splitlines()]
    # nb = len(buyers)

    buyer_maps = []
    for buyer in buyers:
        buyer_map: dict[tuple[int, ...], int] = {}
        seq = deque([])
        last_price = buyer % 10
        for _ in range(2000):
            buyer = evolve(buyer)
            price = buyer % 10

            seq.append(price - last_price)
            last_price = price
            if len(seq) > 4:
                seq.popleft()
            elif len(seq) < 4:
                continue
            seq_t = tuple(seq)
            if seq_t in buyer_map:
                continue
            buyer_map[seq_t] = price
        buyer_maps.append(buyer_map)

    seqs = set([seq for bm in buyer_maps for seq in bm])
    max_bananas, best_seq = 0, None
    for seq in seqs:
        bananas = 0
        for buyer_map in buyer_maps:
            if seq in buyer_map:
                bananas += buyer_map[seq]
        if bananas > max_bananas:
            max_bananas = bananas
            best_seq = seq

    # print(best_seq)
    return max_bananas


print("Part 2:", part2("input.txt"))
