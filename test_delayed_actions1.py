from utility import Utility
from production_cycle import ProductionCycle

working_memory = {'focusbuffer': {'state': 'a'}}
environment_memory = {'button1': {'state': '1'}}
emotional_memory = {'focusbuffer': {'state': 'neurtal'}}
memories = {
    'working_memory': working_memory,
    'environment_memory': environment_memory,
    'emotional_memory': emotional_memory
}

ProceduralProductions = []

def pp1(memories):
    memories['working_memory']['focusbuffer']['state'] = 'b'
    print(f"pp1 executed. Updated working_memory: {memories['working_memory']}")
    print('set delayed_pp1 for 4 cycles later &&&&&&&&&&&&&&&&&&&&&&&&&&&')
    return 4  # Set delay for the delayed action

def delayed_pp1(memories):
    memories['emotional_memory']['focusbuffer']['state'] = 'happy'
    print(f"delayed_pp1 executed. Updated working_memory: {memories['emotional_memory']}")
    print('This should print at 50 msec = 10 msec + 4 cycles &&&&&&&&&&&&&&&&&&&&&&&&&&&&')

ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'a'}}},
    'negations': {},
    'utility': 10,
    'action': pp1,
    'report': "match to focusbuffer, change state from a to b",
    'delayed_action': delayed_pp1
})




def pp2(memories):
    memories['working_memory']['focusbuffer']['state'] = '*'
    print(f"pp2 executed. Updated working_memory: {memories['working_memory']}")
    print('set delayed_pp2 for 4 cycles later ****************************')
    d=4
    return d  # Set delay for the delayed action

def delayed_pp2(memories):
    memories['emotional_memory']['focusbuffer']['state'] = 'troubled'
    print(f"delayed_pp2 executed")
    print('This should print at 60 msec = 20 msec + 4 cycles *******************')


ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'b'}}},
    'negations': {},
    'utility': 10,
    'action': pp2,
    'report': "match to focusbuffer, change state from b to *",
    'delayed_action': delayed_pp2
})

MotorProductions = []

def mp1(memories):
    memories['environment_memory']['button1']['state'] = '2'
    print(f"mp1 executed. Updated environment_memory: {memories['environment_memory']}")
    print('set delayed_mp1 for 3 cycles later @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    return 3  # Set delay for the delayed action

def delayed_mp1(memories):
    memories['environment_memory']['button1']['state'] = '3'
    print(f"delayed_mp1 executed. Updated environment_memory: {memories['environment_memory']}")
    print('This should print at 40 msec = 10 msec + 3 cycles @@@@@@@@@@@@@@@@@@@@@@@@@@@@@')


MotorProductions.append({
    'matches': {'environment_memory': {'button1': {'state': '1'}}},
    'negations': {},
    'utility': 10,
    'action': mp1,
    'report': "match to button1, change state from 1 to 2",
    'delayed_action': delayed_mp1
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
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=10, millisecpercycle=10)
