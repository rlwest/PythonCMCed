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


# def buffer_match_eval_diagnostic(buffer_value, matches, negations):
#     """
#     Evaluates whether a chunk matches the provided conditions and returns diagnostic information.
#
#     Args:
#         buffer_value (dict): The chunk data to evaluate.
#         matches (dict): Criteria that must be present in the chunk for a match.
#         negations (dict): Criteria that must not be present in the chunk for a match.
#
#     Returns:
#         tuple: (bool, dict) where bool indicates if there is a match, and dict provides any wildcard values.
#     """
#     # Diagnostic: Check match criteria
#     for key, value in matches.items():
#         if buffer_value.get(key) != value:
#             print(
#                 f"[DEBUG] Match failed for chunk on key '{key}' with expected value '{value}', but found '{buffer_value.get(key)}'")
#             return False, {}
#
#     # Diagnostic: Check negation criteria
#     for key, value in negations.items():
#         if buffer_value.get(key) == value:
#             print(f"[DEBUG] Negation matched for chunk on key '{key}' with forbidden value '{value}'")
#             return False, {}
#
#     # If all criteria are met, return match with wildcard values (if applicable)
#     print(f"[DEBUG] Chunk matched with buffer_value: {buffer_value}")
#     return True, {}
#     ###########################################################


# def retrieve_memory_chunk(buffer, matches, negations, utility_threshold=0):
#     matched_chunks_data = []
#
#     for buffer_key, buffer_value in buffer.items():
#         match = True
#
#         # Check for matches
#         for key, value in matches.items():
#             if key not in buffer_value or buffer_value[key] != value:
#                 match = False
#                 break
#
#         # Check for negations, including handling wildcard in negations
#         for key, value in negations.items():
#             if key in buffer_value:
#                 # If wildcard is in negations, any chunk with this slot is negated
#                 if value == '*' or buffer_value[key] == value:
#                     match = False
#                     break
#
#         if match:
#             # Add matched chunk to the list if utility meets or exceeds the threshold
#             if buffer_value.get('utility', 0) >= utility_threshold:
#                 matched_chunks_data.append(buffer_value)
#
#     # If no chunks matched, return a no-match placeholder
#     if not matched_chunks_data:
#         return {"name": "no_match", "utility": 0}
#
#     # Find the maximum utility among matched chunks
#     max_utility = max(chunk.get('utility', 0) for chunk in matched_chunks_data)
#     max_utility_chunks = [chunk for chunk in matched_chunks_data if chunk.get('utility', 0) == max_utility]
#
#     # Randomly select one if multiple chunks have the maximum utility
#     best_chunk_data = random.choice(max_utility_chunks)
#     return best_chunk_data

# def retrieve_memory_chunk(buffer, matches, negations=None, utility_threshold=0):
#     """
#     Retrieves the chunk with the highest utility from the buffer that meets the match conditions
#     and does not violate negation conditions.
#
#     Args:
#         buffer (dict): Memory buffer containing chunks (key-value pairs).
#         matches (dict): Matching criteria; required attributes in each chunk.
#         negations (dict): Negation criteria; disallowed attributes in each chunk.
#         utility_threshold (float, optional): Minimum utility level for chunk consideration. Defaults to 0.
#
#     Returns:
#         dict: The selected chunk based on highest utility or a "no_match" placeholder if none match.
#     """
#     matched_chunks_data = []
#
#     # Loop through each chunk in the buffer
#     for buffer_key, buffer_value in buffer.items():
#         # Check matches
#         if all((buffer_value.get(key) == value or (value == '*' and key in buffer_value)) for key, value in matches.items()):
#             # Check negations, if provided
#             if negations is None or all((buffer_value.get(key) != value) for key, value in negations.items()):
#                 # Add to matched chunks if both match and negation conditions are met
#                 matched_chunks_data.append(buffer_value)
#
#     # If no chunks matched the criteria, return a "no_match" placeholder
#     if not matched_chunks_data:
#         return {"name": "no_match", "utility": 0}
#
#     # Find the maximum utility value among matched chunks
#     max_utility = max(chunk.get('utility', 0) for chunk in matched_chunks_data)
#
#     # Filter matched chunks for those meeting the maximum utility and threshold
#     max_utility_chunks = [chunk for chunk in matched_chunks_data if chunk.get('utility', 0) == max_utility and chunk.get('utility', 0) >= utility_threshold]
#
#     # Return a "no_match" placeholder if no chunks meet the utility threshold
#     if not max_utility_chunks:
#         return {"name": "no_match", "utility": 0}
#
#     # Randomly select a chunk from those with the maximum utility
#     best_chunk_data = random.choice(max_utility_chunks)
#
#     return best_chunk_data

