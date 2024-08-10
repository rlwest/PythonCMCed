#  this file uses motor productions to model actions in the environment that take time

from utility import Utility
from production_cycle import ProductionCycle

### works but only complete up to cheese
### may be some issues still

working_memory = {'focusbuffer': {'state': 'bread1'}, 'motorbuffer': {'state': 'no_action'}}
environment_memory = {'bread1': {'location': 'counter'},
                      'cheese': {'location': 'counter'},
                      'ham': {'location': 'counter'},
                      'bread2': {'location': 'counter'}
                      }

memories = {
    'working_memory': working_memory,
    'environment_memory': environment_memory,
}

ProceduralProductions = []
MotorProductions = []

def bread1(memories):
    memories['working_memory']['motorbuffer']['state'] = 'do_bread1'
    memories['working_memory']['focusbuffer']['state'] = 'cheese'
    print(f"bread1 executed. Updated working_memory: {memories['working_memory']}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'bread1'}, 'motorbuffer': {'state': 'no_action'}}},
    'negations': {},
    'utility': 10,
    'action': bread1,
    'report': "bread1",
})

def move_bread(memories):
    memories['working_memory']['motorbuffer']['state'] = 'moving_bread1'
    print(f"move_bread executed. Updated working_memory: {memories['working_memory']}")
    print('set action completion for 3 cycles later')
    return 3

def delayed_mb(memories):
    memories['environment_memory']['bread1']['location'] = 'plate'
    memories['working_memory']['motorbuffer']['state'] = 'no_action'
    print(f"delayed_action executed. Updated environment_memory: {memories['environment_memory']}")
    print(f"delayed_action executed. Updated working_memory: {memories['working_memory']}")
MotorProductions.append({
    'matches': {'working_memory': {'motorbuffer': {'state': 'do_bread1'}}},
    'negations': {},
    'utility': 10,
    'action': move_bread,
    'report': "move_bread",
    'delayed_action': delayed_mb
})

def cheese(memories):
    memories['working_memory']['motorbuffer']['state'] = 'do_cheese'
    memories['working_memory']['focusbuffer']['state'] = 'ham'
    print(f"cheese executed. Updated working_memory: {memories['working_memory']}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'cheese'}, 'motorbuffer': {'state': 'no_action'}}},
    'negations': {},
    'utility': 10,
    'action': cheese,
    'report': "cheese",
})

def move_cheese(memories):
    memories['working_memory']['motorbuffer']['state'] = 'moving_cheese'
    print(f"move_cheese executed. Updated working_memory: {memories['working_memory']}")
    print('set action completion for 3 cycles later')
    return 3

def delayed_mc(memories):
    memories['environment_memory']['cheese']['location'] = 'plate'
    memories['working_memory']['motorbuffer']['state'] = 'no_action'
    print(f"delayed_action executed. Updated environment_memory: {memories['environment_memory']}")
    print(f"delayed_action executed. Updated working_memory: {memories['working_memory']}")
MotorProductions.append({
    'matches': {'working_memory': {'motorbuffer': {'state': 'do_cheese'}}},
    'negations': {},
    'utility': 10,
    'action': move_cheese,
    'report': "move_cheese",
    'delayed_action': delayed_mc
})

def ham(memories):
    memories['working_memory']['motorbuffer']['state'] = 'do_ham'
    memories['working_memory']['focusbuffer']['state'] = 'bread2'
    print(f"ham executed. Updated working_memory: {memories['working_memory']}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'ham'}, 'motorbuffer': {'state': 'no_action'}}},
    'negations': {},
    'utility': 10,
    'action': ham,
    'report': "ham",
})

def move_ham(memories):
    memories['working_memory']['motorbuffer']['state'] = 'moving_ham'
    print(f"move_ham executed. Updated working_memory: {memories['working_memory']}")
    print('set action completion for 3 cycles later')
    return 3

def delayed_mh(memories):
    memories['environment_memory']['ham']['location'] = 'plate'
    memories['working_memory']['motorbuffer']['state'] = 'no_action'
    print(f"delayed_action executed. Updated environment_memory: {memories['environment_memory']}")
    print(f"delayed_action executed. Updated working_memory: {memories['working_memory']}")
MotorProductions.append({
    'matches': {'working_memory': {'motorbuffer': {'state': 'do_ham'}}},
    'negations': {},
    'utility': 10,
    'action': move_ham,
    'report': "move_ham",
    'delayed_action': delayed_mh
})

def bread2(memories):
    memories['working_memory']['motorbuffer']['state'] = 'do_bread2'
    memories['working_memory']['focusbuffer']['state'] = 'done'
    print(f"bread2 executed. Updated working_memory: {memories['working_memory']}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'bread2'}, 'motorbuffer': {'state': 'no_action'}}},
    'negations': {},
    'utility': 10,
    'action': bread2,
    'report': "bread2",
})

def move_bread2(memories):
    memories['working_memory']['motorbuffer']['state'] = 'moving_bread2'
    print(f"move_bread2 executed. Updated working_memory: {memories['working_memory']}")
    print('set action completion for 3 cycles later')
    return 3

def delayed_mb2(memories):
    memories['environment_memory']['bread2']['location'] = 'plate'
    memories['working_memory']['motorbuffer']['state'] = 'no_action'
    print("The ham and cheese sandwich is ready!")
    print(f"delayed_action executed. Updated environment_memory: {memories['environment_memory']}")
    print(f"delayed_action executed. Updated working_memory: {memories['working_memory']}")
MotorProductions.append({
    'matches': {'working_memory': {'motorbuffer': {'state': 'do_bread2'}}},
    'negations': {},
    'utility': 10,
    'action': move_bread2,
    'report': "move_bread2",
    'delayed_action': delayed_mb2
})

# Production system delays in ticks
ProductionSystem1_Countdown = 1
ProductionSystem2_Countdown = 1

# Stores the number of cycles for a production system to fire and reset
DelayResetValues = {
    'ProductionSystem1': ProductionSystem1_Countdown,
    'ProductionSystem2': ProductionSystem2_Countdown
}

# Dictionary of all production systems and delays
AllProductionSystems = {
    'ProductionSystem1': [ProceduralProductions, ProductionSystem1_Countdown],
    'ProductionSystem2': [MotorProductions, ProductionSystem2_Countdown]
}

# Initialize ProductionCycle
ps = ProductionCycle()

# Run the cycle with custom parameters
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=20, millisecpercycle=10)


