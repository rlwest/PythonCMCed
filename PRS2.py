from CMCed.production_cycle import ProductionCycle
from CMCed.Cognitive_Functions import *

environment_memory = {
    'agent1hand': {'hand': 'closed', 'move':'unknown'},
    'agent2hand': {'hand': 'closed', 'move':'unknown'}
}

agent1_working_memory = {
    'focus_buffer': {'state': 'start'},
    'lag_buffer': {'lag1': 'rock', 'lag0': 'paper'}
}

agent1_declarative_memory = {
    'sequence1': {'lag1': 'rock', 'lag0': 'paper', 'utility': 100},
    'sequence2': {'lag1': 'rock', 'lag0': 'rock', 'utility': 100},
    'sequence3': {'lag1': 'rock', 'lag0': 'scissors', 'utility': 100},
    'sequence4': {'lag1': 'paper', 'lag0': 'paper', 'utility': 100},
    'sequence5': {'lag1': 'paper', 'lag0': 'rock', 'utility': 100},
    'sequence6': {'lag1': 'paper', 'lag0': 'scissors', 'utility': 100},
    'sequence7': {'lag1': 'scissors', 'lag0': 'paper', 'utility': 100},
    'sequence8': {'lag1': 'scissors', 'lag0': 'rock', 'utility': 100},
    'sequence9': {'lag1': 'scissors', 'lag0': 'scissors', 'utility': 100}
}

agent2_working_memory = {
    'focus_buffer': {'state': 'start'},
    'lag_buffer': {'lag2': 'rock', 'lag1': 'rock', 'lag0': 'paper'}
}

agent2_declarative_memory = {
    'sequence1': {'lag2': 'rock', 'lag1': 'rock', 'lag0': 'paper', 'utility': 100},
    'sequence2': {'lag2': 'rock', 'lag1': 'rock', 'lag0': 'rock', 'utility': 100},
    'sequence3': {'lag2': 'rock', 'lag1': 'rock', 'lag0': 'scissors', 'utility': 100},
    'sequence4': {'lag2': 'rock', 'lag1': 'paper', 'lag0': 'paper', 'utility': 100},
    'sequence5': {'lag2': 'rock', 'lag1': 'paper', 'lag0': 'rock', 'utility': 100},
    'sequence6': {'lag2': 'rock', 'lag1': 'paper', 'lag0': 'scissors', 'utility': 100},
    'sequence7': {'lag2': 'rock', 'lag1': 'scissors', 'lag0': 'paper', 'utility': 100},
    'sequence8': {'lag2': 'rock', 'lag1': 'scissors', 'lag0': 'rock', 'utility': 100},
    'sequence9': {'lag2': 'rock', 'lag1': 'scissors', 'lag0': 'scissors', 'utility': 100},
    'sequence10': {'lag2': 'paper', 'lag1': 'rock', 'lag0': 'paper', 'utility': 100},
    'sequence11': {'lag2': 'paper', 'lag1': 'rock', 'lag0': 'rock', 'utility': 100},
    'sequence12': {'lag2': 'paper', 'lag1': 'rock', 'lag0': 'scissors', 'utility': 100},
    'sequence13': {'lag2': 'paper', 'lag1': 'paper', 'lag0': 'paper', 'utility': 100},
    'sequence14': {'lag2': 'paper', 'lag1': 'paper', 'lag0': 'rock', 'utility': 100},
    'sequence15': {'lag2': 'paper', 'lag1': 'paper', 'lag0': 'scissors', 'utility': 100},
    'sequence16': {'lag2': 'paper', 'lag1': 'scissors', 'lag0': 'paper', 'utility': 100},
    'sequence17': {'lag2': 'paper', 'lag1': 'scissors', 'lag0': 'rock', 'utility': 100},
    'sequence18': {'lag2': 'paper', 'lag1': 'scissors', 'lag0': 'scissors', 'utility': 100},
    'sequence19': {'lag2': 'scissors', 'lag1': 'rock', 'lag0': 'paper', 'utility': 100},
    'sequence20': {'lag2': 'scissors', 'lag1': 'rock', 'lag0': 'rock', 'utility': 100},
    'sequence21': {'lag2': 'scissors', 'lag1': 'rock', 'lag0': 'scissors', 'utility': 100},
    'sequence22': {'lag2': 'scissors', 'lag1': 'paper', 'lag0': 'paper', 'utility': 100},
    'sequence23': {'lag2': 'scissors', 'lag1': 'paper', 'lag0': 'rock', 'utility': 100},
    'sequence24': {'lag2': 'scissors', 'lag1': 'paper', 'lag0': 'scissors', 'utility': 100},
    'sequence25': {'lag2': 'scissors', 'lag1': 'scissors', 'lag0': 'paper', 'utility': 100},
    'sequence26': {'lag2': 'scissors', 'lag1': 'scissors', 'lag0': 'rock', 'utility': 100},
    'sequence27': {'lag2': 'scissors', 'lag1': 'scissors', 'lag0': 'scissors', 'utility': 100}
}

