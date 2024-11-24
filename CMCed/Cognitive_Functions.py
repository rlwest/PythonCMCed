## functions called from within a production


from CMCed.utility import *

import random

def retrieve_memory_chunk(buffer, matches, negations={}, utility_threshold=0):
    """
    Retrieve the highest utility chunk that meets match criteria and negation constraints.

    Args:
        buffer (dict): Memory buffer containing chunks.
        matches (dict): Key-value pairs to match in each chunk. '*' indicates any value is acceptable if the slot exists.
        negations (dict): Key-value pairs to avoid in each chunk. '*' indicates any value in the slot will negate the match.
        utility_threshold (int, optional): Minimum utility required to consider a chunk.

    Returns:
        dict: The chunk with the highest utility or a placeholder if no matches.
    """
    matched_chunks = []

    # Iterate through each chunk in the buffer to check for matches
    for chunk in buffer.values():
        match = True

        # Check positive matches
        for key, value in matches.items():
            if key not in chunk:  # Slot must exist for wildcard match
                match = False
                break
            elif value != '*' and chunk[key] != value:  # Specific value required, no wildcard
                match = False
                break

        # Check negations
        for key, value in negations.items():
            if key in chunk:  # Slot must exist for wildcard negation
                if value == '*' or chunk[key] == value:  # Any value in this slot negates the match
                    match = False
                    break

        # Add chunk if it matches and meets the utility threshold
        if match and chunk.get('utility', 0) >= utility_threshold:
            matched_chunks.append(chunk)

    # Return placeholder if no chunks matched
    if not matched_chunks:
        return {"name": "no_match", "utility": 0}

    # Find the highest-utility chunk among matches
    max_utility = max(chunk.get('utility', 0) for chunk in matched_chunks)
    best_chunks = [chunk for chunk in matched_chunks if chunk.get('utility', 0) == max_utility]

    # Randomly select one chunk if multiple have the same max utility
    return random.choice(best_chunks)

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

def utility_change_by_description(memories, memory_store, chunk_description, amount, max_utility=None):
    """
    Adjust the utility of a specific chunk by finding a match based on its description. Ensures the utility
    doesn't go below 0 and can optionally be capped by a specified max_utility. If multiple chunks match
    the description, an error message is printed.

    :param memories: Dictionary of memories (including declarative memory)
    :param memory_store: The memory store where the chunks reside (e.g., 'declarative_memory')
    :param chunk_description: A dictionary describing the chunk to find
    :param amount: The amount to change the utility by (positive or negative)
    :param max_utility: (Optional) The maximum allowable utility value for the chunk
    """
    matches = []  # Keep track of matching chunks

    # Find all matching chunks
    for chunk_name, chunk_data in memories[memory_store].items():
        if all(chunk_data.get(key) == value for key, value in chunk_description.items()):
            matches.append((chunk_name, chunk_data))

    # Check for duplicates
    if len(matches) > 1:
        print("Error: Multiple chunks match the given BOOST description. No changes were applied.")
        for chunk_name, _ in matches:
            print(f"Matching chunk: {chunk_name}")
        return

    if not matches:
        print("No matching chunk found for utility boost.")
        return

    # Update the utility of the single matching chunk
    chunk_name, chunk_data = matches[0]
    chunk_data['utility'] += amount

    # Ensure utility doesn't drop below 0
    if chunk_data['utility'] < 0:
        chunk_data['utility'] = 0

    # If a max_utility is specified, ensure utility doesn't exceed it
    if max_utility is not None and chunk_data['utility'] > max_utility:
        chunk_data['utility'] = max_utility

    print(f"Updated utility for {chunk_name}: {chunk_data['utility']}")

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

def report_memory_contents(memory, matches=None, negations=None):
    """
    Reports the contents of a selected memory, including utility levels and whether a chunk matched given criteria.
    if matches and negations are not specified it defaults to None and everything is a match

    Args:
        memory (dict): The memory to report on (e.g., declarative or environment memory).
        matches (dict, optional): Criteria for matching. The chunk must contain these key-value pairs to match.
        negations (dict, optional): Criteria for negations. If a chunk contains these key-value pairs, it will not match.

    Returns:
        None
    """
    print("\n--- Memory Report ---")

    if matches:
        print(f"Match Criteria: {matches}")
    if negations:
        print(f"Negation Criteria: {negations}")

    if not memory:
        print("The memory is empty.")
        return

    for chunk_name, chunk_data in memory.items():
        print(f"Chunk '{chunk_name}':")

        # Check if the chunk matches the criteria
        match = True
        if matches:
            for key, value in matches.items():
                if key not in chunk_data or (value != '*' and chunk_data[key] != value):
                    match = False
                    break
        if match and negations:
            for neg_key, neg_value in negations.items():
                if neg_key in chunk_data and (neg_value == '*' or chunk_data[neg_key] == neg_value):
                    match = False
                    break

        # Print match status
        print("  Match status:", "MATCHED" if match else "DID NOT MATCH")

        # Print each key-value pair in the chunk, except utility (handled separately)
        for key, value in chunk_data.items():
            if key != 'utility':
                print(f"  {key}: {value}")

        # Print utility if available
        if 'utility' in chunk_data:
            print(f"  Utility: {chunk_data['utility']}")
        else:
            print("  No utility information.")

    print("--- End of Memory Report ---\n")


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

    # for debugging ############################


def spreading_activation_boost(memories, memory_store, source_chunk, boost_factor=1):
    """
    Boost the utility of chunks in memory based on partial matching with a source chunk.
    The matching score is determined by counting shared values between the source chunk and each chunk in memory.

    Args:
        memories (dict): The memory system containing the memory store.
        memory_store (str): The name of the memory store to search (e.g., 'declarative_memory').
        source_chunk (dict): The source chunk for spreading activation.
        boost_factor (float): The multiplier applied to the matching score for utility boost.

    Returns:
        None
    """
    if memory_store not in memories:
        print(f"[ERROR] Memory store '{memory_store}' not found in memories.")
        return

    memory = memories[memory_store]
    source_values = set(source_chunk.values())  # Extract values from the source chunk

    print(f"[DEBUG] Source chunk values for spreading activation: {source_values}")

    for chunk_name, chunk_data in memory.items():
        chunk_values = set(chunk_data.values())  # Extract values from the target chunk
        match_score = len(source_values & chunk_values)  # Count intersecting values
        utility_boost = match_score * boost_factor

        # Apply the utility boost
        chunk_data['utility'] += utility_boost

        print(f"[DEBUG] Chunk '{chunk_name}': Match score = {match_score}, Utility boost = {utility_boost}")
        print(f"[DEBUG] Updated utility for chunk '{chunk_name}': {chunk_data['utility']}")