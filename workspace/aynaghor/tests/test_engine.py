import unittest
import os
import sys

# Add the parent directory to the path so we can import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.engine import Engine

class TestEngine(unittest.TestCase):
    def test_engine_initialization(self):
        # We can at least test that it initializes
        # Even if environment variables are missing, it should handle it
        engine = Engine()
        self.assertIsNotNone(engine)
        self.assertTrue(hasattr(engine, 'use_gemini'))

    def test_health_check(self):
        engine = Engine()
        status = engine.health_check()
        self.assertIn('engine_status', status)
        self.assertEqual(status['engine_status'], 'healthy')

if __name__ == '__main__':
    unittest.main()