# memory dictionary
memories = {
    'agent1_working_memory': agent1_working_memory,
    'agent2_working_memory': agent2_working_memory,
    'environment_memory': environment_memory,
    'agent1_declarative_memory': agent1_declarative_memory,
    'agent2_declarative_memory': agent2_declarative_memory,
}

# Procedural Productions
Agent1Productions = []
Agent2Productions = []

#######################################################################################################
# Agent1Productions

def recall_agent1_move(memories):
    # decay agent1_declarative_memory
    decay_all_memory_chunks(memories, 'agent1_declarative_memory', 1)
    # get lag1 from lag_buffer
    lag1 = memories['agent1_working_memory']['lag_buffer']['lag1']
    print('lag_buffer is: ',memories['agent1_working_memory']['lag_buffer'])
    print('lag1 is: ',lag1)
    # use lag1 to retrieve prediction from agent1_declarative_memory
    target_memory = memories['agent1_declarative_memory']
    matches = {'lag1': lag1, 'lag0': '*'}  # already shifted lag1
    negations = {}
    retrieved_chunk = retrieve_memory_chunk(target_memory, matches, negations)
    print(f"Agent 1 recalls {retrieved_chunk}")

    memories['agent1_working_memory']['lag_buffer'] = retrieved_chunk
    print('lag_buffer updated to :',memories['agent1_working_memory']['lag_buffer'])
    memories['agent1_working_memory']['focus_buffer']['state'] = 'counter'
Agent1Productions.append({
    'matches': {'agent1_working_memory': {'focus_buffer': {'state': 'start'}},
                'environment_memory': {'agent1hand': {'hand': 'closed', 'move':'unknown'}}},
    'negations': {},
    'utility': 10,
    'action': recall_agent1_move,
    'report': "agent1_recall_move"
})

### get counter move

# Agent 1 counters 'paper' by choosing 'scissors'
def counter_paper_agent1(memories):
    memories['environment_memory']['agent1hand']['choice'] = 'scissors'

    print("Agent 1 chooses 'scissors' to counter paper")
    memories['agent1_working_memory']['focus_buffer']['state'] = 'check_move'
Agent1Productions.append({
    'matches': {'agent1_working_memory': {'focus_buffer': {'state': 'counter'}, 'lag_buffer': {'lag0': 'paper'}}},
    'negations': {},
    'utility': 10,
    'action': counter_paper_agent1,
    'report': "counter_paper_agent1"
})

# Agent 1 counters 'scissors' by choosing 'rock'
def counter_scissors_agent1(memories):
    memories['environment_memory']['agent1hand']['choice'] = 'rock'
    print("Agent 1 chooses 'rock' to counter scissors")
    memories['agent1_working_memory']['focus_buffer']['state'] = 'check_move'
Agent1Productions.append({
    'matches': {'agent1_working_memory': {'focus_buffer': {'state': 'counter'}, 'lag_buffer': {'lag0': 'scissors'}}},
    'negations': {},
    'utility': 10,
    'action': counter_scissors_agent1,
    'report': "counter_scissors_agent1"
})

