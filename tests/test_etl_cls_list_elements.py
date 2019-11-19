import unittest
import collections
import os
import etl

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestListElements(unittest.TestCase):
    """Testing all methods of the ListElements class"""

    def setUp(self):
        self.file_name_csv = os.path.join(THIS_DIR, 'examples_cls_lst_elem/test_csv_data.csv')
        self.file_name_json = os.path.join(THIS_DIR, 'examples_cls_lst_elem/test_json_data.json')
        self.file_name_xml = os.path.join(THIS_DIR, 'examples_cls_lst_elem/test_xml_data.xml')
        self.file_name_tsv = os.path.join(THIS_DIR, 'examples_cls_lst_elem/test_tsv_data.tsv')
        self.file_name_csv_except = os.path.join(THIS_DIR, 'examples_cls_lst_elem/test_csv_data_except.csv')
        self.file_name_json_except = os.path.join(THIS_DIR, 'examples_cls_lst_elem/test_json_data_except.json')
        self.file_names = [self.file_name_csv, self.file_name_json, self.file_name_xml]

    def test_process_elements(self):
        """
        Testing process_elements using a list of file names
        to make sure it is being processed correctly
        """
        list_elements = etl.ListElements(self.file_names)
        list_elements.process_elements()
        given_list_csv = list_elements.elements[0].list_of_dicts
        expected_list_csv = [collections.OrderedDict([('D1', 'a'), ('D2', 'b'), ('M1', '1'), ('M2', '1')]),
                             collections.OrderedDict([('D1', 'b'), ('D2', 'a'), ('M1', '0'), ('M2', '0')])]
        given_list_json = list_elements.elements[1].list_of_dicts
        expected_list_json = [{'D1': 'a', 'D2': 'a', 'M1': 2},
                              {'D1': 'b', 'D2': 'b', 'M1': 1}]
        given_list_xml = list_elements.elements[2].list_of_dicts
        expected_list_xml = [{'D1': 'a', 'D2': 'a', 'M1': '1', 'M2': '1'}]
        self.assertEqual(given_list_csv, expected_list_csv)
        self.assertEqual(given_list_json, expected_list_json)
        self.assertEqual(given_list_xml, expected_list_xml)

        file_names_with_tsv = [self.file_name_csv, self.file_name_tsv]
        list_elements_with_tsv = etl.ListElements(file_names_with_tsv)
        self.assertRaises(NameError, lambda: list_elements_with_tsv.process_elements())

    def test_list_intersection(self):
        """
        Testing list_intersection to make sure
        that these files intersect correctly
        """
        list_elements = etl.ListElements(self.file_names)
        list_elements.process_elements()
        given_list_intersection = list_elements.list_intersection()
        expected_list_intersection = [{'D1': 'a', 'D2': 'b', 'M1': '1'},
                                      {'D1': 'b', 'D2': 'a', 'M1': '0'},
                                      {'D1': 'a', 'D2': 'a', 'M1': 2},
                                      {'D1': 'b', 'D2': 'b', 'M1': 1},
                                      {'D1': 'a', 'D2': 'a', 'M1': '1'}]
        self.assertEqual(given_list_intersection, expected_list_intersection)

    def test_sorted_list_of_dicts(self):
        """
        Testing sorted_list_of_dicts to check the sorting of the dictionary list by the specified key.
        In cases when the key is not specified or the specified key is not in the dictionary,
        the sorting of the dictionary list is performed by the key in alphabetical order
        """
        list_of_dicts = [{'M1': '1', 'D1': 'c', 'D2': 'a'},
                         {'D1': 'a', 'M1': '1', 'D2': 'b'},
                         {'D2': 'b', 'D1': 'b', 'M1': '1'}]
        given_list = etl.ListElements.sorted_list_of_dicts(list_of_dicts, 'D1')
        given_list_any_key = etl.ListElements.sorted_list_of_dicts(list_of_dicts, 'A')
        given_list_without_key = etl.ListElements.sorted_list_of_dicts(list_of_dicts)
        expected_list = [{'D1': 'a', 'D2': 'b', 'M1': '1'},
                         {'D1': 'b', 'D2': 'b', 'M1': '1'},
                         {'D1': 'c', 'D2': 'a', 'M1': '1'}]
        self.assertEqual(given_list, expected_list)
        self.assertEqual(given_list_any_key, expected_list)
        self.assertEqual(given_list_without_key, expected_list)

    def test_key_separation(self):
        """
        Testing key_separation to make sure that these lists are
        divided into two and assigned to class attributes correctly
        """
        list_elements = etl.ListElements(self.file_names)
        list_elements.process_elements()
        res_list_intersection = list_elements.list_intersection()
        sorted_list_by_value = list_elements.sorted_list_of_dicts(res_list_intersection)
        list_elements.key_separation(sorted_list_by_value[0].keys())
        given_keys_with_d = list_elements._keys_with_d
        expected_keys_with_d = ['D1', 'D2']
        given_keys_with_m = list_elements._keys_with_m
        expected_keys_with_m = ['M1']
        self.assertEqual(given_keys_with_d, expected_keys_with_d)
        self.assertEqual(given_keys_with_m, expected_keys_with_m)

    def test_value_conversion(self):
        """
        Testing value_conversion to make sure that string digits are
        converted to integer digits correctly
        """
        list_elements = etl.ListElements(self.file_names)
        list_elements.process_elements()
        res_list_intersection = list_elements.list_intersection()
        sorted_list_by_value = list_elements.sorted_list_of_dicts(res_list_intersection)
        list_elements.key_separation(sorted_list_by_value[0].keys())
        given_converted_list = list_elements.value_conversion(sorted_list_by_value)
        expected_converted_list = [{'D1': 'a', 'D2': 'b', 'M1': 1},
                                   {'D1': 'a', 'D2': 'a', 'M1': 2},
                                   {'D1': 'a', 'D2': 'a', 'M1': 1},
                                   {'D1': 'b', 'D2': 'a', 'M1': 0},
                                   {'D1': 'b', 'D2': 'b', 'M1': 1}]
        self.assertEqual(given_converted_list, expected_converted_list)

    def test_value_conversion_except(self):
        """
        Testing the method to make sure that string values are
        converted to integer digits correctly,
        provided that the values may not be correct
        """
        file_names = [self.file_name_csv_except, self.file_name_json_except, self.file_name_xml]
        list_elements = etl.ListElements(file_names)
        list_elements.process_elements()
        res_list_intersection = list_elements.list_intersection()
        sorted_list_by_value = list_elements.sorted_list_of_dicts(res_list_intersection)
        list_elements.key_separation(sorted_list_by_value[0].keys())
        given_converted_list = list_elements.value_conversion(sorted_list_by_value)
        expected_converted_list = [{'D1': 'a', 'D2': 'b', 'M1': 0},
                                   {'D1': 'a', 'D2': 'a', 'M1': 0},
                                   {'D1': 'a', 'D2': 'a', 'M1': 1},
                                   {'D1': 'b', 'D2': 'a', 'M1': 0},
                                   {'D1': 'b', 'D2': 'b', 'M1': 1}]
        self.assertEqual(given_converted_list, expected_converted_list)

    def test_dictionary_comparison(self):
        """
        Testing dictionary_comparison to check the correctness
        of the dictionary list transformation
        """
        list_elements = etl.ListElements(self.file_names)
        list_elements.process_elements()
        res_list_intersection = list_elements.list_intersection()
        sorted_list_by_value = list_elements.sorted_list_of_dicts(res_list_intersection)
        list_elements.key_separation(sorted_list_by_value[0].keys())
        convert_val = list_elements.value_conversion(sorted_list_by_value)
        given_transformed_list_of_dicts = list_elements.dictionary_comparison(convert_val)
        expected_transformed_list_of_dicts = [{'D1': 'a', 'D2': 'b', 'MS1': 1},
                                              {'D1': 'a', 'D2': 'a', 'MS1': 3},
                                              {'D1': 'b', 'D2': 'a', 'MS1': 0},
                                              {'D1': 'b', 'D2': 'b', 'MS1': 1}]
        self.assertEqual(given_transformed_list_of_dicts, expected_transformed_list_of_dicts)


if __name__ == '__main__':
    unittest.main()
