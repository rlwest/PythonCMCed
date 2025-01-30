from CMCed.production_cycle import ProductionCycle

working_memory = {'focusbuffer': {'state': 'a'}}
memories = {'working_memory': working_memory}

ProceduralProductions = []

def a_to_b(memories):
    memories['working_memory']['focusbuffer']['state'] = 'b'
    print(f"Updated working_memory: {memories['working_memory']}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'a'}}},
    'negations': {},
    'utility': 10,
    'action': a_to_b,
    'report': "match to focusbuffer, change state from a to b"
})

def b_to_c(memories):
    memories['working_memory']['focusbuffer']['state'] = 'c'
    print(f"Updated working_memory: {memories['working_memory']}")
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'b'}}},
    'negations': {},
    'utility': 10,
    'action': b_to_c,
    'report': "match to focusbuffer, change state from b to *"
})

## set up the production cycle

# Production system delays in ticks
ProductionSystem1_Countdown = 3

# Store the number of cycles for all production systems to fire and reset
DelayResetValues = {
    'ProductionSystem1': ProductionSystem1_Countdown
}

# Dictionary of all production systems and delays
AllProductionSystems = {
    'ProductionSystem1': [ProceduralProductions, ProductionSystem1_Countdown],
}

# Initialize ProductionCycle
ps = ProductionCycle()

# Run the cycle with custom parameters
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=10, millisecpercycle=10)
