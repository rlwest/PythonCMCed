# uses a generic motor production to do all actions
#from CMCed.utility import *

from CMCed.production_cycle import ProductionCycle
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
                                      'utility':3},
                      'poutine': {'name': 'poutine',
                                  'condition': 'good',
                                  'side_order': 'yes',
                                  'utility':7},
                      'ceasar_salad': {'name': 'ceasar_salad',
                                       'condition': 'bad',
                                       'side_order': 'no',
                                       'utility':9},
                      'fido': {'name': 'fido',
                               'isa':'dog',
                               'temperment': 'good'}
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
    # add noise
    add_noise_to_utility(declarative_memory, 'declarative_memory', scalar=0.5)
    # add decay
    #decay_all_memory_chunks(memories, 'declarative_memory',1)
    # add boost
    #utility_change(memories, 'declarative_memory', 'poutine', 1, max_utility=10)
    # set memory retrieval variables
    #target_memory = declarative_memory
    #cue = {'matches': {'side_order': 'no'}, 'negations': {'condition': '*'}}
    # retrieve with threshold (threshold default = 0
    #retrieved_chunk = match_chunks_with_diagnostics(target_memory, cue, utility_threshold=0)
    #chunk_description = {'name': 'poutine', 'condition': 'good', 'side_order': 'yes'}
    chunk_description = {'name': 'house_salad', 'condition': 'good', 'side_order': 'yes'}
    #chunk_description = {'name': 'fries', 'condition': 'good', 'side_order': 'yes'}
    utility_change_by_description(memories, 'declarative_memory', chunk_description, amount=2, max_utility=10)

    buffer = declarative_memory
    matches = {'side_order': 'yes', 'condition': '*'}
    negations = {'extra': '*'}
    report_memory_contents(buffer, matches, negations)    # print results
    report_memory_contents(buffer)    # print results

# get the chunk
    retrieved_chunk = retrieve_memory_chunk(buffer, matches, negations)
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
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=1, millisecpercycle=10)
