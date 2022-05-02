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
python main.py -g ../gs/subtask-entities/distemist_subtrack1_mentions.tsv -p ../toy-data/subtask-entities/distemist_subtrack1_mentions_tests.tsv -s ner
```

+ Subtrack 2 - DisTEMIST Linking

```
cd src  
python main.py -g ../gs/subtask-linking/distemist_subtrack2_linking.tsv -p ../toy-data/subtask-linking/distemist_subtrack2_linking_tests.tsv -s norm
```



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
$ python main.py -g ../gs/subtask-entities/distemist_subtrack1_mentions.tsv -p ../toy-data/subtask-entities/distemist_subtrack1_mentions_tests.tsv -s ner

According to file headers, you are on subtask ner

According to file headers, you are on subtask ner
/home/antonio/Documents/Work/BSC/Projects/Tasks/distemist/distemist_evaluation_library/src/distemist_entities_linking.py:190: FutureWarning: In a future version of pandas all arguments of DataFrame.drop except for the argument 'labels' will be keyword-only
/home/antonio/Documents/Work/BSC/Projects/Tasks/distemist/distemist_evaluation_library/src/distemist_entities_linking.py:201: FutureWarning: In a future version of pandas all arguments of DataFrame.drop except for the argument 'labels' will be keyword-only

-----------------------------------------------------
Clinical case name			Precision
-----------------------------------------------------
es-S0210-48062010000100019-3		1.0
-----------------------------------------------------
es-S0210-56912007000900007-3		0.8571
-----------------------------------------------------

-----------------------------------------------------
Clinical case name			Recall
-----------------------------------------------------
es-S0210-48062010000100019-3		0.8
-----------------------------------------------------
es-S0210-56912007000900007-3		0.8571
-----------------------------------------------------

-----------------------------------------------------
Clinical case name			F-score
-----------------------------------------------------
es-S0210-48062010000100019-3		0.8889
-----------------------------------------------------
es-S0210-56912007000900007-3		0.8571
-----------------------------------------------------

-----------------------------------------------------
Micro-average metrics
-----------------------------------------------------

Micro-average precision = 0.9091


Micro-average recall = 0.8333


Micro-average F-score = 0.8696

../toy-data/subtask-entities/distemist_subtrack1_mentions_tests.tsv|0.9091|0.8333|0.8696

```

+ Subtrack 2

```
$ cd src
$ python main.py -g ../gs/subtask-linking/distemist_subtrack2_linking.tsv -p ../toy-data/subtask-linking/distemist_subtrack2_linking_tests.tsv -s norm

According to file headers, you are on subtask norm, GS file

According to file headers, you are on subtask norm, predictions file
/home/antonio/Documents/Work/BSC/Projects/Tasks/distemist/distemist_evaluation_library/src/ann_parsing.py:45: UserWarning: There are duplicated entries in ../toy-data/subtask-linking/distemist_subtrack2_linking_tests.tsv. Keeping just the first one...
/home/antonio/Documents/Work/BSC/Projects/Tasks/distemist/distemist_evaluation_library/src/distemist_entities_linking.py:190: FutureWarning: In a future version of pandas all arguments of DataFrame.drop except for the argument 'labels' will be keyword-only
/home/antonio/Documents/Work/BSC/Projects/Tasks/distemist/distemist_evaluation_library/src/distemist_entities_linking.py:201: FutureWarning: In a future version of pandas all arguments of DataFrame.drop except for the argument 'labels' will be keyword-only

-----------------------------------------------------
Clinical case name			Precision
-----------------------------------------------------
es-S1130-05582017000200099-1		0.6667
-----------------------------------------------------
es-S1139-76322014000100010-1		0.75
-----------------------------------------------------

-----------------------------------------------------
Clinical case name			Recall
-----------------------------------------------------
es-S1130-05582017000200099-1		0.8
-----------------------------------------------------
es-S1139-76322014000100010-1		0.75
-----------------------------------------------------

-----------------------------------------------------
Clinical case name			F-score
-----------------------------------------------------
es-S1130-05582017000200099-1		0.7273
-----------------------------------------------------
es-S1139-76322014000100010-1		0.75
-----------------------------------------------------

-----------------------------------------------------
Micro-average metrics
-----------------------------------------------------

Micro-average precision = 0.7


Micro-average recall = 0.7778


Micro-average F-score = 0.7368

../toy-data/subtask-linking/distemist_subtrack2_linking_tests.tsv|0.7|0.7778|0.7368
```
