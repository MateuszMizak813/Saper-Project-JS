""" Plik z testami jednostkowymi """

import unittest
import functionality


class TestSaperGame(unittest.TestCase):
    def test_submitting_data(self):
        self.assertRaises(functionality.ArgumentNotInRange, functionality.check_settings, '1', '1', '1')
        self.assertRaises(functionality.ArgumentNotInRange, functionality.check_settings, '5', '1', '2')
        self.assertRaises(functionality.ArgumentNotInRange, functionality.check_settings, '4', '1', '2')
        self.assertRaises(functionality.ArgumentNotInRange, functionality.check_settings, '20', '500', '12')
        self.assertRaises(functionality.WrongTypeOfArguments, functionality.check_settings, '5', '6', '-4')
        self.assertRaises(functionality.ArgumentNotInRange, functionality.check_settings, '3', '3', '10')
        self.assertRaises(functionality.ArgumentNotInRange, functionality.check_settings, '1', '10', '5')


if __name__ == '__main__':
    unittest.main()
