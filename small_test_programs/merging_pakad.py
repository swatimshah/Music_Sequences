# Original list of lists
data = [
    ['sa', 're', 'ga'],
    ['ga', 'pa', 'dha'],
    ['sa', 're', 'ga', 'pa'],
    ['re', 'ga', 'pa'],
    ['ga', 'pa', 'dha'],
    ['sa', 're', 'ga', 'pa'],
    ['re', 'ga', 'pa', 'dha'],
    ['sa', 're'],
    ['sa', 're'],
    ['re', 'ga'],
    ['ga', 'pa'],
    ['pa', 'dha'],
    ['dha', 'pa'],
    ['re', 'sa']
]

# Convert each sublist to a tuple so they can be added to a set (removes exact duplicates)
unique_tuples = sorted(list(set(tuple(sublist) for sublist in data)), key=len, reverse=True)

merged_result = []

for current in unique_tuples:
    # Check if 'current' is a subset of any already accepted longer list
    if not any(set(current).issubset(set(longer)) for longer in merged_result):
        merged_result.append(list(current))

# Print the final merged list
print(merged_result)
