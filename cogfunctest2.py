import unittest
from CMCed.Cognitive_Functions import buffer_match_eval_diagnostic

class TestCogFunc(unittest.TestCase):

    def test_buffer_match_eval_diagnostic(self):
        # Define a buffer entry that we want to evaluate
        buffer_entry = {
            'type': 'task',
            'status': 'incomplete',
            'priority': 'high',
            'utility': 7
        }

        # Define a cue with matches and negations for testing
        cue = {
            'matches': {'type': 'task', 'priority': 'high'},
            'negations': {'status': 'complete'}
        }

        # Call buffer_match_eval_diagnostic
        match, wildcard_values = buffer_match_eval_diagnostic(buffer_entry, cue['matches'], cue['negations'])

        # Expected results
        self.assertTrue(match, "Expected the buffer to match the cue conditions.")
        self.assertEqual(wildcard_values, {}, "Expected no wildcards for exact matches.")

        # Test with non-matching conditions
        cue_non_match = {
            'matches': {'type': 'event'},  # Different type
            'negations': {'status': 'incomplete'}
        }
        match_non, wildcard_values_non = buffer_match_eval_diagnostic(buffer_entry, cue_non_match['matches'], cue_non_match['negations'])

        # Expected non-match results
        self.assertFalse(match_non, "Expected the buffer to NOT match the non-matching cue conditions.")
        self.assertEqual(wildcard_values_non, {}, "Expected no wildcards for non-matching.")

if __name__ == '__main__':
    unittest.main()