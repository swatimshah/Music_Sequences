import time  # 1. Import the time module
from musicpy import *

note_mapping = {
    'sa': 0,
    're': 2,
    'ga': 4,
    'ma': 5,
    'pa': 7,
    'dha': 9,
    'ni': 11,
    'sa+': 12
}


bhoop_raag_alap = ['sa', 're', 'ga', 'pa', 'dha', 'sa+', 'sa+', 'dha', 'pa', 'ga', 're', 'sa']

bhoop_raag_alap_seq_number = [note_mapping[note] for note in bhoop_raag_alap if note in note_mapping]

print(bhoop_raag_alap_seq_number)

# 1. Establish your base note ('Sa')
base_note = note('C', 4)
melody_notes = [base_note + semitones for semitones in bhoop_raag_alap_seq_number]

# Combine the notes into a playable chord/melody sequence (each note lasting 1 beats)
arohana = chord(melody_notes, duration=1/4, interval=1/4)

# Play it using the default synthesizer (requires pygame installed)
play(arohana, bpm=90, instrument=41) # 41 is Violin


time.sleep(12)