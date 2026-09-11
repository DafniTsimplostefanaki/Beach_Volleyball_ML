import pandas as pd
import numpy as np
import random

# 1. Ορισμός των παραμέτρων από το Data Dictionary
num_samples = 1000 # Πόσες φάσεις θέλουμε να παράγουμε

passing_types = ['Middle', 'Close', 'Wide', 'Back', 'Super', 'Go']
attack_zones = ['left_front', 'center_front', 'right_front', 'left_back', 'center_back', 'right_back']
defense_positions = ['1_open', '1_closed', '2_open', '2_closed']
server_types = ['standing', 'float', 'jump']
play_phases = ['sideout', 'transition']

# 2. Δημιουργία κενής λίστας για να αποθηκεύσουμε τα δεδομένα
data = []

for i in range(num_samples):
    # Παραγωγή τυχαίων αρχικών συνθηκών
    match_id = random.randint(1, 10)
    reception_quality = random.choice([1, 2, 3, 4, 5])
    passing_quality = random.choice([1, 2, 3, 4, 5])
    passing_type = random.choice(passing_types)
    attack_zone = random.choice(attack_zones)
    attacker_distance = round(random.uniform(0.2, 4.0), 1)
    num_blockers = random.choice([0, 1])
    defense_position = random.choice(defense_positions)
    
    # 3. Εφαρμογή Λογικής (Golden Rules + Noise)
    
    # --- ΚΑΝΟΝΑΣ 1: Κακή πάσα/υποδοχή οδηγεί σε poke ή forearm ---
    if passing_quality <= 2:
        attack_type = np.random.choice(['poke', 'forearm_attack', 'cut_shot'], p=[0.6, 0.3, 0.1])
        # Συνήθως αυτά δεν τελειώνουν σε kill
        attack_outcome = np.random.choice(['defended', 'error', 'kill'], p=[0.7, 0.2, 0.1])
        
    # --- ΚΑΝΟΝΑΣ 2: Καλή πάσα απέναντι σε 2_closed οδηγεί σε line_shot ---
    elif passing_quality >= 4 and defense_position == '2_closed':
        attack_type = np.random.choice(['line_shot', 'hard_spike', 'cut_shot'], p=[0.7, 0.2, 0.1])
        
        # Αν όντως κάνει line_shot σε 2_closed, τεράστιο win probability
        if attack_type == 'line_shot':
            attack_outcome = np.random.choice(['kill', 'defended', 'error'], p=[0.85, 0.10, 0.05])
        else:
            attack_outcome = np.random.choice(['defended', 'kill', 'blocked'], p=[0.5, 0.3, 0.2])
            
    # --- DEFAULT ΚΑΝΟΝΑΣ: Για όλες τις άλλες νορμάλ συνθήκες ---
    else:
        attack_type = np.random.choice(
            ['hard_spike', 'cut_shot', 'line_shot', 'poke'], 
            p=[0.4, 0.3, 0.2, 0.1]
        )
        attack_outcome = np.random.choice(
            ['defended', 'kill', 'error', 'blocked'], 
            p=[0.4, 0.35, 0.15, 0.1]
        )

    # 4. Προσθήκη της γραμμής στα δεδομένα (4th change)
    data.append([
        match_id, reception_quality, passing_quality, passing_type, attack_zone,
        attacker_distance, num_blockers, defense_position, attack_type, attack_outcome
    ])

# 5. Δημιουργία DataFrame και εξαγωγή 
columns = [
    'match_id', 'reception_quality', 'passing_quality', 'passing_type', 'attack_zone', 
    'attacker_distance', 'num_blockers', 'defense_position', 'attack_type', 'attack_outcome'
]
df = pd.DataFrame(data, columns=columns)

# Αποθήκευση σε CSV
df.to_csv('synthetic_beach_volley_data.csv', index=False)
print(f"Το dataset δημιουργήθηκε με επιτυχία! Μέγεθος: {df.shape}")
