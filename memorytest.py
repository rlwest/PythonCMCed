
from CMCed.production_cycle import ProductionCycle
from CMCed.Cognitive_Functions import *

# Initialize memories
working_memory = {'focus_buffer': {'state': 'start'}}
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

def recall_order(memories):
    buffer = declarative_memory
    matches = {'side_order': 'yes', 'condition': '*'}
    negations = {'extra': '*'}
    #negations = {}

    #cue = {'matches': {'side_order': 'yes', 'condition': 'good'}, 'negations': {}} # positive matching and mismatching works
    #cue = {'matches': {'side_order': 'yes', 'condition': 'good'}, 'negations': {'name': 'fries'}} # negation works
    #cue = {'matches': {'side_order': 'yes', 'condition': '*'}, 'negations': {'name': 'fries'}} # wild card works when it is in existing slot
    #cue = {'matches': {'side_order': 'yes', 'bat': '*'}, 'negations': {'cat': '*'}} # wild card works when it is in non existing slot
    #cue = {'matches': {'side_order': 'yes', 'temperature': '*'}, 'negations': {'name': 'fries'}}
    # wild card does not cause a match to fail when a slot is not there - no chunks have a temperature slot so they should all fail
    # cue = {'matches': {'side_order': 'yes', 'condition': '*'}, 'negations': {'name': '*'}}
    # a negating wild card does not cause a match to fail - all chunks have a name slot so none should match
    retrieved_chunk = retrieve_memory_chunk(buffer, matches, negations, utility_threshold=0)
    report_memory_contents(declarative_memory,"Declarative Memory",matches,negations)
    print('I recall the side order was.........................................***************************')
    print(retrieved_chunk['name'])

ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'state': 'start'}}},
    'negations': {},
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
