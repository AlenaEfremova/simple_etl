# Simple ETL

The console application is a simple ETL with different file formats.

## About the application

The application processes files of any size with extensions `.csv`, `.json` and `xml`, which have a certain structure.  
  
The first file `.csv` has the following structure:

|D1  |D2  |... |Dn  |M1  |M2  |... |Mn  |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|s   |s   |... |s   |i   |i   |... |i   |
|... |... |... |... |... |... |... |... |

The second `.csv` has the following structure: 

|D1  |D2  |... |Dn  |M1  |M2  |... |Mn  |... |Mz  |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|s   |s   |... |s   |i   |i   |... |i   |... |i   |
|... |... |... |... |... |... |... |... |... |... |

The order of the columns may not be the same. Both files have headings.

The `.json` file has the following structure:
```python
{
  "fields": [
    {
      "D1": "s",
      "D2": "s",
      ...
      "Dn": "s",
      "M1": i,
      ...
      "Mp": i,
    },
    ...
  ]
}
```

The `.xml` file contains the following structure:
```xml
<objects>
  <object name="D1">
    <value>s</value>
  </object>
  <object name="D2">
    <value>i</value>
  </object>
  ...
  <object name="Dn">
    <value>s</value>
  </object>
  <object name="M1">
    <value>i</value>
  </object>
  <object name="M2">
    <value>i</value>
  </object>
  ...
  <object name="Mn">
    <value>i</value>
  </object>
</objects>
```

Where *z* > *n*, *p* >= *n*, *s* a string and *i* an integer.  
  
**The result of the program execution is two `.tsv` files.** 
  
The first `.tsv` file contains data from all four files and is sorted by column **D1**.   
It has the following structure:

|D1  |D2  |... |Dn  |M1  |M2  |... |Mn  |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|s   |s   |... |s   |i   |i   |... |i   |
|... |... |... |... |... |... |... |... |

The second `.tsv` file in the columns **MS1**...**MSn** contains the sums of values corresponding to **M1**...**Mn** of the four files, grouped by unique values of combinations of lines from **D1**...**Dn**.  
It has the following structure:

|D1   |D2   |... |Dn   |MS1  |MS2  |...  |MSn  |
|:---:|:--:|:---:|:---:|:---:|:---:|:---:|:---:|
|s    |s   |...  |s    |i    |i    |...  |i    |
|...  |... |...  |...  |...  |...  |...  |...  |

#### Example
Contents of `.tsv` file with data from 4 files:

|D1  |D2  |M1  |M2  |M3  |
|:--:|:--:|:--:|:--:|:--:|
|a   |a   |0   |0   |0   |
|a   |a   |1   |0   |S   |
|a   |a   |0   |2   |1   |
|a   |b   |1   |1   |1   |
|c   |c   |7   |7   |7   |

Result:

|D1  |D2  |M1  |M2  |M3  |
|:--:|:--:|:--:|:--:|:--:|
|a   |a   |1   |2   |1   |
|a   |b   |1   |1   |1   |
|c   |c   |7   |7   |7   |

If there are symbols in the columns with numerical values, an error will be displayed.
However, the program execution will continue and the symbols will be replaced by 0.

## Technologies

The app is written in the language

* Python 3.7.5

## Run

To do this, you should run the command from the terminal in the simple_etl directory specifying the paths to the files to be processed.

#### Example
```
$ python etl.py -i examples/csv_data_1.csv examples/csv_data_2.csv examples/json_data.json examples/xml_data.xml
```

In this case, the files with the result will be located in the simple_etl directory.
It is also possible to specify the paths for the output files.

#### Example
```
$ python etl.py -i examples/csv_data_1.csv examples/csv_data_2.csv examples/json_data.json examples/xml_data.xml -ob examples/basic_results.tsv -oa examples/advanced_results.tsv
```

## Possible improvement options

* Implement testing of all methods of the ListElements class in the test_etl_cls_list_elements.py` module.
* To work with other file types, you can inherit the Element class to add a method for processing the corresponding file type.
Also override the process_elements() method of the ListElements class.
 