import numpy as np
import re
from musicpy import *
import time  
import random


def find_last_element_position(large_arr, short_arr):
    # Extract and split the string into a list of musical notes
    short_tokens = short_arr[0].split()
    
    n_large = len(large_arr)
    n_short = len(short_tokens)
    
    # Iterate backwards through the large array to find the last (rightmost) match
    for i in range(n_large - n_short, -1, -1):
        # Check if the slice matches the short sequence
        if large_arr[i:i + n_short] == short_tokens:
            # Calculate the index of the last element in that matched sequence
            last_element_index = i + n_short - 1
            return last_element_index
            
    return -1  # Return -1 if the sequence isn't found



def pick_random_with_distance(arr, seed, min_distance, num_elements=16):
    # Retry loop in case the random path hits a dead end
    np.random.seed(seed)  # Setting a new seed
    selected_indices = []
    while len(selected_indices) <= num_elements:
        available_indices = list(range(len(arr)))
        # Pick the first random index
        first_idx = np.random.choice(available_indices)
        selected_indices.append(first_idx)
        #available_indices.remove(first_idx)
        
        success = True
        for _ in range(num_elements - 1):
            last_idx = selected_indices[-1]
            
            # Filter remaining indices to maintain the distance constraint
            valid_candidates = [
                i for i in available_indices 
                if abs(i - last_idx) <= min_distance
            ]
            
            # If no valid moves are left, break and try again
            if not valid_candidates:
                success = False
                break
              
            next_idx = np.random.choice(valid_candidates)
            selected_indices.append(next_idx)
            #available_indices.remove(next_idx)
            #seed = seed + 1
            
        if success:
            # Map the selected indices back to the original array values
            return [arr[idx] for idx in selected_indices], selected_indices


# Define the aaroh and avroh lists
aaroh = ["pa-", "dha-", "sa", "re", "ga", "pa", "dha", "sa+", "re+", "ga+"]
avroh = ["ga+", "re+", "sa+", "dha", "pa", "ga", "re", "sa", "dha-", "pa-"]

note_mapping = {
    'pa-':  -5,
    'dha-': -3,
    'ni-':  -1,
    'sa': 0,
    're': 2,
    'ga': 4,
    'ma': 5,
    'pa': 7,
    'dha': 9,
    'ni': 11,
    'sa+': 12,
    're+':  14,
    'ga+':  16,
    'ma+':  17
}


# Combine them into the aarohAvroh array (list)
aarohAvroh = aaroh + avroh

# Verify the size and contents
print("aarohAvroh Array:", aarohAvroh)
print("Total Size:", len(aarohAvroh))

pakad = [['sa', 're', 'ga'], ['ga', 're', 'pa', 'ga'], ['pa', 'ga', 're'], ['ga', 're', 'sa', 're', 'dha-', 'sa'], ['dha-', 'sa', 're', 'ga'], ['dha', 'pa', 'ga'], ['sa+', 're+', 'ga+'], ['ga+', 're+', 'sa+'], ['sa+', 'dha', 'pa', 'ga'], ['pa', 'dha', 'sa+'], ['ga', 'pa', 'dha'], ['ga', 'pa', 'ga', 're', 'ga'], ['sa', 're', 'ga', 'pa'], ['re+', 'sa+', 'dha', 'sa+'], ['pa', 'dha', 'sa+', 'dha'], ['pa-', 'dha-', 'sa', 'dha-'], ['re', 'sa', 'dha-', 'sa'], ['re', 'ga', 'pa'], ['ga', 'pa', 'dha'], ['pa', 'dha', 'sa'], ['sa', 'dha', 'pa'], ['dha', 'pa', 'ga'], ['pa', 'ga', 're'], ['ga', 're', 'sa'], ['sa', 're', 'ga', 'pa'], ['re', 'ga', 'pa', 'dha'], ['ga', 'pa', 'dha', 'sa'], ['sa', 'dha', 'pa', 'ga'], ['dha', 'pa', 'ga', 're'], ['pa', 'ga', 're', 'sa'], ['sa', 're'], ['re', 'ga'], ['ga', 'pa'], ['pa', 'dha'], ['dha', 'sa'], ['sa', 'dha'], ['dha', 'pa'], ['pa', 'ga'], ['ga', 're'], ['re', 'sa'], ['sa', 're', 'sa', 're', 'ga'], ['re', 'ga', 're', 'ga', 'pa'], ['ga', 'pa', 'ga', 'pa', 'dha'], ['pa', 'dha', 'pa', 'dha', 'sa'], ['sa', 'dha', 'sa', 'dha', 'pa'], ['dha', 'pa', 'dha', 'pa', 'ga'], ['pa', 'ga', 'pa', 'ga', 're'], ['ga', 're', 'ga', 're', 'sa']]

vadi = [4, 16]
samvadi = [-3, 9]

N = 300
MIN_DISTANCE = 2

# Verify the size and contents
print("Pakad Array:", pakad)

# Generate the 'notesSequence' array of size 16, 1
# np.random.choice picks random elements from the input array to fill the specified shape
notesSequenceList, indices = pick_random_with_distance(aarohAvroh, 0, MIN_DISTANCE, num_elements=16)
# Convert the list to a NumPy array
notesSequence = np.array(notesSequenceList)

# Verification
#print(f"Array Shape: {notesSequence.shape}")
print("First sequence:", notesSequence)
print("First indices:", indices)


