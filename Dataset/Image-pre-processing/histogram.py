import matplotlib.pyplot as plt

# Data for counts
number_counts = {
    0: 973,
    1: 1342,
    2: 614,
    3: 579,
    4: 602,
    5: 819,
    6: 655,
    7: 488,
    8: 470,
    9: 606,
    10: 675,
    11: 517
}

# Labels for each number
labels = {
    0: 'yali',
    1: 'akhi jhyal',
    2: 'taleju temple',
    3: 'nyatapola',
    4: 'hanging pala',
    5: 'boudhanath',
    6: 'prayer wheel',
    7: 'garud',
    8: 'hanuman idol',
    9: 'kala bhairav',
    10: 'shveta bhairav',
    11: 'taleju bell'
}

# Sort the data by number
sorted_numbers = sorted(number_counts.keys())
sorted_counts = [number_counts[num] for num in sorted_numbers]
sorted_labels = [labels[num] for num in sorted_numbers]

# Plotting the histogram
plt.figure(figsize=(10, 6))
plt.bar(sorted_labels, sorted_counts, color='black')
plt.xlabel('Labels')
plt.ylabel('Occurrences')
plt.title('Histogram of multiple classes')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
