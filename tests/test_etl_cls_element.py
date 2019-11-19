import unittest
import collections
import tempfile
import io
import os
import etl

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestElement(unittest.TestCase):
    """Testing all methods of the Element class"""

    def setUp(self):
        self.file_name_csv = os.path.join(THIS_DIR, 'examples_cls_elem/test_csv_data.csv')
        self.file_name_csv_empty = os.path.join(THIS_DIR, 'examples_cls_elem/test_csv_data_empty.csv')
        self.file_name_json = os.path.join(THIS_DIR, 'examples_cls_elem/test_json_data.json')
        self.file_name_json_empty = os.path.join(THIS_DIR, 'examples_cls_elem/test_json_data_empty.json')
        self.file_name_xml = os.path.join(THIS_DIR, 'examples_cls_elem/test_xml_data.xml')
        self.file_name_xml_empty = os.path.join(THIS_DIR, 'examples_cls_elem/test_xml_data_empty.xml')
        self.expected_test_write_tsv = os.path.join(THIS_DIR, 'examples_cls_elem/expected_test_write_tsv.tsv')

    def test_read_csv(self):
        """
        Testing read_csv using a CSV file
        to make sure it is being processed correctly
        """
        self.element = etl.Element(self.file_name_csv)
        self.element.read_csv()
        given_list = self.element.list_of_dicts
        expected_list = [collections.OrderedDict([('D1', 'a'), ('D2', 'b'), ('M1', '1'), ('M2', '1')]),
                         collections.OrderedDict([('D1', 'b'), ('D2', 'a'), ('M1', '0'), ('M2', '0')])]
        self.assertEqual(given_list, expected_list)

    def test_read_csv_empty(self):
        """
        Testing read_csv using an empty CSV file
        to make sure it is being processed correctly
        """
        self.element = etl.Element(self.file_name_csv_empty)
        self.element.read_csv()
        given_list = self.element.list_of_dicts
        self.assertEqual(given_list, list())

    def test_read_json(self):
        """
        Testing read_json using a JSON file
        to make sure it is being processed correctly
        """
        self.element = etl.Element(self.file_name_json)
        self.element.read_json()
        given_list = self.element.list_of_dicts
        expected_list = [{'D1': 'a', 'D2': 'a', 'M1': 0, 'M2': 0},
                         {'D1': 'b', 'D2': 'b', 'M1': 1, 'M2': 1}]
        self.assertEqual(given_list, expected_list)

    def test_read_json_empty(self):
        """
        Testing read_json using an empty JSON file
        to make sure it is being processed correctly
        """
        self.element = etl.Element(self.file_name_json_empty)
        self.element.read_json()
        given_list = self.element.list_of_dicts
        self.assertEqual(given_list, list())

    def test_read_xml(self):
        """
        Testing read_xml using a XML file
        to make sure it is being processed correctly
        """
        self.element = etl.Element(self.file_name_xml)
        self.element.read_xml()
        given_list = self.element.list_of_dicts
        expected_list = [{'D1': 'a', 'D2': 'a', 'M1': '0', 'M2': '0'},
                         {'D1': 'b', 'D2': 'b', 'M1': '2', 'M2': '2'}]
        self.assertEqual(given_list, expected_list)

    def test_read_xml_empty(self):
        """
        Testing read_xml using an empty XML file
        to make sure it is being processed correctly
        """
        self.element = etl.Element(self.file_name_xml_empty)
        self.element.read_xml()
        given_list = self.element.list_of_dicts
        self.assertEqual(given_list, list())

    def test_keys_of_dicts(self):
        """
        Testing keys_of_dicts to verify that keys
        are extracted from a list of dictionaries
        """
        self.element = etl.Element(self.file_name_csv)
        self.element.read_csv()
        given_list_of_keys = list(self.element.keys_of_dicts())
        expected_list_of_keys = ['D1', 'D2', 'M1', 'M2']
        self.assertEqual(given_list_of_keys, expected_list_of_keys)

    def test_keys_of_dicts_empty(self):
        """
        Testing keys_of_dicts to verify that keys
        are extracted from an empty a list of dictionaries
        """
        self.element = etl.Element(self.file_name_csv_empty)
        self.element.read_csv()
        given_list_of_keys = list(self.element.keys_of_dicts())
        self.assertEqual(given_list_of_keys, list())

    def test_write_tsv(self):
        """
        Testing write_tsv for the correctness
        of writing a list of dictionaries to a file
        """
        with tempfile.TemporaryDirectory() as tempdir:
            path = os.path.join(tempdir, 'given_test_write_tsv.tsv')
            etl.Element.write_tsv([{'D1': 'a', 'M1': 0}, {'D1': 'b', 'M1': 1}], path)
            with io.open(path) as given_file, io.open(self.expected_test_write_tsv) as expected_file:
                self.assertListEqual(list(given_file), list(expected_file))


if __name__ == '__main__':
    unittest.main()