# def retrieve_memory_chunk(buffer, matches, utility_threshold=0):
#     """
#     Retrieves the chunk with the highest utility from a memory buffer, based on exact matching criteria
#     and mandatory slot presence indicated by wildcards.
#
#     Args:
#         buffer (dict): Memory store with chunks, each as a dictionary of attributes.
#         matches (dict): Key-value pairs that must be present in a chunk for a match.
#                         Use '*' to indicate the slot must exist but can hold any value.
#         utility_threshold (float, optional): Minimum utility level for consideration. Default is 0.
#
#     Returns:
#         dict: The chunk with the highest utility that meets criteria or a placeholder if no match.
#     """
#     matched_chunks = []
#
#     for buffer_key, chunk in buffer.items():
#         # Check if all required matches are present in this chunk
#         match_found = True
#         for key, value in matches.items():
#             # If the value is '*', only check if the key exists in the chunk
#             if value == '*':
#                 if key not in chunk:
#                     match_found = False
#                     print(f"Chunk '{buffer_key}' missing required slot '{key}' for wildcard match.")
#                     break
#             # Otherwise, check for an exact match
#             elif chunk.get(key) != value:
#                 match_found = False
#                 print(f"Chunk '{buffer_key}' failed exact match for '{key}': expected '{value}', found '{chunk.get(key)}'.")
#                 break
#
#         # If all conditions match and utility is above the threshold, add to matched_chunks
#         if match_found and chunk.get('utility', 0) >= utility_threshold:
#             matched_chunks.append(chunk)
#         elif match_found:
#             print(f"Chunk '{buffer_key}' below utility threshold.")
#
#     # Return no-match if nothing met criteria
#     if not matched_chunks:
#         print("No chunks matched the criteria.")
#         return {"name": "no_match", "utility": 0}
#
#     # Select highest utility chunk or random among ties
#     max_utility = max(chunk['utility'] for chunk in matched_chunks)
#     highest_utility_chunks = [chunk for chunk in matched_chunks if chunk['utility'] == max_utility]
#     return random.choice(highest_utility_chunks)

### for matching
# def match_chunks_with_diagnostics(buffer, cue, utility_threshold=0):
#     """
#     Finds and returns the chunk with the highest utility from a buffer, based on matching criteria.
#
#     This function iterates over each chunk in the provided buffer, checks if it meets the conditions
#     specified in the cue, and collects all matching chunks. Then, it selects the chunk with the
#     highest utility that exceeds a given threshold, or returns a placeholder if no matches are found.
#
#     Args:
#         buffer (dict): The memory store containing chunks, where each key is a chunk identifier,
#                        and each value is a dictionary representing the chunk's attributes.
#         cue (dict): Contains 'matches' and 'negations' criteria for chunk matching.
#                     - 'matches': Specifies key-value pairs that must be present in a chunk for it to match.
#                     - 'negations': Specifies key-value pairs that must not be present in a chunk for it to match.
#         utility_threshold (float, optional): Minimum utility level required for a chunk to be considered.
#                                              Defaults to 0.
#
#     Returns:
#         dict: The chunk with the highest utility that meets the match criteria and exceeds the threshold.
#               If no chunk meets the criteria, returns a placeholder dictionary.
#     """
#
#     # Initialize an empty list to store data of chunks that match the criteria.
#     matched_chunks_data = []
#
#     # Loop through each chunk in the buffer
#     for buffer_key, buffer_value in buffer.items():
#         # Evaluate if the chunk matches the given 'matches' and 'negations' criteria in the cue.
#         # Also retrieves any wildcard values for unspecified matching.
#         match, wildcard_values = Utility.buffer_match_eval_diagnostic(
#             buffer_value, cue['matches'], cue['negations']
#         )
#
#         # If the chunk matches the criteria, it proceeds to add it to matched_chunks_data.
#         if match:
#             # Copy the data of the matched chunk to avoid altering the original data in the buffer.
#             matched_chunk_data = buffer_value.copy()
#
#             # Update the copied chunk data with any wildcard values (if any were found).
#             matched_chunk_data.update(wildcard_values)
#
#             # Append the modified chunk data to matched_chunks_data for later processing.
#             matched_chunks_data.append(matched_chunk_data)
#
#             # Log debug info to show which chunks matched and their wildcard values.
#             print(f"Appending {buffer_key} to matches with wildcard values: {wildcard_values}")
#
#     # If no chunks matched the criteria, return a placeholder dictionary to indicate no match.
#     if not matched_chunks_data:
#         print("No chunks matched the criteria.")
#         return {"name": "no_match", "utility": 0}
#
#     # Find the maximum utility value among the matched chunks.
#     # This will help us filter for the highest-utility chunks.
#     max_utility = max(chunk.get('utility', 0) for chunk in matched_chunks_data)
#     print(f"Max utility found: {max_utility}")
#
#     # Filter the matched chunks to include only those with utility equal to the maximum.
#     # This ensures we’re working with the most relevant chunks based on utility.
#     max_utility_chunks = [
#         chunk for chunk in matched_chunks_data
#         if chunk.get('utility', 0) == max_utility and chunk.get('utility', 0) >= utility_threshold
#     ]
#     print(f"Chunks with max utility: {max_utility_chunks}")
#
#     # If no chunks meet the utility threshold, return a placeholder dictionary.
#     if not max_utility_chunks:
#         print("No chunks meet the utility threshold.")
#         return {"name": "no_match", "utility": 0}
#
#     # Randomly select one chunk from those with the maximum utility.
#     # This adds randomness in case there are multiple chunks with the same high utility.
#     best_chunk_data = random.choice(max_utility_chunks)
#     print(f"Randomly selected chunk: {best_chunk_data}")
#
#     # Return the selected chunk as the best match based on utility and the matching criteria.
#     return best_chunk_data

