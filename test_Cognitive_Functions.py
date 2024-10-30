import unittest
from CMCed.Cognitive_Functions import buffer_match_eval_diagnostic, match_chunks_with_diagnostics

class TestCogFunc(unittest.TestCase):

    def test_buffer_match_eval_diagnostic_variations(self):
        print("\nRunning variations for buffer_match_eval_diagnostic...")

        # Exact match test
        buffer_entry = {'type': 'task', 'status': 'complete', 'priority': 'high', 'utility': 7}
        cue_exact = {'matches': {'type': 'task', 'priority': 'high'}, 'negations': {'status': 'incomplete'}}
        match, _ = buffer_match_eval_diagnostic(buffer_entry, cue_exact['matches'], cue_exact['negations'])
        print(f"Exact match expected: True, got: {match}")
        self.assertTrue(match)

        # Wildcard match test
        cue_wildcard = {'matches': {'type': 'task', 'priority': '*'}, 'negations': {'status': 'incomplete'}}
        match, _ = buffer_match_eval_diagnostic(buffer_entry, cue_wildcard['matches'], cue_wildcard['negations'])
        print(f"Wildcard match expected: True, got: {match}")
        self.assertTrue(match)

    def test_match_chunks_with_diagnostics_variations(self):
        print("\nRunning variations for match_chunks_with_diagnostics...")

        # Buffer with chunks
        buffer = {
            'chunk1': {'type': 'task', 'status': 'complete', 'utility': 5},
            'chunk2': {'type': 'task', 'status': 'incomplete', 'utility': 8},
            'chunk3': {'type': 'event', 'status': 'upcoming', 'utility': 3},
            'chunk4': {'type': 'task', 'status': 'incomplete', 'utility': 8}
        }

        # Threshold test: retrieve only if above threshold
        cue_threshold = {'matches': {'type': 'task'}, 'negations': {'status': 'complete'}}
        best_chunk = match_chunks_with_diagnostics(buffer, cue_threshold, utility_threshold=6)
        print(f"Threshold test expected: chunk2 or chunk4, got: {best_chunk}")
        self.assertIn(best_chunk, [
            {'type': 'task', 'status': 'incomplete', 'utility': 8}
        ])

        # Test for multiple matches with the same utility
        best_chunk_multiple = match_chunks_with_diagnostics(buffer, cue_threshold, utility_threshold=6)
        print(f"Multiple matches with same utility - Random choice test result: {best_chunk_multiple}")
        self.assertIn(best_chunk_multiple, [
            {'type': 'task', 'status': 'incomplete', 'utility': 8}
        ])

        # Test for no matches found, expecting 'no_match' placeholder
        cue_no_match = {'matches': {'type': 'task'}, 'negations': {'status': 'incomplete'}}
        best_chunk_no_match = match_chunks_with_diagnostics(buffer, cue_no_match, utility_threshold=2)
        expected_no_match_chunk = {'name': 'no_match', 'utility': 0}
        print(f"Non-matching cue expected: {expected_no_match_chunk}, got: {best_chunk_no_match}")
        self.assertEqual(best_chunk_no_match, expected_no_match_chunk)


if __name__ == '__main__':
    unittest.main()


# import unittest
# from CMCed.utility import Utility
# from CMCed.Cognitive_Functions import match_chunks_with_diagnostics, buffer_match_eval_diagnostic
#
# class TestCogFunc(unittest.TestCase):
#
#     def test_buffer_match_eval_diagnostic_variations(self):
#         print("\nRunning variations for buffer_match_eval_diagnostic...")
#
#         # Exact match
#         buffer_entry = {'type': 'task', 'status': 'complete', 'priority': 'high', 'utility': 7}
#         cue_exact = {'matches': {'type': 'task', 'status': 'complete'}}
#         match, _ = buffer_match_eval_diagnostic(buffer_entry, cue_exact['matches'], {})
#         print(f"Exact match expected: True, got: {match}")
#         self.assertTrue(match)
#
#         # Partial match with wildcard
#         cue_wildcard = {'matches': {'type': 'task', 'priority': '*'}}
#         match, _ = buffer_match_eval_diagnostic(buffer_entry, cue_wildcard['matches'], {})
#         print(f"Wildcard match expected: True, got: {match}")
#         self.assertTrue(match)
#
#         # Negation disqualifies match
#         cue_negation = {'matches': {'type': 'task'}, 'negations': {'status': 'complete'}}
#         match, _ = buffer_match_eval_diagnostic(buffer_entry, cue_negation['matches'], cue_negation['negations'])
#         print(f"Negation disqualifies match expected: False, got: {match}")
#         self.assertFalse(match)
#
#     def test_match_chunks_with_diagnostics_variations(self):
#         print("\nRunning variations for match_chunks_with_diagnostics...")
#
#         buffer = {
#             'chunk1': {'type': 'task', 'status': 'complete', 'utility': 5},
#             'chunk2': {'type': 'task', 'status': 'incomplete', 'utility': 8},
#             'chunk3': {'type': 'task', 'status': 'incomplete', 'utility': 5}
#         }
#
#         # Threshold test
#         cue_threshold = {'matches': {'type': 'task'}, 'negations': {}}
#         best_chunk = match_chunks_with_diagnostics(buffer, cue_threshold, utility_threshold=6)
#         print(f"Threshold test expected: chunk2, got: {best_chunk}")
#         self.assertEqual(best_chunk, {'type': 'task', 'status': 'incomplete', 'utility': 8})
#
#         # Multiple matches with same utility
#         buffer['chunk4'] = {'type': 'task', 'status': 'incomplete', 'utility': 8}
#         best_chunk = match_chunks_with_diagnostics(buffer, cue_threshold)
#         print(f"Multiple matches with same utility - Random choice test result: {best_chunk}")
#         self.assertIn(best_chunk, [{'type': 'task', 'status': 'incomplete', 'utility': 8}])
#
#         # Non-matching cue
#         cue_non_match = {'matches': {'type': 'event'}, 'negations': {}}
#         best_chunk = match_chunks_with_diagnostics(buffer, cue_non_match)
#         print(f"Non-matching cue expected: None, got: {best_chunk}")
#         self.assertIsNone(best_chunk)
#
# if __name__ == '__main__':
#     unittest.main()