# Agent 1 counters 'rock' by choosing 'paper'
def counter_rock_agent1(memories):
    memories['environment_memory']['agent1hand']['choice'] = 'paper'
    print("Agent 1 chooses 'paper' to counter rock")
    memories['agent1_working_memory']['focus_buffer']['state'] = 'check_move'
Agent1Productions.append({
    'matches': {'agent1_working_memory': {'focus_buffer': {'state': 'counter'}, 'lag_buffer': {'lag0': 'rock'}}},
    'negations': {},
    'utility': 10,
    'action': counter_rock_agent1,
    'report': "counter_rock_agent1"
})


# Agent 1 checks Agent 2's move

def check_agent2_move(memories):
    opponent_move = memories['environment_memory']['agent2hand']['move']
    print(f"Agent 1 sees that Agent 2 played: {opponent_move}")
    memories['agent1_working_memory']['lag_buffer']['lag0'] = opponent_move
    print(f"updated lag buffer for Agent 1: {memories['agent1_working_memory']['lag_buffer']}")
    # boost the chunk in memory that corresponds to the chunk in the lag_buffer
    chunk_description = memories['agent1_working_memory']['lag_buffer']
    # Print the chunk description for clarity
    print("Extracted chunk description:", chunk_description)
    # Boost the utility
    utility_change_by_description(memories, 'agent1_working_memory', chunk_description, amount=5)
    # memories['environment_memory']['refinstructions']['agent1_done'] = 'done2'
    memories['environment_memory']['agent1hand'].update({'hand': 'closed', 'move': 'unknown'})
    memories['agent1_working_memory']['focus_buffer']['state'] = 'start'
Agent1Productions.append({
    'matches': {'agent1_working_memory': {'focus_buffer': {'state': 'check_move'}},
                'environment_memory': {'agent2hand': {'hand': 'open', 'move':'*'}}},
    'negations': {},
    'utility': 10,
    'action': check_agent2_move,
    'report': "check_agent2_move"
})

def waiting_for_move(memories):
    print('waiting........................')
Agent1Productions.append({
    'matches': {'agent1_working_memory': {'focus_buffer': {'state': 'check_move'}},
                'environment_memory': {'agent2hand': {'hand': 'closed', 'move':'*'}}},
    'negations': {},
    'utility': 10,
    'action': waiting_for_move,
    'report': "check_agent2_move"
})


#####################################################################################################
# Agent2Productions
def recall_agent1_move(memories):
    # decay agent1_declarative_memory
    decay_all_memory_chunks(memories, 'agent1_declarative_memory', 1)
    # get lag1 from lag_buffer
    lag1 = memories['agent1_working_memory']['lag_buffer']['lag1']
    print('lag_buffer is: ',memories['agent1_working_memory']['lag_buffer'])
    print('lag1 is: ',lag1)
    # use lag1 to retrieve prediction from agent1_declarative_memory
    target_memory = memories['agent1_declarative_memory']
    matches = {'lag1': lag1, 'lag0': '*'}  # already shifted lag1
    negations = {}
    retrieved_chunk = retrieve_memory_chunk(target_memory, matches, negations)
    print(f"Agent 1 recalls {retrieved_chunk}")

    memories['agent2_working_memory']['lag_buffer'] = retrieved_chunk
    print('lag_buffer updated to :',memories['agent1_working_memory']['lag_buffer'])
    memories['agent2_working_memory']['focus_buffer']['state'] = 'counter'
Agent1Productions.append({
    'matches': {'agent2_working_memory': {'focus_buffer': {'state': 'start'}},
                'environment_memory': {'agent1hand': {'hand': 'closed', 'move':'unknown'}}},
    'negations': {},
    'utility': 10,
    'action': recall_agent1_move,
    'report': "agent1_recall_move"
})

### get counter move

# Agent 1 counters 'paper' by choosing 'scissors'
def counter_paper_agent1(memories):
    memories['environment_memory']['agent2hand']['choice'] = 'scissors'

    print("Agent 1 chooses 'scissors' to counter paper")
    memories['agent2_working_memory']['focus_buffer']['state'] = 'check_move'
