# Original list of lists containing space-separated strings
data = [
    ['sa re ga'], ['ga pa dha'], ['sa re ga pa'], ['re ga pa'], 
    ['ga pa dha'], ['sa re ga pa'], ['re ga pa dha'], ['sa re'], 
    ['sa re'], ['re ga'], ['ga pa'], ['pa dha'], ['dha pa'], ['re sa']
]

# Extract the strings from the single-element lists and remove exact duplicates
unique_phrases = sorted(list(set(item[0] for item in data)), key=len, reverse=True)

merged_result = []

for phrase in unique_phrases:
    # Check if the phrase is already contained inside any longer phrase
    if not any(phrase in longer for longer in merged_result):
        merged_result.append(phrase)

# Wrap back into the original list-of-list format
final_output = [[phrase] for phrase in merged_result]

print(final_output)