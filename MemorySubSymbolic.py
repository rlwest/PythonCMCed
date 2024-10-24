# uses a generic motor production to do all actions
#from CMCed.utility import *

from CMCed.production_cycle import ProductionCycle
from CMCed.Cognitive_Functions import match_chunks_with_diagnostics
from CMCed.Cognitive_Functions import *



# Initialize memories
working_memory = {'focus_buffer': {'state': 'start'}}

environment_memory = {'bread1': {'location': 'counter'},
                      'cheese': {'location': 'counter'},
                      'ham': {'location': 'counter'},
                      'bread2': {'location': 'counter'}
                      }
declarative_memory = {'fries': {'name': 'fries',
                                'condition': 'good',
                                'side_order': 'yes',
                                'utility':7},
                      'house_salad': {'name': 'house_salad',
                                      'condition': 'good',
                                      'side_order': 'yes',
                                      'utility':7},
                      'poutine': {'name': 'poutine',
                                  'condition': 'good',
                                  'side_order': 'yes',
                                  'utility':7},
                      'ceasar_salad': {'name': 'ceasar_salad',
                                       'condition': 'bad',
                                       'side_order': 'yes',
                                       'utility':9}
                      }
memories = {
    'working_memory': working_memory,
    'environment_memory': environment_memory,
    'declarative_memory': declarative_memory
}

# Initialize productions
ProceduralProductions = []

# Procedural Production to announce the sandwich is ready
def announce_sandwich(memories):
    decay_all_memory_chunks(memories, 'declarative_memory',1)
    #utility_change(memories, 'declarative_memory', 'poutine', 1, max_utility=10)
    #report_memory_contents(declarative_memory, "Declarative Memory")
    target_memory = declarative_memory
    cue = {'matches': {'side_order': 'yes'}, 'negations': {'condition': 'good'}}
    report_memory_contents(declarative_memory, "Declarative Memory", cue)

    #retrieved_chunk = match_chunks_with_diagnostics(target_memory, cue)
    retrieved_chunk = match_chunks_with_diagnostics(target_memory, cue, utility_threshold=2)
    print("Retrieved:", retrieved_chunk)
    print("Retrieved:", retrieved_chunk)
    print('I recall the side order was.........................................***************************')
    print(retrieved_chunk['name'])

ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'state': 'start'}}},
    'negations': {},
    'utility': 10,
    'action': announce_sandwich,
    'report': "announce_sandwich",
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
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=9, millisecpercycle=10)
