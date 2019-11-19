import csv
import json
import argparse
from xml.etree import ElementTree


class Element:
    def __init__(self, file_name):
        self.file_name = file_name
        self.list_of_dicts = list()
        return

    def read_csv(self):
        with open(self.file_name, 'r') as csv_file:
            reader_csv = csv.DictReader(csv_file)
            result = list(reader_csv)
            if len(result) == 0:
                print("\nCSV file is empty")
            self.list_of_dicts.extend(result)
        return

    def read_json(self):
        with open(self.file_name, newline='') as json_file:
            try:
                reader_json = json.load(json_file)
                self.list_of_dicts.extend(reader_json['fields'])
            except ValueError as err:
                print('\nError JSON:  {}'.format(err))
        return

    def read_xml(self):
        try:
            tree = ElementTree.parse(self.file_name)
            root = tree.getroot()
            for obs in root.findall(".//objects"):
                dict_xml = dict()
                for obj in obs:
                    dict_xml[obj.attrib['name']] = obj.find('value').text
                self.list_of_dicts.append(dict_xml)
        except ElementTree.ParseError as err:
            print('\nError parsing XML:  {}'.format(err))
        return

    def keys_of_dicts(self):
        if len(self.list_of_dicts) == 0:
            return list()
        else:
            return self.list_of_dicts[0].keys()

    @staticmethod
    def write_tsv(list_of_dicts, pathname):
        """Writes the list of dictionaries into the '.tsv' file"""
        with open(pathname, 'w', newline='') as out_file:
            tsv_writer = csv.DictWriter(out_file, delimiter='\t', fieldnames=list_of_dicts[0].keys())
            tsv_writer.writeheader()
            tsv_writer.writerows(list_of_dicts)
        return


class ListElements:
    def __init__(self, list_of_file_names):
        self.list_of_file_names = list_of_file_names
        self.elements = list()
        self._keys_with_d = list()
        self._keys_with_m = list()
        return

    def process_elements(self):
        for file_name in self.list_of_file_names:
            element = Element(file_name)
            self.elements.append(element)
            if file_name.endswith('.csv'):
                element.read_csv()
            elif file_name.endswith('.json'):
                element.read_json()
            elif file_name.endswith('.xml'):
                element.read_xml()
            else:
                raise NameError("Acceptable file types - '.csv', '.json', '.xml'")
        return

    def list_intersection(self):
        """
        Looking for intersection of keys that are present in all
        dictionary lists, generates one list of dictionaries with
        these keys and their values
        """
        inter_keys = self.elements[0].keys_of_dicts()
        for element in self.elements:
            inter_keys &= element.keys_of_dicts()
        res_list_of_dicts = list()
        for element in self.elements:
            res_list_of_dicts.extend([{key: dct[key] for key in inter_keys} for dct in element.list_of_dicts])
        return res_list_of_dicts

    @staticmethod
    def sorted_list_of_dicts(res_list_of_dicts, sorting_key=''):
        """Sorts by dictionary key, and then by the values of the specified key"""
        keys_of_dict = res_list_of_dicts[0].keys()
        if sorting_key == '' or sorting_key not in keys_of_dict:
            sorting_key = sorted(keys_of_dict)[0]
            key_sorted_dicts = [{k: dct[k] for k in sorted(dct)} for dct in res_list_of_dicts]
        else:
            key_sorted_dicts = [{k: dct[k] for k in sorted(dct)} for dct in res_list_of_dicts]
        return sorted(key_sorted_dicts, key=lambda i: i[sorting_key])

    def key_separation(self, list_of_keys):
        """
        Divides the list of keys into two, a list in which the key names begin with a 'D'
        and a list where the key names begin with an 'M'
        """
        for key in list_of_keys:
            if key.startswith('D'):
                self._keys_with_d.append(key)
            elif key.startswith('M'):
                self._keys_with_m.append(key)
        return

    def value_conversion(self, list_of_dicts):
        """Conversion of values by specified keys to 'int' type"""
        self.key_separation(list_of_dicts[0].keys())
        converted_list = list()
        for dct in list_of_dicts:
            new_dct = dict()
            for key, value in dct.items():
                if key in self._keys_with_m:
                    try:
                        value = int(value)
                    except ValueError as err:
                        print('\nError in string conversion:  {}'.format(err))
                        value = 0
                new_dct[key] = value
            converted_list.append(new_dct)
        return converted_list

    def dictionary_comparison(self, list_of_dicts):
        """
        Sums the values corresponding to the specified dictionary keys
        by unique combinations of dictionary values
        and forms a new list of dictionaries
        """
        multi_key_dict = dict()
        for dct in list_of_dicts:
            key = tuple([dct.get(key) for key in self._keys_with_d])
            if key in multi_key_dict:
                value = [dct.get(key) for key in self._keys_with_m]
                multi_key_dict[key] = list(map(lambda a, b: a + b, multi_key_dict[key], value))
            else:
                multi_key_dict[key] = [dct.get(key) for key in self._keys_with_m]

        transformed_list_of_dicts = list()
        for keys, values in multi_key_dict.items():
            dct = dict()
            for key, d in zip(keys, self._keys_with_d):
                dct[d] = key
            for val, m in zip(values, self._keys_with_m):
                dct[m.replace('M', 'MS')] = val
            transformed_list_of_dicts.append(dct)
        return transformed_list_of_dicts


if __name__ == "__main__":

    def parser_cmd():
        """Parses command line arguments"""

        parser = argparse.ArgumentParser(prog='simple_etl',
                                         description='The program is a simple ETL with different file formats.')
        parser.add_argument('-i', '--in_files', nargs='*', type=argparse.FileType('r'),
                            required=True, help='files with different formats')
        parser.add_argument('-ob', '--out_basic', type=argparse.FileType('w'),
                            help='optional file path for recording results')
        parser.add_argument('-oa', '--out_advanced', type=argparse.FileType('w'),
                            help='optional file path for recording results')
        args = parser.parse_args()
        return args

    args_parse = parser_cmd()
    file_names = [arg.name for arg in args_parse.in_files]
    list_elements = ListElements(file_names)
    list_elements.process_elements()

    res_list_intersection = list_elements.list_intersection()
    sorted_list_by_value = list_elements.sorted_list_of_dicts(res_list_intersection)
    if args_parse.out_basic is not None:
        Element.write_tsv(sorted_list_by_value, args_parse.out_basic.name)
    else:
        Element.write_tsv(sorted_list_by_value, 'result_basic.tsv')

    convert_val = list_elements.value_conversion(sorted_list_by_value)
    processed_list = list_elements.dictionary_comparison(convert_val)
    if args_parse.out_basic is not None:
        Element.write_tsv(processed_list, args_parse.out_advanced.name)
    else:
        Element.write_tsv(processed_list, 'result_advanced.tsv')
