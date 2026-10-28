import time  # 1. Import the time module
from musicpy import *

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

vadi = [4, 16]
samvadi = [-3, 9]

bhoop_raag_alap = ['sa+', 're+', 'ga+', 'ga+', 'sa+', 'sa+', 'ga+', 'sa+', 're+', 'sa+', 'sa+', 'dha', 'dha', 're+', 'ga+', 'ga+']

bhoop_raag_alap_seq_number = [note_mapping[note] for note in bhoop_raag_alap if note in note_mapping]

print(bhoop_raag_alap)
print(bhoop_raag_alap_seq_number)

playduration = [None] * 16
for k in range(len(bhoop_raag_alap_seq_number)):
    playduration[k] = 0.125
    if abs(bhoop_raag_alap_seq_number[k] == vadi[0] or bhoop_raag_alap_seq_number[k] == vadi[1]):
        playduration[k] = 0.25			
    if abs(bhoop_raag_alap_seq_number[k] == samvadi[0] or bhoop_raag_alap_seq_number[k] == samvadi[1]):
        playduration[k] = 0.2			

# 1. Establish your base note ('Sa')
base_note = note('C#', 3)
melody_notes = [base_note + semitones for semitones in bhoop_raag_alap_seq_number]

# Combine the notes into a playable chord/melody sequence (each note lasting 1 beats)
arohana = chord(melody_notes, duration=playduration, interval=playduration)

# Play it using the default synthesizer (requires pygame installed)
play(arohana, bpm=90) # 41 is Violin


time.sleep(12)