# def match_chunks_with_diagnostics(buffer, cue, utility_threshold=0):
# # note - if no threshold is set in the production the default is 0
# #        because utility cannot go below zero, nothing goes below threshold
#     matched_chunks_data = []  # Store matched chunks
#     for buffer_key, buffer_value in buffer.items():
#         # Perform the matching and capture wildcard values
#         match, wildcard_values = Utility.buffer_match_eval_diagnostic(buffer_value, cue['matches'], cue['negations'])
#         if match:
#             # Copy matching chunk data and include wildcard values
#             matched_chunk_data = buffer_value.copy()
#             matched_chunk_data.update(wildcard_values)
#             matched_chunks_data.append(matched_chunk_data)
#             print(f"Appending {buffer_key} to matches with wildcard values: {wildcard_values}")
#
#     # Select the best chunk based on utility
#     best_chunk_data = Utility.find_max(matched_chunks_data)
#
#     # Check if the best chunk's utility meets or exceeds the threshold
#     if best_chunk_data and best_chunk_data.get('utility', 0) >= utility_threshold:
#         return best_chunk_data
#     else:
#         # Return a generic "failed" chunk if no valid match is found
#         print(f"No chunk met the utility threshold of {utility_threshold}.")
#         return {'name': 'no_match', 'utility': 0, 'message': 'No matching chunk found'}

# def report_memory_contents(memory, memory_name, matches=None, negations=None):
#     """
#     Reports the contents of a selected memory, including utility levels and whether a chunk matched given criteria.
#
#     Args:
#         memory (dict): The memory to report on (e.g., declarative or environment memory).
#         memory_name (str): The name of the memory (for labeling purposes in the output).
#         matches (dict, optional): Criteria for matching. The chunk must contain these key-value pairs to match.
#         negations (dict, optional): Criteria for negations. If a chunk contains these key-value pairs, it will not match.
#
#     Returns:
#         None
#     """
#     print(f"\n--- Memory Report: {memory_name} ---")
#
#     if matches:
#         print(f"Match Criteria: {matches}")
#     if negations:
#         print(f"Negation Criteria: {negations}")
#
#     if not memory:
#         print("The memory is empty.")
#         return
#
#     for chunk_name, chunk_data in memory.items():
#         print(f"Chunk '{chunk_name}':")
#
#         # Check if the chunk matches the criteria
#         match = True
#         if matches:
#             for key, value in matches.items():
#                 if key not in chunk_data or (value != '*' and chunk_data[key] != value):
#                     match = False
#                     break
#         if match and negations:
#             for neg_key, neg_value in negations.items():
#                 if neg_key in chunk_data and (neg_value == '*' or chunk_data[neg_key] == neg_value):
#                     match = False
#                     break
#
#         # Print match status
#         print("  Match status:", "MATCHED" if match else "DID NOT MATCH")
#
#         # Print each key-value pair in the chunk, except utility (handled separately)
#         for key, value in chunk_data.items():
#             if key != 'utility':
#                 print(f"  {key}: {value}")
#
#         # Print utility if available
#         if 'utility' in chunk_data:
#             print(f"  Utility: {chunk_data['utility']}")
#         else:
#             print("  No utility information.")
#
#     print(f"--- End of {memory_name} Report ---\n")
