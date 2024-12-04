# test chunk  utility

from CMCed.production_cycle import ProductionCycle
from CMCed.Cognitive_Functions import *

# Initialize memories
working_memory = {'focus_buffer': {'step': 1},
                  'target_buffer': {'lag1': 'rock', 'lag0': 'rock','utility': 101}}

# note, all chunks need to have a different name
# if two have the same name the second one will overwrite the first
declarative_memory = {'rp': {'lag1': 'rock', 'lag0': 'paper', 'utility': 100},
    'rr': {'lag1': 'rock', 'lag0': 'rock', 'utility': 100},
    'rs': {'lag1': 'rock', 'lag0': 'scissors', 'utility': 100},
    'pp': {'lag1': 'paper', 'lag0': 'paper', 'utility': 100},
    'pr': {'lag1': 'paper', 'lag0': 'rock', 'utility': 100},
    'ps': {'lag1': 'paper', 'lag0': 'scissors', 'utility': 100},
    'sp': {'lag1': 'scissors', 'lag0': 'paper', 'utility': 100},
    'sr': {'lag1': 'scissors', 'lag0': 'rock', 'utility': 100},
    'ss': {'lag1': 'scissors', 'lag0': 'scissors', 'utility': 100}
    }

environment_memory = {}



memories = {
    'working_memory': working_memory,
    'declarative_memory': declarative_memory,
    'environment_memory': environment_memory}

def do_steps(memories): # function for stepping through productions by counting
    current_step = memories['working_memory']['focus_buffer']['step']  # Accessing 'step' within 'focus_buffer'
    #print('The current step is', current_step)
    # Increment the step
    memories['working_memory']['focus_buffer']['step'] = current_step + 1
    next_step = memories['working_memory']['focus_buffer']['step']
    #print('Next step is', next_step)


# Initialize productions
ProceduralProductions = []
def p1(memories):
    # boost a chunk you have described using utility_change_by_description
    do_steps(memories)
    print('house salad utility should be boosted to 7')
    # describe the chunk you want boosted
    chunk_description = {'name': 'house_salad', 'condition': 'good'}
    print(chunk_description)
    # boost utility
    utility_change_by_description(memories, 'declarative_memory', chunk_description, amount=2, max_utility=10)
    #report_memory_contents(declarative_memory)
ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'step': 1}}},
    'negations': {},
    'utility': 10,
    'action': p1,
    'report': "step 1"
})
def p2(memories):
    # boost a chunk with a description from a buffer using utility_change_by_description
    do_steps(memories)
    # Access the target buffer directly
    chunk_description = memories['working_memory']['target_buffer']
    # Print the chunk description for clarity
    print("Extracted chunk description:", chunk_description)
    # Boost utility
    utility_change_by_description(memories, 'declarative_memory', chunk_description, amount=2, max_utility=200)
    report_memory_contents(declarative_memory)
ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'step': 2}}},
    'negations': {},
    'utility': 10,
    'action': p2,
    'report': "step 2"
})

# def p3(memories):
#     #boost a chunk by using its name using "utility_change" ****** different function for this shortcut
#     do_steps(memories)
#     print('poutine utility should be boosted to 2')
#     chunk_name = 'rr'  # Use the chunk name directly
#     print('poutine is the name of the chunk')
#     utility_change(memories, 'declarative_memory', chunk_name, amount=2, max_utility=10)
#     #report_memory_contents(declarative_memory)
# ProceduralProductions.append({
#     'matches': {'working_memory': {'focus_buffer': {'step': 3}}},
#     'negations': {},
#     'utility': 10,
#     'action': p3,
#     'report': "step 3"
# })
#
# def p4(memories):
#     # use a partial match, this is important because it means you don't need to specify the utility slot
#     # you can also skip other slots
#     do_steps(memories)
#     print('house salad utility should be boosted to 9')
#     # describe the chunk you want boosted
#     # note that the description can be partial as long as it only matches one chunk
#     chunk_description = {'condition': 'good', 'name': 'house_salad'}
#     print(chunk_description)
#     # boost utility
#     utility_change_by_description(memories, 'declarative_memory', chunk_description, amount=2, max_utility=10)
#     #report_memory_contents(declarative_memory)
# ProceduralProductions.append({
#     'matches': {'working_memory': {'focus_buffer': {'step': 4}}},
#     'negations': {},
#     'utility': 10,
#     'action': p4,
#     'report': "step 4"
# })
# def p5(memories):
#     # if two chunks match you will get an error message and nothing is boosted
#     do_steps(memories)
#     print('should be an error')
#     chunk_description = {'side_order': 'yes', 'name': 'house_salad'}
#     print(chunk_description)
#     # boost utility
#     utility_change_by_description(memories, 'declarative_memory', chunk_description, amount=2, max_utility=10)
#     #report_memory_contents(declarative_memory)Procedural
# ProceduralProductions.append({
#     'matches': {'working_memory': {'focus_buffer': {'step': 5}}},
#     'negations': {},
#     'utility': 10,
#     'action': p5,
#     'report': "step 5"
# })


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
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=7, millisecpercycle=50)
