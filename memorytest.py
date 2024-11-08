
from CMCed.production_cycle import ProductionCycle
from CMCed.Cognitive_Functions import *

# Initialize memories
working_memory = {'focus_buffer': {'step': 1}}
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


# negations = {}

# cue = {'matches': {'side_order': 'yes', 'condition': 'good'}, 'negations': {}} # positive matching and mismatching works
# cue = {'matches': {'side_order': 'yes', 'condition': 'good'}, 'negations': {'name': 'fries'}} # negation works
# cue = {'matches': {'side_order': 'yes', 'condition': '*'}, 'negations': {'name': 'fries'}} # wild card works when it is in existing slot
# cue = {'matches': {'side_order': 'yes', 'bat': '*'}, 'negations': {'cat': '*'}} # wild card works when it is in non existing slot
# cue = {'matches': {'side_order': 'yes', 'temperature': '*'}, 'negations': {'name': 'fries'}}
# cue = {'matches': {'side_order': 'yes', 'condition': '*'}, 'negations': {'name': '*'}}


def recall_order1(memories):
    # recall order
    buffer = declarative_memory
    matches = {'side_order': 'yes', 'condition': '*'}
    negations = {'extra': '*'}
    retrieved_chunk = retrieve_memory_chunk(buffer, matches, negations)
    print('I recall the order was ', retrieved_chunk['name'])
    # next order
    step = memories['working_memory']['focus_buffer']['step']
    print('I recall order number.........................................', step)
    memories['working_memory']['focus_buffer']['step'] = step + 1
    next_step = memories['working_memory']['focus_buffer']['step']
    print('next step is', next_step)
ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'step': 1}}},
    'negations': {},
    'utility': 10,
    'action': recall_order1,
    'report': "announce_sandwich"
})
def recall_order2(memories):
    buffer = declarative_memory
    matches = {'side_order': 'yes', 'condition': '*'}
    negations = {'extra': '*'}
    retrieved_chunk = retrieve_memory_chunk(buffer, matches, negations)
    print('I recall the order was ', retrieved_chunk['name'])
    # next order
    step = memories['working_memory']['focus_buffer']['step']
    print('I recall order number.........................................', step)
    memories['working_memory']['focus_buffer']['step'] = step + 1
    next_step = memories['working_memory']['focus_buffer']['step']
    print('next step is', next_step)
ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'step': 2}}},
    'negations': {},
    'utility': 10,
    'action': recall_order2,
    'report': "announce_sandwich"
})
def recall_order3(memories):
    buffer = declarative_memory
    matches = {'side_order': 'yes', 'condition': '*'}
    negations = {'extra': '*'}
    retrieved_chunk = retrieve_memory_chunk(buffer, matches, negations)
    print('I recall the order was ', retrieved_chunk['name'])
    # next order
    step = memories['working_memory']['focus_buffer']['step']
    print('I recall order number.........................................', step)
    memories['working_memory']['focus_buffer']['step'] = step + 1
    next_step = memories['working_memory']['focus_buffer']['step']
    print('next step is', next_step)
ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'step': 3}}},
    'negations': {},
    'utility': 10,
    'action': recall_order2,
    'report': "announce_sandwich"
})
def recall_order4(memories):
    buffer = declarative_memory
    matches = {'side_order': 'yes', 'condition': '*'}
    negations = {'extra': '*'}
    retrieved_chunk = retrieve_memory_chunk(buffer, matches, negations)
    print('I recall the order was ', retrieved_chunk['name'])
    # next order
    step = memories['working_memory']['focus_buffer']['step']
    print('I recall order number.........................................', step)
    memories['working_memory']['focus_buffer']['step'] = step + 1
    next_step = memories['working_memory']['focus_buffer']['step']
    print('next step is', next_step)
ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'step': 4}}},
    'negations': {},
    'utility': 10,
    'action': recall_order2,
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
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=7, millisecpercycle=10)
