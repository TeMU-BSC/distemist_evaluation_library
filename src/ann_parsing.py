#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:20:04 2020
@author: antonio 
@from: https://github.com/TeMU-BSC/cantemist-evaluation-library/blob/master/src/ann_parsing.py
"""
import pandas as pd
import warnings
import csv

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return '%s:%s: %s: %s\n' % (filename, lineno, category.__name__, message)
warnings.formatwarning = warning_on_one_line


def main(datapath, relevant_labels, codes_path):
    # Load
    valid_codes = set(map(lambda k: k.split('\t')[0], open(codes_path).readlines()))
    df = pd.read_csv(datapath, sep='\t', header=0, quoting=csv.QUOTE_NONE, keep_default_na=False, dtype=str)

    # Check column names are correct
    if ','.join(df.columns) == ','.join(['filename','mark','label','off0','off1','span']):
        print("\nAccording to file headers, you are on subtask ner")
    elif ','.join(df.columns) == ','.join(['filename','mark','label','off0','off1',
                                           'span', 'code']):
        print("\nAccording to file headers, you are on subtask norm, predictions file")
    elif ','.join(df.columns) == ','.join(['filename','mark','label','off0','off1',
                                           'span', 'code', 'semantic_rel']):
        print("\nAccording to file headers, you are on subtask norm, GS file")
    else:
        raise Exception(f'Error! File headers are not correct in {datapath}. Check https://temu.bsc.es/distemist/submission/')

    # Check if there are annotations in file
    if df.shape[0] == 0:
        warnings.warn('There are not parsed annotations')
        return df

    # Format DataFrame
    df_ok = df.loc[df['label'].isin(relevant_labels),:].copy()
    df_ok['offset'] = df_ok['off0'].astype(str) + ' ' + df_ok['off1'].astype(str)
    
    # Check if there are duplicated entries
    if df_ok.shape[0] != df_ok.drop_duplicates(subset=['filename', 'label', 'offset']).shape[0]:
        warnings.warn(f"There are duplicated entries in {datapath}. Keeping just the first one...")
        df_ok = df_ok.drop_duplicates(subset=['filename', 'label', 'offset']).copy()
        
    # Check codes are correct
    if "code" in df_ok.columns:
        # Remove "|" at the beginning and end of code column, in case they exist
        df_ok.loc[:,"code"] = df_ok["code"].apply(lambda k: k.strip("|").strip("+"))
        
        # Check all codes are valid, return lines with unvalid codes
        unvalid_lines = check_valid_codes_in_column(df_ok, "code", valid_codes)
        if len(unvalid_lines)>0:
            unvalid_lines_str = list(map(lambda k: str(k), unvalid_lines))
            warnings.warn(f"Lines {','.join(unvalid_lines_str)} in {datapath} contain unvalid codes. " +
                          f"Valid codes are those that appear in {codes_path}. Ignoring lines with valid codes...")
            df_ok = df_ok.drop(unvalid_lines).copy()

    return df_ok

def split_codes(k):
    codes = k.replace('+', '|').replace('|H','').split('|')
    return codes

def check_valid_codes_in_column(df, colname, valid_codes):
    return df.loc[df[colname].apply(lambda k: any([code not in valid_codes for code in split_codes(k)])),:].index
