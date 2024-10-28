## functions called from within a production


from CMCed.utility import *


def match_chunks_with_diagnostics(buffer, cue, utility_threshold=0):
# note - if no threshold is set in the production the default is 0
#        because utility cannot go below zero, nothing goes below threshold
    matched_chunks_data = []  # Store matched chunks
    for buffer_key, buffer_value in buffer.items():
        # Perform the matching and capture wildcard values
        match, wildcard_values = Utility.buffer_match_eval_diagnostic(buffer_value, cue['matches'], cue['negations'])
        if match:
            # Copy matching chunk data and include wildcard values
            matched_chunk_data = buffer_value.copy()
            matched_chunk_data.update(wildcard_values)
            matched_chunks_data.append(matched_chunk_data)
            print(f"Appending {buffer_key} to matches with wildcard values: {wildcard_values}")

    # Select the best chunk based on utility
    best_chunk_data = Utility.find_max(matched_chunks_data)

    # Check if the best chunk's utility meets or exceeds the threshold
    if best_chunk_data and best_chunk_data.get('utility', 0) >= utility_threshold:
        return best_chunk_data
    else:
        # Return a generic "failed" chunk if no valid match is found
        print(f"No chunk met the utility threshold of {utility_threshold}.")
        return {'name': 'no_match', 'utility': 0, 'message': 'No matching chunk found'}


def utility_change(memories, memory_store, chunk_name, amount, max_utility=None):
    """
    Adjust the utility of a specific chunk by a given amount. Ensures the utility doesn't go below 0
    and can optionally be capped by a specified max_utility.

    :param memories: Dictionary of memories (including declarative memory)
    :param memory_store: The memory store where the chunk resides (e.g., 'declarative_memory')
    :param chunk_name: The name of the chunk whose utility will be adjusted
    :param amount: The amount to change the utility by (positive or negative)
    :param max_utility: (Optional) The maximum allowable utility value for the chunk
    """
    chunk = memories[memory_store][chunk_name]

    # Adjust the utility
    chunk['utility'] += amount

    # Ensure utility doesn't drop below 0
    if chunk['utility'] < 0:
        chunk['utility'] = 0

    # If a max_utility is specified, ensure utility doesn't exceed it
    if max_utility is not None and chunk['utility'] > max_utility:
        chunk['utility'] = max_utility

    print(f"Updated utility for {chunk_name}: {chunk['utility']}")


def decay_all_memory_chunks(memories, memory_store, decay_amount):
    # Ensure the specified memory store exists in memories
    if memory_store in memories:
        memory = memories[memory_store]

        # Iterate over all chunks in the specified memory store
        for chunk_name, chunk_data in memory.items():
            # Decrement the utility by the decay amount if the 'utility' field exists
            if 'utility' in chunk_data:
                current_utility = chunk_data.get('utility', 0)
                new_utility = max(0, current_utility - decay_amount)  # Ensure utility doesn't go below zero
                memories[memory_store][chunk_name]['utility'] = new_utility
                print(f"Decayed utility of {chunk_name} in {memory_store} to {new_utility}")
            else:
                print(f"Chunk {chunk_name} in {memory_store} has no utility value.")
    else:
        print(f"Memory store {memory_store} not found in memories.")


def adjust_production_utility(production_systems, system_name, production_name, change, max_utility=None):
    """
    Adjusts the utility of a specific production in a production system.

    Args:
        production_systems (dict): Dictionary of production systems.
        system_name (str): The name of the production system containing the production.
        production_name (str): The name of the production to adjust.
        change (int): The amount to adjust the utility by (can be positive or negative).
        max_utility (int, optional): Maximum allowable utility value. If None, no cap is applied.

    Returns:
        None
    """
    if system_name in production_systems:
        for production in production_systems[system_name]:
            if production['name'] == production_name:
                # Adjust the utility
                production['utility'] += change

                # Ensure utility doesn't fall below 0
                if production['utility'] < 0:
                    production['utility'] = 0

                # Apply max utility cap if specified
                if max_utility is not None and production['utility'] > max_utility:
                    production['utility'] = max_utility

                print(f"Updated utility for production '{production_name}': {production['utility']}")
                return
    else:
        print(f"Production system '{system_name}' not found.")


def report_memory_contents(memory, memory_name, cue=None):
    """
    Reports the contents of a selected memory, including utility levels and whether a chunk matched a given cue.

    Args:
        memory (dict): The memory to report on (e.g., declarative or environment memory).
        memory_name (str): The name of the memory (for labeling purposes in the output).
        cue (dict, optional): A cue to check matches against. If provided, will report whether each chunk matches.

    Returns:
        None
    """
    print(f"\n--- Memory Report: {memory_name} ---")

    if cue:
        print(f"Match Criterion: {cue['matches']}, Negations: {cue.get('negations', {})}")

    if not memory:
        print("The memory is empty.")
        return

    for chunk_name, chunk_data in memory.items():
        print(f"Chunk '{chunk_name}':")

        # Check if a chunk matches the cue, if cue is provided
        if cue:
            match, _ = Utility.buffer_match_eval_diagnostic(chunk_data, cue.get('matches', {}),
                                                            cue.get('negations', {}))
            if match:
                print("  Match status: MATCHED")
            else:
                print("  Match status: DID NOT MATCH")

        # Print each key-value pair in the chunk, except utility (handled separately)
        for key, value in chunk_data.items():
            if key != 'utility':
                print(f"  {key}: {value}")

        # Print utility if available
        if 'utility' in chunk_data:
            print(f"  Utility: {chunk_data['utility']}")
        else:
            print("  No utility information.")

def add_noise_to_utility(memory, memory_name, scalar=1.0):
    """
    Adds noise to the utility values of each chunk in a specified memory.
    Noise is drawn from a normal distribution (mean=0, std=1) and scaled by the given scalar.

    Args:
        memory (dict): The memory to add noise to (e.g., declarative or environment memory).
        memory_name (str): The name of the memory (for labeling purposes in the output).
        scalar (float): The factor to scale the noise, default is 1.0.

    Returns:
        None
    """
    print(f"\n--- Adding Noise to {memory_name} ---")

    for chunk_name, chunk_data in memory.items():
        if 'utility' in chunk_data:
            # Generate noise from a normal distribution and scale it
            noise = random.gauss(0, 1) * scalar
            old_utility = chunk_data['utility']
            new_utility = max(0, old_utility + noise)  # Ensure utility doesn't go below 0
            chunk_data['utility'] = new_utility
            print(f"Chunk '{chunk_name}': Old Utility = {old_utility}, Noise = {noise:.2f}, New Utility = {new_utility:.2f}")
        else:
            print(f"Chunk '{chunk_name}' has no utility to add noise to.")

    print(f"--- End of Noise Addition for {memory_name} ---\n")


