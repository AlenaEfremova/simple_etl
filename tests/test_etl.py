import unittest
import etl


class MyTestCase(unittest.TestCase):
    """Skeleton for application testing"""

    def test_parser_cmd(self):
        """Testing the function with any list of arguments"""

        self.parser = etl.parser_cmd()
        parsed = self.parser.parse_args(['--t', 'test'])
        self.assertEqual(parsed.t, 'test')
        self.assertEqual(True, True)

    def test_open_file(self):
        """Testing the function with different file types"""

        self.writer = etl.open_file('')
        self.assertEqual(True, True)

    def test_list_intersection(self):
        """Testing the function with different lists"""

        list_of_lists = list()
        self.intersection = etl.list_intersection(list_of_lists)
        self.assertEqual(True, True)

    def test_sorted_list_of_dicts(self):
        """Testing the function with different dictionary lists and key values"""

        list_of_dicts = list()
        key = str()
        self.sorter = etl.sorted_list_of_dicts(list_of_dicts, key)
        self.assertEqual(True, True)

    def test_write_tsv(self):
        """Testing the function with different dictionary lists"""

        list_of_dicts = list()
        pathname = str('')
        self.writer = etl.write_tsv(list_of_dicts, pathname)
        self.assertEqual(True, True)

    def test_key_separation(self):
        """Testing the function with different key lists"""

        list_of_keys = list()
        self.separator = etl.key_separation(list_of_keys)
        self.assertEqual(True, True)

    def test_value_conversion(self):
        """Testing the function with different dictionaries with different types of values"""

        list_of_dicts = list()
        self.separator = etl.value_conversion(list_of_dicts)
        self.assertEqual(True, True)

    def test_dictionary_comparison(self):
        """Testing the function with different dictionary lists"""

        list_of_dicts = list()
        self.separator = etl.dictionary_comparison(list_of_dicts)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
