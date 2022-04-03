# 1. Introduction

Scripts to compute DisTEMIST evaluation metrics.

Written in Python 3.7


# 2. Requirements

+ Python3
+ pandas

To install them: 
```
pip install -r requirements.txt
```


# 3. Execution
+ Subtrack 1 - DisTEMIST Entities 

```
cd src  
python main.py -g ../gs/sample_entities_subtask1.tsv -p ../toy-data/sample_entities_subtask1_MISSING_ONE_FILE.tsv -s ner
```

+ Subtrack 2 - DisTEMIST Linking

To be published



# 4. Other interesting stuff:

### Metrics

For Subtrack 1 the relevant metrics are precision, recall and f1-score. The latter will be used to decide the award winners.

For Subtrack 2 the relevant metric is still to be disclosed.

For more information about metrics, see the shared task webpage: https://temu.bsc.es/distemist/

### Script Arguments
+ ```-g/--gs_path```: path to Gold Standard TSV file with the annotations
+ ```-p/--pred_path```: path to predictions TSV file with the annotations
+ ```-c/--valid_codes_path```: path to TSV file with valid codes (provided here).
+ ```-s/--subtask```: subtask name (```ner```, ```norm```, or ```app```).

### Examples: 

+ Subtrack 1

```
$ cd src
$ python main.py -g ../gs/toy_data_gs.tsv -p ../toy-data/toy_data_ner_remove_one_document.tsv -s ner
```

