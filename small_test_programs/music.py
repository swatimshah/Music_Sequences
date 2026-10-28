import numpy as np
import re
from musicpy import *
import time  


# setting the seed
seed = 42
np.random.seed(seed)


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

pakad = [['sa', 're', 'ga'], ['ga', 're', 'pa', 'ga'], ['pa', 'ga', 're'], ['ga', 're', 'sa', 're', 'dha-', 'sa'], ['dha-', 'sa', 're', 'ga'], ['dha', 'pa', 'ga'], ['sa+', 're+', 'ga+'], ['ga+', 're+', 'sa+'], ['sa+', 'dha', 'pa', 'ga'], ['pa', 'dha', 'sa+'], ['ga', 'pa', 'dha'], ['ga', 'pa', 'ga', 're', 'ga'], ['sa', 're', 'ga', 'pa'], ['re+', 'sa+', 'dha', 'sa+'], ['pa', 'dha', 'sa+', 'dha'], ['pa-', 'dha-', 'sa', 'dha-'], ['re', 'sa', 'dha-', 'sa']]

vadi = [4, 16]
samvadi = [-3, 9]


# Verify the size and contents
print("Pakad Array:", pakad)

# Generate the 'notesSequence' array of size 16, 1
# np.random.choice picks random elements from the input array to fill the specified shape
notesSequence = np.random.choice(aarohAvroh, size=(16, 1))

# Verification
print(f"Array Shape: {notesSequence.shape}")
print("First sequence (Column 0):", notesSequence[:, 0])

for k in range(0, 25000):

    # Change seed and generate a new batch -> Shape: 16 x 1
    np.random.seed(k)  # Setting a new seed
    new_notes = np.random.choice(aarohAvroh, size=(16, 1))

    # Add the new notes to the existing array (Horizontal stack)
    notesSequence = np.hstack((notesSequence, new_notes))

    # Verification
    print(f"Updated Array Shape: {notesSequence.shape}")  # Outputs: (16, 1)

    # Chunk the array into groups of 4 and join them with spaces
    chunks = [" ".join(notesSequence[i:i+4, k]) for i in range(0, len(notesSequence), 4)]

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

print(search_matrix.shape)

print("=== SEARCH RESULTS AND COMPLETE QUALIFYING SEQUENCES ===\n")
match_count = 0
aFlag = True

# Loop through all 2500 column sequences
for col_idx in range(search_matrix.shape[1]):
    current_column = search_matrix[:, col_idx]
    detected_phrases = []

    # Check this individual sequence against all pakad criteria
    for p_idx, phrase in enumerate(pakad):
        p_len = len(phrase)
        phrase_to_check = [n.lower() for n in phrase] if CASE_INSENSITIVE else phrase
        
        # Sliding window lookahead
        for i in range(len(current_column) - p_len + 1):
            sub_seq = list(current_column[i:i+p_len])
            
            if sub_seq == phrase_to_check:
                detected_phrases.append({
                    "id": p_idx,
                    "phrase": " ".join(phrase),
                    "pos": i
                })
                
    # If the column satisfied ANY pakad criteria, print its entire sequence layout
    formattedSequences = []    

    if detected_phrases:
        match_count += 1
        
        # Pull original elements from notesSequence to preserve original layout casing
        full_sequence = notesSequence[:, col_idx]
        
        # Chunk into 4 blocks of 4 notes for elegant visual separation
        chunks = [" ".join(full_sequence[k:k+4]) for k in range(0, len(full_sequence), 4)]
        formatted_sequence = " | ".join(chunks)
        
        print(f"🎵 [Sequence Match #{match_count}] Column Index: {col_idx}")
        print(f"   Full Sequence: {formatted_sequence}")
        print(f"   Criteria Satisfied:")
        for pattern in detected_phrases:
            print(f"     • Pakad #{pattern['id']} ('{pattern['phrase']}') discovered at note position {pattern['pos']}")
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
        bhoop_raag_alap_seq_number = [note_mapping[note] for note in bhoop_raag_alap if note in note_mapping]
        print(bhoop_raag_alap_seq_number)
        
        for i in range(len(bhoop_raag_alap_seq_number)):
            # Check difference with the next note
            if i < len(bhoop_raag_alap_seq_number) - 1:        
                if abs(bhoop_raag_alap_seq_number[i] - bhoop_raag_alap_seq_number[i+1]) > 10:
                    aFlag = False
                    break
        
        if (aFlag == False):
            aFlag = True
            i = 0
            continue    


        if(bhoop_raag_alap_seq_number[0] != 0 and bhoop_raag_alap_seq_number[0] != 12):
            continue


        playduration = [None] * 16
        for k in range(len(bhoop_raag_alap_seq_number)):
            playduration[k] = 0.125
            if abs(bhoop_raag_alap_seq_number[k] == vadi[0] or bhoop_raag_alap_seq_number[k] == vadi[1]):
                playduration[k] = 0.25			
            if abs(bhoop_raag_alap_seq_number[k] == samvadi[0] or bhoop_raag_alap_seq_number[k] == samvadi[1]):
                playduration[k] = 0.2			

        # Establish your base note ('Sa')
        base_note = note('C', 4)
        melody_notes = [base_note + semitones for semitones in bhoop_raag_alap_seq_number]

        # Combine the notes into a playable chord/melody sequence (each note lasting 1 beats)
        arohana = chord(melody_notes, duration=playduration, interval=playduration)

        # Play it using the default synthesizer (requires pygame installed)
        play(arohana, bpm=90, instrument=41) # 41 is Violin  # 25 is guitar

        time.sleep(8)

print(f"\nSearch complete. Total valid composition matches: {match_count} out of 5000.")