Agent1Productions.append({
    'matches': {'agent2_working_memory': {'focus_buffer': {'state': 'counter'}, 'lag_buffer': {'lag0': 'paper'}}},
    'negations': {},
    'utility': 10,
    'action': counter_paper_agent1,
    'report': "counter_paper_agent1"
})

# Agent 1 counters 'scissors' by choosing 'rock'
def counter_scissors_agent1(memories):
    memories['environment_memory']['agent2hand']['choice'] = 'rock'
    print("Agent 1 chooses 'rock' to counter scissors")
    memories['agent2_working_memory']['focus_buffer']['state'] = 'check_move'
Agent1Productions.append({
    'matches': {'agent2_working_memory': {'focus_buffer': {'state': 'counter'}, 'lag_buffer': {'lag0': 'scissors'}}},
    'negations': {},
    'utility': 10,
    'action': counter_scissors_agent1,
    'report': "counter_scissors_agent1"
})

# Agent 1 counters 'rock' by choosing 'paper'
def counter_rock_agent1(memories):
    memories['environment_memory']['agent2hand']['choice'] = 'paper'
    print("Agent 1 chooses 'paper' to counter rock")
    memories['agent2_working_memory']['focus_buffer']['state'] = 'check_move'
Agent1Productions.append({
    'matches': {'agent2_working_memory': {'focus_buffer': {'state': 'counter'}, 'lag_buffer': {'lag0': 'rock'}}},
    'negations': {},
    'utility': 10,
    'action': counter_rock_agent1,
    'report': "counter_rock_agent1"
})


# Agent 1 checks Agent 2's move

def check_agent2_move(memories):
    opponent_move = memories['environment_memory']['agent1hand']['move']
    print(f"Agent 2 sees that Agent 1 played: {opponent_move}")
    memories['agent2_working_memory']['lag_buffer']['lag0'] = opponent_move
    print(f"updated lag buffer for Agent 2: {memories['agent2_working_memory']['lag_buffer']}")
    # boost the chunk in memory that corresponds to the chunk in the lag_buffer
    chunk_description = memories['agent1_working_memory']['lag_buffer']
    # Print the chunk description for clarity
    print("Extracted chunk description:", chunk_description)
    # Boost the utility
    utility_change_by_description(memories, 'agent2_working_memory', chunk_description, amount=5)
    # memories['environment_memory']['refinstructions']['agent1_done'] = 'done2'
    memories['environment_memory']['agent2hand'].update({'hand': 'closed', 'move': 'unknown'})
    memories['agent2_working_memory']['focus_buffer']['state'] = 'start'
Agent1Productions.append({
    'matches': {'agent2_working_memory': {'focus_buffer': {'state': 'check_move'}},
                'environment_memory': {'agent2hand': {'hand': 'open', 'move':'*'}}},
    'negations': {},
    'utility': 10,
    'action': check_agent2_move,
    'report': "check_agent2_move"
})

def waiting_for_move(memories):
    print('waiting........................')
Agent1Productions.append({
    'matches': {'agent2_working_memory': {'focus_buffer': {'state': 'check_move'}},
                'environment_memory': {'agent2hand': {'hand': 'closed', 'move':'*'}}},
    'negations': {},
    'utility': 10,
    'action': waiting_for_move,
    'report': "check_agent2_move"
})


# Production system delays in ticks
Agent1Productions_Countdown = 1
Agent2Productions_Countdown = 1

# Stores the number of cycles for a production system to fire and reset

DelayResetValues = {
    'Agent1Productions': Agent1Productions_Countdown,
    'Agent2Productions': Agent2Productions_Countdown,
}

# Dictionary of all production systems and delays

AllProductionSystems = {
    'Agent1Productions': [Agent1Productions, Agent1Productions_Countdown],
    'Agent2Productions': [Agent2Productions, Agent2Productions_Countdown]
}

# Initialize ProductionCycle

ps = ProductionCycle()

# Run the cycle with custom parameters

ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=10, millisecpercycle=10)

