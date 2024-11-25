
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
                                'utility':5},
                      'house_salad': {'name': 'house_salad',
                                      'condition': 'good',
                                      'side_order': 'yes',
                                      'utility':6},
                      'poutine': {'name': 'poutine',
                                  'condition': 'good',
                                  'side_order': 'yes',
                                  'utility':7},
                      'ceasar_salad': {'name': 'ceasar_salad',
                                       'condition': 'bad',
                                       'side_order': 'no',
                                       'utility':9}
                      }
memories = {
    'working_memory': working_memory,
    'environment_memory': environment_memory,
    'declarative_memory': declarative_memory
}

# Initialize productions
ProceduralProductions = []

def announce_sandwich(memories):
# increase utility (house salad will be chosen due to boost)
    chunk_description = {'name': 'house_salad', 'condition': 'good', 'side_order': 'yes'}
    utility_change_by_description(memories, 'declarative_memory', chunk_description, amount=2, max_utility=10)
# do the retrieval
    buffer = declarative_memory
    matches = {'side_order': 'yes', 'condition': '*'}
    negations = {'extra': '*'}
    retrieved_chunk = retrieve_memory_chunk(buffer, matches, negations)
# report
    print('I recall the side order was.........................................***************************')
    print(retrieved_chunk['name'])
    report_memory_contents(buffer, matches, negations)  # print results

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
