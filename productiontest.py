# uses a generic motor production to do all actions
#from CMCed.utility import *

from CMCed.production_cycle import ProductionCycle
from CMCed.Cognitive_Functions import *



# Initialize memories
working_memory = {'focus_buffer': {'state': 'start', 'code':'red'}}

declarative_memory = {'fries': {'name': 'fries',
                                'condition': 'good',
                                'side_order': 'yes',
                                'extra': 'yes',
                                'utility':7},
                      'house_salad': {'x': 'house_salad',
                                      'y': 'good',
                                      'z': 'yes',
                                      'utility':9},
                      'poutine': {'name': 'poutine',
                                  'condition': 'good',
                                  'side_order': 'yes',
                                  'utility':0},
                      'ceasar_salad': {'name': 'ceasar_salad',
                                       'condition': 'bad',
                                       'side_order': 'yes',
                                       'utility':4}
                      }
memories = {
    'working_memory': working_memory,
    'declarative_memory': declarative_memory
}

# Initialize productions
ProceduralProductions = []

# Procedural Production to announce the sandwich is ready
def recall_order(memories):
    print('fired production.........................................***************************')

ProceduralProductions.append({
    #'matches': {'working_memory': {'focus_buffer': {'code': 'red', 'state': '*'}}},  # works
    #'matches': {'declarative_memory': {'poutine': {'side_order': 'yes'}}},  # works on any specified memory system
    #'matches': {'working_memory': {'focus_buffer': {'code': 'red', 'state': 'start', 'missing': '*'}}},  # works, mismatches on missing because it's missing
    'matches': {'working_memory': {'focus_buffer': {'code': 'red', 'state': 'start'}}},
    # positive matching and mismatching works
    #'negations': {'focus_buffer': {'state': 'start'}}, # negation not working, should block it
    'negations': {},
    '''
    PROCEDURAL MATCHING NOTES
    Memory systems
    - works on any specified memory system
    Positive matching works on production matching
    - must make all the positive matches
    Wild card works on production matching
    - positive match - the slot exists, putting a star means anything can be in it
    - negative match - the slot does not exist, putting a star means it will not match regardless of the slot value
    Negation does not work on production matching !!!!!!!!!!!!!!!!!!!!!!!!!
    '''
    'utility': 10,
    'action': recall_order,
    'report': "announce_sandwich"
})


# Production system delays in ticks
ProductionSystem1_Countdown = 1

# Stores the number of cycles for a production system to fire and reset
DelayResetValues = {
    'ProductionSystem1': ProductionSystem1_Countdown,
}

# Dictionary of all production systems and delays
AllProductionSystems = {
    'ProductionSystem1': [ProceduralProductions, ProductionSystem1_Countdown],
}

# Initialize ProductionCycle
ps = ProductionCycle()

# Run the cycle with custom parameters
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=1, millisecpercycle=10)
