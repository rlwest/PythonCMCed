# everything seems to work, lag 1 vs lag 1, no ref

import pandas as pd
import matplotlib.pyplot as plt
from CMCed.production_cycle import ProductionCycle
from CMCed.Cognitive_Functions import *

environment_memory = {
    'agent1hand': {'hand': 'open', 'move': 'unknown'},
    'agent2hand': {'hand': 'open', 'move': 'unknown'}
}

referee_working_memory = {
    'focus_buffer': {'state': 'start'},
    'rounds_played': 0,
    'agent1_score': 0,
    'agent2_score': 0,
    'draws': 0,
    'score_difference': 0,
    'game_results': []
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
    'referee_working_memory': referee_working_memory,
    'agent1_working_memory': agent1_working_memory,
    'agent2_working_memory': agent2_working_memory,
    'environment_memory': environment_memory,
    'agent1_declarative_memory': agent1_declarative_memory,
    'agent2_declarative_memory': agent2_declarative_memory,
}

# Procedural Productions
Agent1Productions = []
Agent2Productions = []
RefProductions = []

#######################################################################################################
# Agent1Productions

def recall_agent1_move(memories):
    print('111111111111111111111111111111111111')
    # decay agent1_declarative_memory
    decay_all_memory_chunks(memories, 'agent1_declarative_memory', 1)
    add_noise_to_utility(agent1_declarative_memory, 'agent1 declarative memory', scalar=0.01)

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
    add_noise_to_utility(agent2_declarative_memory, 'agent2 declarative memory', scalar=0.5)

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

#####################################################################################################
# RefProductions

# Evaluation and scoring
def evaluate_results(memories):
    ref_mem = memories['referee_working_memory']
    agent1_choice = memories['environment_memory']['agent1hand']['move']
    agent2_choice = memories['environment_memory']['agent2hand']['move']

    ref_mem['rounds_played'] += 1
    print(f"\nStarting Round {ref_mem['rounds_played']}")

    if agent1_choice == agent2_choice:
        result = "It's a tie!"
        ref_mem['draws'] += 1
    elif (agent1_choice == 'rock' and agent2_choice == 'scissors') or \
            (agent1_choice == 'paper' and agent2_choice == 'rock') or \
            (agent1_choice == 'scissors' and agent2_choice == 'paper'):
        result = "Agent 1 wins!"
        ref_mem['agent1_score'] += 1
    else:
        result = "Agent 2 wins!"
        ref_mem['agent2_score'] += 1
    ref_mem['score_difference'] = ref_mem['agent1_score'] - ref_mem['agent2_score']
    print(f"Referee sees that Agent 1 played {agent1_choice} and Agent 2 played {agent2_choice}. {result}")
    print(f"Current Score - Agent 1: {ref_mem['agent1_score']}, Agent 2: {ref_mem['agent2_score']}, Draws: {ref_mem['draws']}")

    round_data = {
        'Round': ref_mem['rounds_played'],
        'Agent 1 Score': ref_mem['agent1_score'],
        'Agent 2 Score': ref_mem['agent2_score'],
        'Draws': ref_mem['draws'],
        'Score Difference': ref_mem['score_difference'],
        'Result': result
    }
    ref_mem['game_results'].append(round_data)
    #ref_mem['focus_buffer']['state'] = 'end_game'

RefProductions.append({
    'matches': {'environment_memory': {'agent1hand': {'hand': 'open', 'move': '*'}},
                'environment_memory': {'agent2hand': {'hand': 'open', 'move': '*'}}},
    'negations': {},
    'utility': 10,
    'action': evaluate_results,
    'report': "evaluate_results"
})


# Production set up and run
########################################################################

# Production system delays in ticks
Agent1Productions_Countdown = 1
Agent2Productions_Countdown = 1
RefProductions_Countdown = 1
# Stores the number of cycles for a production system to fire and reset

DelayResetValues = {
    'Agent1Productions': Agent1Productions_Countdown,
    'Agent2Productions': Agent2Productions_Countdown,
    'RefProductions': RefProductions_Countdown
}

# Dictionary of all production systems and delays

AllProductionSystems = {
    'Agent1Productions': [Agent1Productions, Agent1Productions_Countdown],
    'Agent2Productions': [Agent2Productions, Agent2Productions_Countdown],
    'RefProductions': [RefProductions, RefProductions_Countdown]
}

# Initialize ProductionCycle

ps = ProductionCycle()

# Run the cycle with custom parameters

ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=30, millisecpercycle=10)


# Save results to Excel
def save_to_excel(ref_mem):
    df = pd.DataFrame(ref_mem['game_results'])
    df.to_excel("game_results_cmc.xlsx", index=False)


# Plot score difference over rounds
def plot_score_difference(ref_mem):
    df = pd.DataFrame(ref_mem['game_results'])
    plt.figure(figsize=(10, 6))
    plt.plot(df['Round'], df['Score Difference'], linestyle='-', color='b', label='Score Difference')
    plt.fill_between(df['Round'], df['Score Difference'], where=(df['Score Difference'] > 0), color='green', alpha=0.3,
                     label="Agent1 Leading")
    plt.fill_between(df['Round'], df['Score Difference'], where=(df['Score Difference'] < 0), color='red', alpha=0.3,
                     label="Agent2 Leading")
    plt.axhline(0, color='black', linewidth=1, linestyle='--')
    plt.title('Score Difference Across Rounds')
    plt.xlabel('Round')
    plt.ylabel('Score Difference')
    plt.legend()
    plt.grid(True)
    plt.savefig('score_difference_graph_cmc.png')
    plt.show()


# Save and plot results
save_to_excel(referee_working_memory)
plot_score_difference(referee_working_memory)

