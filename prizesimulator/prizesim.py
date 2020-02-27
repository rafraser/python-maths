import random
import matplotlib.pyplot as plt
import statistics

# List of all prizes with relative frequencies
# Most common prizes are 4x more common than the rarest etc.
PRIZES = [
    ("Bowling Pin", 4),
    ("Suspicious Chocolate", 4),
    ("Toy Rocket (Red)", 4),
    ("Toy Rocket (Green)", 4),
    ("Industrial Drum", 4),
    ("Deck of Cards", 3),
    ("Fuzzy Dice", 3),
    ("Toy Rocket (Purple)", 3),
    ("Ancient Barrel", 3),
    ("Toy Rocket (Blue)", 3),
    ("Fluffy Servers Token", 2),
    ("Broken Monitor", 2),
    ("Corrosive Waste Drum", 2),
    ("Gamebro", 2),
    ("Mysterious Orb", 2),
    ("Pluto", 1),
    ("Royal (Broken) Monitor", 1),
    ("Plush Fox", 1),
    ("Ice Fox", 1),
    ("Gamebro Color", 1),
]

# Save re-computing the total constantly
total = sum(pair[1] for pair in PRIZES)

# Specify the remaining prizes to obtain
# For all 20 prizes: [item[0] for item in prizes]
remaining = [item[0] for item in PRIZES]


def subtract_list(rem):
    """
    Inverts a list of prizes
    """
    return [item[0] for item in PRIZES if item[0] not in rem]


def weighted_random(choices, total=None):
    """
    Weighted random
    Given a list of (Item, Weight) pairs, will pick a weighting
    """
    # Calculate the total if not specified
    if not total:
        total = sum(pair[1] for pair in choices)

    # Pick a random number
    # Add list elements until we go past this 'marker'
    r = random.randint(1, total)
    for (value, weight) in choices:
        r -= weight
        if r <= 0:
            return value


def trial():
    """
    Run a single trial of the prize simulator
    """
    collected = subtract_list(remaining)
    count = 0
    while len(collected) < len(PRIZES):
        count += 1
        prize = weighted_random(PRIZES)

        if prize not in collected:
            collected.append(prize)

    return count


def plot(results, bins=20):
    """
    Generate a histogram from a set of prize simulations
    """
    plt.hist(results, bins=bins)
    plt.show()


def main(n):
    """
    Run multiple trials and perform some statistical analysis
    """
    # Run a bunch of trials
    results = []
    for i in range(n):
        results.append(trial())

    # Print the statistical Ms
    print("Min:", min(results))
    print("Mean:", sum(results) / len(results))
    print("Median:", statistics.median(results))
    print("Mode: ", statistics.mode(results))
    print("Max:", max(results))

    # Truncate and plot the data
    truncated_results = [x for x in results if x < 200]
    plot(truncated_results)


if __name__ == "__main__":
    main(10000)

