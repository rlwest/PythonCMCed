from CMCed.production_cycle import ProductionCycle
from CMCed.Cognitive_Functions import *

environment_memory = {
    'agent1hand': {'hand': 'open', 'move': 'unknown'},
    'agent2hand': {'hand': 'open', 'move': 'unknown'}
}

agent1_working_memory = {
    'focus_buffer': {'state': 'start'},
    'lag_buffer': {'lag1': 'paper', 'lag0': 'unknown'}
}

agent1_declarative_memory = {
    'rp': {'lag1': 'rock', 'lag0': 'paper', 'utility': 100},
    'rr': {'lag1': 'rock', 'lag0': 'rock', 'utility': 100},
    'rs': {'lag1': 'rock', 'lag0': 'scissors', 'utility': 100},
    'pp': {'lag1': 'paper', 'lag0': 'paper', 'utility': 100},
    'pr': {'lag1': 'paper', 'lag0': 'rock', 'utility': 100},
    'ps': {'lag1': 'paper', 'lag0': 'scissors', 'utility': 100},
    'sp': {'lag1': 'scissors', 'lag0': 'paper', 'utility': 100},
    'sr': {'lag1': 'scissors', 'lag0': 'rock', 'utility': 100},
    'ss': {'lag1': 'scissors', 'lag0': 'scissors', 'utility': 100}
}

agent2_working_memory = {
    'focus_buffer': {'state': 'start'},
    'lag_buffer': {'lag1': 'scissors', 'lag0': 'unknown'}
}

