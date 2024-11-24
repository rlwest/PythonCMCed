
from CMCed.production_cycle import ProductionCycle
from CMCed.Cognitive_Functions import *

# Initialize memories
working_memory = {'focus_buffer': {'step': 1}}
declarative_memory = {}
environment_memory = {}

memories = {
    'working_memory': working_memory,
    'declarative_memory': declarative_memory,
    'environment_memory': environment_memory,
}

def do_steps(memories): # function for stepping through productions by counting
    current_step = memories['working_memory']['focus_buffer']['step']  # Accessing 'step' within 'focus_buffer'
    print('The current step is', current_step)
    # Increment the step
    memories['working_memory']['focus_buffer']['step'] = current_step + 1
    next_step = memories['working_memory']['focus_buffer']['step']
    print('Next step is', next_step)


# Initialize productions PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
ProceduralProductions = []
def p1(memories):
    do_steps(memories)
ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'step': 1}}},
    'negations': {},
    'utility': 10,
    'action': p1,
    'report': "step 1"
})
def p2(memories):
    do_steps(memories)
ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'step': 2}}},
    'negations': {},
    'utility': 10,
    'action': p2,
    'report': "step 2"
})

def p3(memories):
    do_steps(memories)
ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'step': 3}}},
    'negations': {},
    'utility': 10,
    'action': p3,
    'report': "step 3"
})

def p4(memories):
    do_steps(memories)
ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'step': 4}}},
    'negations': {},
    'utility': 10,
    'action': p4,
    'report': "step 4"
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
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=5, millisecpercycle=50)