# import unittest
# from CMCed.utility import Utility
# from CMCed.Cognitive_Functions import match_chunks_with_diagnostics, buffer_match_eval_diagnostic
#
#
# class TestCogFunc(unittest.TestCase):
#
#     def test_buffer_match_eval_diagnostic(self):
#         print("\nRunning test for buffer_match_eval_diagnostic...")
#
#         # Define a buffer entry that we want to evaluate
#         buffer_entry = {
#             'type': 'task',
#             'status': 'incomplete',
#             'priority': 'high',
#             'utility': 7
#         }
#
#         # Define a cue with matches and negations for testing
#         cue = {
#             'matches': {'type': 'task', 'priority': 'high'},
#             'negations': {'status': 'complete'}
#         }
#
#         # Call buffer_match_eval_diagnostic with matching conditions
#         print("Testing with matching conditions in cue...")
#         match, wildcard_values = buffer_match_eval_diagnostic(buffer_entry, cue['matches'], cue['negations'])
#
#         # Expected results for match
#         print(f"Expected match: True, Actual match: {match}")
#         self.assertTrue(match, "Expected the buffer to match the cue conditions.")
#         print(f"Expected wildcards: {{}}, Actual wildcards: {wildcard_values}")
#         self.assertEqual(wildcard_values, {}, "Expected no wildcards for exact matches.")
#
#         # Test with non-matching conditions
#         cue_non_match = {
#             'matches': {'type': 'event'},  # Different type
#             'negations': {'status': 'incomplete'}
#         }
#         print("Testing with non-matching conditions in cue...")
#         match_non, wildcard_values_non = buffer_match_eval_diagnostic(buffer_entry, cue_non_match['matches'],
#                                                                       cue_non_match['negations'])
#
#         # Expected non-match results
#         print(f"Expected match: False, Actual match: {match_non}")
#         self.assertFalse(match_non, "Expected the buffer to NOT match the non-matching cue conditions.")
#         print(f"Expected wildcards: {{}}, Actual wildcards: {wildcard_values_non}")
#         self.assertEqual(wildcard_values_non, {}, "Expected no wildcards for non-matching.")
#
#     def test_match_chunks_with_diagnostics(self):
#         print("\nRunning test for match_chunks_with_diagnostics...")
#
#         # Define a buffer with multiple items, each with different attributes and utilities
#         buffer = {
#             'chunk1': {'type': 'task', 'status': 'complete', 'utility': 5},
#             'chunk2': {'type': 'task', 'status': 'incomplete', 'utility': 8},
#             'chunk3': {'type': 'event', 'status': 'upcoming', 'utility': 3}
#         }
#
#         # Define cues for matching and negation
#         cue = {
#             'matches': {'type': 'task'},
#             'negations': {'status': 'complete'}
#         }
#
#         # Call match_chunks_with_diagnostics with buffer and cue
#         print("Testing match_chunks_with_diagnostics with matching criteria and negations...")
#         best_chunk = match_chunks_with_diagnostics(buffer, cue)
#
#         # Output the matched chunk details
#         print("Expected result: chunk2 with highest utility among matching items.")
#         expected_chunk = {'type': 'task', 'status': 'incomplete', 'utility': 8}
#
#         # Check that the retrieved chunk matches our expectation
#         print(f"Best chunk retrieved: {best_chunk}")
#         self.assertEqual(best_chunk, expected_chunk, "Expected 'chunk2' with highest utility and matching conditions.")
#
#
# if __name__ == '__main__':
#     unittest.main()
#