for k in range(1, N):

    # Change seed and generate a new batch -> Shape: 16 x 1
    # np.random.seed(k)  # Setting a new seed
    new_notesList, indicesList = pick_random_with_distance(aarohAvroh, k, MIN_DISTANCE, num_elements=16)
    new_notes = np.array(new_notesList)

    print("sequence:", new_notes)
    print("sequence:", indicesList)

    # Add the new notes to the existing array (Horizontal stack)
    notesSequence = np.vstack((notesSequence, new_notes))

    # Verification
    print(f"Updated Array Shape: {notesSequence.shape}")  # Outputs: (N, 16)

    # Chunk the array into groups of 4 and join them with spaces
    chunks = [" ".join(notesSequence[k, i:i+4]) for i in range(0, len(notesSequence[k]), 4)]

    # Join the groups with the "|" separator
    formatted_output = " | ".join(chunks)

    # Print the final result
    print(formatted_output)

#==========================================================

CASE_INSENSITIVE = True  # Handles 'Re' vs 're' seamlessly

# Normalize casing for accurate string matching
if CASE_INSENSITIVE:
    search_matrix = np.char.lower(notesSequence)
else:
    search_matrix = notesSequence

print("search matrix shape", search_matrix.shape)

print("=== SEARCH RESULTS AND COMPLETE QUALIFYING SEQUENCES ===\n")
match_count = 0
aFlag = True

# Loop through all N column sequences
for col_idx in range(search_matrix.shape[0]):
    current_row = search_matrix[col_idx, :]
    print(current_row)
    distinct_detected_phrases = []

    # Check this individual sequence against all pakad criteria
    for p_idx, phrase in enumerate(pakad):
        p_len = len(phrase)
        phrase_to_check = [n.lower() for n in phrase] if CASE_INSENSITIVE else phrase        

        # Sliding window lookahead
        for i in range(len(current_row) - p_len + 1):
            sub_seq = list(current_row[i:i+p_len])
            
            if sub_seq == phrase_to_check:
                distinct_detected_phrases.append({
                    "id": p_idx,
                    "phrase": " ".join(phrase),
                    "pos": i
                })
                
    # If the column satisfied ANY pakad criteria, print its entire sequence layout

    print(distinct_detected_phrases)

    # Extract the strings from the single-element lists and remove exact duplicates
    unique_phrases = sorted(list(set(item['phrase'] for item in distinct_detected_phrases)), key=len, reverse=True)

    merged_result = []

    for phrase in unique_phrases:

        # Check if the phrase is already contained inside any longer phrase
        if not any(phrase in longer for longer in merged_result):
            merged_result.append(phrase)

        # Wrap back into the original list-of-list format
        detected_phrases = [[phrase] for phrase in merged_result]

        print(detected_phrases)

    ####################

    formattedSequences = []    

    if detected_phrases:
        match_count += 1
        
        # Pull original elements from notesSequence to preserve original layout casing
        full_sequence = notesSequence[col_idx, :]
        
        # Chunk into 4 blocks of 4 notes for elegant visual separation
        chunks = [" ".join(full_sequence[k:k+4]) for k in range(0, len(full_sequence), 4)]
        formatted_sequence = " | ".join(chunks)
        
        print(f"🎵 [Sequence Match #{match_count}] Column Index: {col_idx}")
        print(f"   Full Sequence: {formatted_sequence}")
        print(f"   Criteria Satisfied:")
        for pattern in detected_phrases:
            #print(f"     • Pakad #{pattern['id']} ('{pattern['phrase']}') discovered at note position {pattern['pos']}")
            print(pattern)
        print("-" * 85)

        # Add the new notes to the existing array (Horizontal stack)
        formattedSequences = np.hstack((formattedSequences, formatted_sequence))

        # Verification
        print(f"Updated Array Shape: {formattedSequences.shape}")  # Outputs: (16, 1)

        # Split by either a comma (,) or a pipe (|)
        # The strip() removes any accidental surrounding whitespaces
        bhoop_raag_alap = []
        tokens = [token.strip() for token in re.split(r'[ | ]', formatted_sequence)]
        bhoop_raag_alap = [t for t in tokens if t]
        print (bhoop_raag_alap)

        # print(bhoop_raag_alap)
        print(detected_phrases[0])
        position = find_last_element_position(bhoop_raag_alap, detected_phrases[0])
        print(f"The position of the last element is: {position}")

        bhoop_raag_alap_seq_number = [note_mapping[note] for note in bhoop_raag_alap if note in note_mapping]
        # print(bhoop_raag_alap_seq_number)       

        if(bhoop_raag_alap_seq_number[0] != 0 and bhoop_raag_alap_seq_number[0] != 12):
            continue

        if(bhoop_raag_alap_seq_number[15] != 4 and bhoop_raag_alap_seq_number[15] != 16):
            continue


        playduration = [None] * 16
        for k in range(len(bhoop_raag_alap_seq_number)):
            playduration[k] = 0.125                
            if abs(bhoop_raag_alap_seq_number[k] == vadi[0] or bhoop_raag_alap_seq_number[k] == vadi[1]):
                playduration[k] = 0.25			
            if abs(bhoop_raag_alap_seq_number[k] == samvadi[0] or bhoop_raag_alap_seq_number[k] == samvadi[1]):
                playduration[k] = 0.2			
            
        playduration[position] = 0.25		

        # Establish your base note ('Sa')
        base_note = note('C#', 3)
        melody_notes = [base_note + semitones for semitones in bhoop_raag_alap_seq_number]

        # Combine the notes into a playable chord/melody sequence (each note lasting 1 beats)
        print(playduration)
        arohana = chord(melody_notes, duration=playduration, interval=playduration)

        # Play it using the default synthesizer (requires pygame installed)
        play(arohana, bpm=90) # 41 is Violin  # 25 is guitar  # default is piano, instrument=41

        time.sleep(9)

print(f"\nSearch complete. Total valid composition matches: {match_count} out of ", N)

