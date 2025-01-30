from CMCed.production_cycle import ProductionCycle

working_memory = {'focusbuffer': {'state': 'bread1'}}
environment = {'bread1': {'location': 'counter'},
                'cheese': {'location': 'counter'},
                'ham': {'location': 'counter'},
                'bread2': {'location': 'counter'}}

memories = {
    'working_memory': working_memory,
    'environment': environment
}

ProceduralProductions = []

def bread1(memories):
    memories['working_memory']['focusbuffer']['state'] = 'cheese'
    print(f"bread bottom executed. Updated working_memory: {memories['working_memory']}")
    print('set action completion for 3 cycles later')
    return 2
def delayed_mb(memories):
    memories['environment']['bread1']['location'] = 'plate'
    print(f"{memories['environment']}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'bread1'}}},
    'negations': {},
    'utility': 10,
    'action': bread1,
    'delayed_action': delayed_mb,
    'report': "bread1",
})

def cheese(memories):
    memories['working_memory']['focusbuffer']['state'] = 'ham'
    print(f"cheese executed. Updated working_memory: {memories['working_memory']}")
    memories['environment']['cheese']['location'] = 'plate'
    print(f"{memories['environment']}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'cheese'}},
                'environment': {'bread1': {'location': 'plate'}}},
    'negations': {},
    'utility': 10,
    'action': cheese,
    'report': "cheese",
})

def ham(memories):
    memories['working_memory']['focusbuffer']['state'] = 'bread2'
    print(f"ham executed. Updated working_memory: {memories['working_memory']}")
    memories['environment']['ham']['location'] = 'plate'
    print(f"{memories['environment']}")
    print(f"ham executed. Updated working_memory: {memories['working_memory']}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'ham'}}},
    'negations': {},
    'utility': 10,
    'action': ham,
    'report': "ham",
})

def bread2(memories):
    memories['working_memory']['focusbuffer']['state'] = 'done'
    print(f"bread top executed. Updated working_memory: {memories['working_memory']}")
    memories['environment']['bread2']['location'] = 'plate'
    print(f"{memories['environment']}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'bread2'}}},
    'negations': {},
    'utility': 10,
    'action': bread2,
    'report': "bread2",
})

# Production system delays in ticks
ProductionSystem1_Countdown = 1

# Stores the number of cycles for a production system to fire and reset
DelayResetValues = {
    'ProductionSystem1': ProductionSystem1_Countdown}

# Dictionary of all production systems and delays
AllProductionSystems = {
    'ProductionSystem1': [ProceduralProductions, ProductionSystem1_Countdown]}

# Initialize ProductionCycle
ps = ProductionCycle()

# Run the cycle with custom parameters
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=7, millisecpercycle=50)

