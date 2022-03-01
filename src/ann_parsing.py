#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:20:04 2020
@author: antonio 
@from: https://github.com/TeMU-BSC/cantemist-evaluation-library/blob/master/src/ann_parsing.py
"""

import os
import pandas as pd
import warnings

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return '%s:%s: %s: %s\n' % (filename, lineno, category.__name__, message)
warnings.formatwarning = warning_on_one_line

def parse_ann(datapath, relevant_labels, with_notes=False):
    '''
    Parse information in .ann files.
    
    Parameters
    ----------
    datapath : str. 
        Route to the folder where the files are. 
    relevant_labels : list
        List of labels we parse
    with_notes : bool
        whether to take into account AnnotatorNotes or not (Brat comments)
           
    Returns
    -------
    df : pandas DataFrame 
        It has information from ann files. Columns: filename',
        'mark', 'label', 'offset', span' and (if with_notes=True) 'code'
    
    '''
    
    info = []
    
    ## Iterate over the files and parse them
    for root, dirs, files in os.walk(datapath):
         for filename in files:
             if filename[-3:] != 'ann':
                 continue            
             info = parse_one_ann(info, root, filename, relevant_labels,
                                  ignore_related=True, with_notes=with_notes)

    # Save parsed .ann files
    if with_notes == True:
        df = pd.DataFrame(info, columns=['filename', 'mark', 'label','offset',
                                         'span', 'code'])
    else:
        df = pd.DataFrame(info, columns=['filename', 'mark', 'label','offset',
                                         'span'])
    
    return df


def parse_one_ann(info, root, filename, relevant_labels, ignore_related=False,
                  with_notes=False):
    '''
    Parse information in one ANN file.
    
    Parameters
    ----------
    info : list
        it contains parsed ANN information. One element per ANN annotation
    root : str
        route to parent directory where ANN file is stored
    filename : str
        ANN file name
    relevant_labels : list
        ANN labels I will parse
    ignore_related : bool
        whether to ignore annotations included in a Brat relation
    with_notes : bool
        whether to take into account AnnotatorNotes or not (Brat comments)
           
    Returns
    -------
    info : list
        it contains parsed ANN information. One element per ANN annotation
    
    '''
    
    f = open(os.path.join(root,filename)).readlines()
    ### Check all .ANN lines have 3 \t ###
    for line in f:
       splitted = line.split('\t')
       if len(splitted)<3:
            print('ERROR in {}. Line with less than 3 tabular splits: {}.'.format(root+filename, line) +
                  ' Skipping this file...')
            return info
       if len(splitted)>3:
            print('ERROR in {}. Line with more than 3 tabular splits: {}.'.format(root+filename, line) +
                  ' Skipping this file...')
            return info
       if (splitted[0][0] == 'T') & (';' in ' '.join(splitted[1].split(' ')[1:])):
            print('ERROR in {}. Text span with discontinuous annotation: {}.'.format(root+filename, line) +
                  ' Skipping this file...')
            return info
        
    ### Parse .ann file ###
    ignore_marks = []    
    # extract relations
    if ignore_related == True:   
        for line in f:
            if line[0] != 'R':
                continue
            ignore_marks.append(line.split('\t')[1].split(' ')[1].split(':')[1])
            ignore_marks.append(line.split('\t')[1].split(' ')[2].split(':')[1])
            
    mark2code = {}
    if with_notes == True:
        # extract notes
        for line in f:
            if line[0] != '#':
                continue
            line_split = line.split('\t')
            mark2code[line_split[1].split(' ')[1]] = line_split[2].strip()
    
    for line in f:
        if line[0] != 'T':
            continue
        splitted = line.split('\t')

        mark = splitted[0]
        if mark in ignore_marks:
            continue
        label_offset = splitted[1]
        label = label_offset.split(' ')[0]
        if label not in relevant_labels:
            continue
        offset = ' '.join(label_offset.split(' ')[1:])
        span = splitted[2].strip()
        
        if with_notes == False:
            info.append([filename, mark, label, offset, span])
            continue
        
        if mark in mark2code.keys():
            code = mark2code[mark]
            info.append([filename, mark, label, offset, span, code])
            
    return info


def format_df(df):
    '''
    Divide offset column into two: starting and ending annotation positions.
    
    '''
    
    df[['offset0','offset1']] = df['offset'].str.split(' ', n=1, expand=True)
    df['offset0'] = df['offset0'].astype("int")
    df['offset1'] = df['offset1'].astype("int")
    
    return df

def main(datapath, relevant_labels, with_notes=False):
    
    df = parse_ann(datapath, relevant_labels, with_notes)
    if df.shape[0] == 0:
        warnings.warn('There are not parsed annotations')
        return df
    df_ok = format_df(df)
    
    return df_ok