agent2_declarative_memory = {
    'rp': {'lag1': 'rock', 'lag0': 'paper', 'utility': 100},
    'rr': {'lag1': 'rock', 'lag0': 'rock', 'utility': 100},
    'rs': {'lag1': 'rock', 'lag0': 'scissors', 'utility': 100},
    'pp': {'lag1': 'paper', 'lag0': 'paper', 'utility': 100},
    'pr': {'lag1': 'paper', 'lag0': 'rock', 'utility': 100},
    'ps': {'lag1': 'paper', 'lag0': 'scissors', 'utility': 100},
    'sp': {'lag1': 'scissors', 'lag0': 'paper', 'utility': 100},
    'sr': {'lag1': 'scissors', 'lag0': 'rock', 'utility': 100},
    'ss': {'lag1': 'scissors', 'lag0': 'scissors', 'utility': 100}
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
    print('111111111111111111111111111111111111')
    # decay agent1_declarative_memory
    decay_all_memory_chunks(memories, 'agent1_declarative_memory', 1)
    # get lag1 from lag_buffer
    lag1 = memories['agent1_working_memory']['lag_buffer']['lag1']
    print('lag_buffer is: ', memories['agent1_working_memory']['lag_buffer'])
    # use lag1 to retrieve prediction from agent1_declarative_memory
    target_memory = memories['agent1_declarative_memory']
    matches = {'lag1': lag1, 'lag0': '*'}  # already shifted lag1
    negations = {}
    retrieved_chunk = retrieve_memory_chunk(target_memory, matches, negations)
    print(f"Agent 1 recalls {retrieved_chunk}")

    memories['agent1_working_memory']['lag_buffer'] = retrieved_chunk
    print('lag_buffer updated to :', memories['agent1_working_memory']['lag_buffer'])
    memories['agent1_working_memory']['focus_buffer']['state'] = 'counter'


Agent1Productions.append({
    'matches': {'agent1_working_memory': {'focus_buffer': {'state': 'start'}}},
    'negations': {},
    'utility': 10,
    'action': recall_agent1_move,
    'report': "agent1_recall_move"
})


### get counter move

# Agent 1 counters 'paper' by choosing 'scissors'
def counter_paper_agent1(memories):
    print('111111111111111111111111111111111111')

    memories['environment_memory']['agent1hand']['move'] = 'scissors'
    print(environment_memory)

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
    print('111111111111111111111111111111111111')
    memories['environment_memory']['agent1hand']['move'] = 'rock'
    print(environment_memory)
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
    print('111111111111111111111111111111111111')
    memories['environment_memory']['agent1hand']['move'] = 'paper'
    print(environment_memory)

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

def agent1_checks_agent2_move(memories):
    print('111111111111111111111111111111111111')
    opponent_move = memories['environment_memory']['agent2hand']['move']
    print(f"Agent 1 sees that Agent 2 played: {opponent_move}")

    # update lag buffer to true state
    memories['agent1_working_memory']['lag_buffer']['lag0'] = opponent_move

    print(f"updated lag buffer for Agent 1 to actual result: {memories['agent1_working_memory']['lag_buffer']}")
    # boost the chunk in memory that corresponds to the chunk in the lag_buffer
    chunk_description = memories['agent1_working_memory']['lag_buffer']
    # Print the chunk description for clarity
    print("Extracted chunk description:", chunk_description)
    # Boost the utility
    utility_change_by_description(memories, 'agent1_declarative_memory', chunk_description, amount=1, max_utility=1000)
    # set for next round
    memories['agent1_working_memory']['focus_buffer']['state'] = 'start'
    # shift and update lag buffer for next guess
    memories['agent1_working_memory']['lag_buffer']['lag1'] = opponent_move
    memories['agent1_working_memory']['lag_buffer']['lag0'] = 'unknown'
    print(f"shifted lag buffer for Agent 1 for next round: {memories['agent1_working_memory']['lag_buffer']}")


Agent1Productions.append({
    'matches': {'agent1_working_memory': {'focus_buffer': {'state': 'check_move'}},
                'environment_memory': {'agent2hand': {'hand': 'open', 'move': '*'}}},
    'negations': {},
    'utility': 10,
    'action': agent1_checks_agent2_move,
    'report': "check_agent2_move"
})


#####################################################################################################
# Agent2Productions

def recall_agent2_move(memories):
    print('222222222222222222222222222222222222')

    # decay agent1_declarative_memory
    decay_all_memory_chunks(memories, 'agent2_declarative_memory', 1)
    # get lag1 from lag_buffer
    lag1 = memories['agent2_working_memory']['lag_buffer']['lag1']
    print('lag_buffer is: ', memories['agent2_working_memory']['lag_buffer'])
    # use lag1 to retrieve prediction from agent1_declarative_memory
    target_memory = memories['agent2_declarative_memory']
    matches = {'lag1': lag1, 'lag0': '*'}  # already shifted lag1
    negations = {}
    retrieved_chunk = retrieve_memory_chunk(target_memory, matches, negations)
    print(f"Agent 2 recalls {retrieved_chunk}")
    memories['agent2_working_memory']['lag_buffer'] = retrieved_chunk
    print('lag_buffer updated to :', memories['agent2_working_memory']['lag_buffer'])
    memories['agent2_working_memory']['focus_buffer']['state'] = 'counter'


Agent2Productions.append({
    'matches': {'agent2_working_memory': {'focus_buffer': {'state': 'start'}}},
    'negations': {},
    'utility': 10,
    'action': recall_agent2_move,
    'report': "agent2_recall_move"
})


### get counter move

def counter_paper_agent2(memories):
    print('222222222222222222222222222222222222')
    memories['environment_memory']['agent2hand']['move'] = 'scissors'
    print(environment_memory)

    print("Agent 2 chooses 'scissors' to counter paper")
    memories['agent2_working_memory']['focus_buffer']['state'] = 'check_move'


Agent2Productions.append({
    'matches': {'agent2_working_memory': {'focus_buffer': {'state': 'counter'}, 'lag_buffer': {'lag0': 'paper'}}},
    'negations': {},
    'utility': 10,
    'action': counter_paper_agent2,
    'report': "counter_paper_agent2"
})


def counter_scissors_agent2(memories):
    print('222222222222222222222222222222222222')
    memories['environment_memory']['agent2hand']['move'] = 'rock'
    print(environment_memory)

    print("Agent 2 chooses 'rock' to counter scissors")
    memories['agent2_working_memory']['focus_buffer']['state'] = 'check_move'


Agent2Productions.append({
    'matches': {'agent2_working_memory': {'focus_buffer': {'state': 'counter'}, 'lag_buffer': {'lag0': 'scissors'}}},
    'negations': {},
    'utility': 10,
    'action': counter_scissors_agent2,
    'report': "counter_scissors_agent2"
})


def counter_rock_agent2(memories):
    print('222222222222222222222222222222222222')
    memories['environment_memory']['agent2hand']['move'] = 'paper'
    print(environment_memory)

    print("Agent 2 chooses 'paper' to counter rock")
    memories['agent2_working_memory']['focus_buffer']['state'] = 'check_move'


Agent2Productions.append({
    'matches': {'agent2_working_memory': {'focus_buffer': {'state': 'counter'}, 'lag_buffer': {'lag0': 'rock'}}},
    'negations': {},
    'utility': 10,
    'action': counter_rock_agent2,
    'report': "counter_rock_agent2"
})


# Agent 1 checks Agent 2's move

def agent2_checks_agent1_move(memories):
    print('222222222222222222222222222222222222')
    opponent_move = memories['environment_memory']['agent1hand']['move']
    print(f"Agent 2 sees that Agent 1 played: {opponent_move}")

    # update lag buffer to true state
    memories['agent2_working_memory']['lag_buffer']['lag0'] = opponent_move

    print(f"updated lag buffer for Agent 2 to actual result: {memories['agent2_working_memory']['lag_buffer']}")
    # boost the chunk in memory that corresponds to the chunk in the lag_buffer
    chunk_description = memories['agent2_working_memory']['lag_buffer']
    # Print the chunk description for clarity
    print("Extracted chunk description:", chunk_description)
    # Boost the utility
    utility_change_by_description(memories, 'agent2_declarative_memory', chunk_description, amount=1, max_utility=1000)
    # set for next round
    memories['agent2_working_memory']['focus_buffer']['state'] = 'start'
    # shift and update lag buffer for next guess
    memories['agent2_working_memory']['lag_buffer']['lag1'] = opponent_move
    memories['agent2_working_memory']['lag_buffer']['lag0'] = 'unknown'
    print(f"shifted lag buffer for Agent 2 for next round: {memories['agent2_working_memory']['lag_buffer']}")



Agent2Productions.append({
    'matches': {'agent2_working_memory': {'focus_buffer': {'state': 'check_move'}},
                'environment_memory': {'agent1hand': {'hand': 'open', 'move': '*'}}},
    'negations': {},
    'utility': 10,
    'action': agent2_checks_agent1_move,
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

ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=200, millisecpercycle=10)



