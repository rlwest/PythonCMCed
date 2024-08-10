# uses a generic motor production to do all actions

from utility import Utility
from production_cycle import ProductionCycle

# Initialize memories
working_memory = {'focus_buffer': {'state': 'bread1'}, 'motor_buffer': {'state': 'no_action'}}
environment_memory = {'bread1': {'location': 'counter'},
                      'cheese': {'location': 'counter'},
                      'ham': {'location': 'counter'},
                      'bread2': {'location': 'counter'}
                      }

memories = {
    'working_memory': working_memory,
    'environment_memory': environment_memory,
}

# Initialize productions
ProceduralProductions = []
MotorProductions = []


# Procedural Production to move bread1
def bread1(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'bread1',
        'slot': 'location',
        'newslotvalue': 'plate',
        'delay': 3
    })
    memories['working_memory']['focus_buffer']['state'] = 'cheese'
    print(f"bread1 executed. Updated working_memory: {memories['working_memory']}")


ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'state': 'bread1'}, 'motor_buffer': {'state': 'no_action'}}},
    'negations': {},
    'utility': 10,
    'action': bread1,
    'report': "bread1",
})


# Procedural Production to move cheese after bread1
def cheese(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'cheese',
        'slot': 'location',
        'newslotvalue': 'plate',
        'delay': 3
    })
    memories['working_memory']['focus_buffer']['state'] = 'ham'
    print(f"cheese executed. Updated working_memory: {memories['working_memory']}")


ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'state': 'cheese'}, 'motor_buffer': {'state': 'no_action'}}},
    'negations': {},
    'utility': 10,
    'action': cheese,
    'report': "cheese",
})


# Procedural Production to move ham after cheese
def ham(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'ham',
        'slot': 'location',
        'newslotvalue': 'plate',
        'delay': 3
    })
    memories['working_memory']['focus_buffer']['state'] = 'bread2'
    print(f"ham executed. Updated working_memory: {memories['working_memory']}")


ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'state': 'ham'}, 'motor_buffer': {'state': 'no_action'}}},
    'negations': {},
    'utility': 10,
    'action': ham,
    'report': "ham",
})


# Procedural Production to move bread2 after ham
def bread2(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'bread2',
        'slot': 'location',
        'newslotvalue': 'plate',
        'delay': 3
    })
    memories['working_memory']['focus_buffer']['state'] = 'done'
    print(f"bread2 executed. Updated working_memory: {memories['working_memory']}")


ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'state': 'bread2'}, 'motor_buffer': {'state': 'no_action'}}},
    'negations': {},
    'utility': 10,
    'action': bread2,
    'report': "bread2",
})


# Procedural Production to announce the sandwich is ready
def announce_sandwich(memories):
    print("Ham and cheese sandwich is ready!")


ProceduralProductions.append({
    'matches': {'working_memory': {'focus_buffer': {'state': 'done'}, 'motor_buffer': {'state': 'no_action'}}},
    'negations': {},
    'utility': 10,
    'action': announce_sandwich,
    'report': "announce_sandwich",
})


# Motor Production to move item
def move_item(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    env_object = motorbuffer['env_object']
    slot = motorbuffer['slot']
    newslotvalue = motorbuffer['newslotvalue']
    delay = motorbuffer['delay']

    memories['working_memory']['motor_buffer']['state'] = 'moving'
    print(f"move_item executed for {env_object}. Updated working_memory: {memories['working_memory']}")
    print(f'set action completion for {delay} cycles later')
    return delay


def delayed_action(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    env_object = motorbuffer['env_object']
    slot = motorbuffer['slot']
    newslotvalue = motorbuffer['newslotvalue']

    memories['environment_memory'][env_object][slot] = newslotvalue
    memories['working_memory']['motor_buffer']['state'] = 'no_action'
    print(f"delayed_action executed. Updated environment_memory: {memories['environment_memory']}")
    print(f"delayed_action executed. Updated working_memory: {memories['working_memory']}")


MotorProductions.append({
    'matches': {'working_memory': {'motor_buffer': {'state': 'do_action'}}},
    'negations': {},
    'utility': 10,
    'action': move_item,
    'report': "move_item",
    'delayed_action': delayed_action
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
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=22, millisecpercycle=10)
