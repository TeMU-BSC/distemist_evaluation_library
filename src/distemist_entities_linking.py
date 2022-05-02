#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 15:22:29 2022

@author: tonifuc3m
"""

import pandas as pd
import ann_parsing
import warnings
import os

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return '%s:%s: %s: %s\n' % (filename, lineno, category.__name__, message)
warnings.formatwarning = warning_on_one_line


def main(gs_path, pred_path, codes_path, subtask=['ner','norm']):
    '''
    Load GS and Predictions; format them; compute precision, recall and 
    F1-score and show them.

    Parameters
    ----------
    gs_path : str
        Path to directory with GS .ANN files (Brat format).
    pred_path : str
        Path to directory with Predicted .ANN files (Brat format).
    subtask : str
        Subtask name

    Returns
    -------
    None.

    '''
    
    if subtask=='norm':
        gs = ann_parsing.main(gs_path, ['ENFERMEDAD'], codes_path)
        pred = ann_parsing.main(pred_path, ['ENFERMEDAD'], codes_path)
        
        if pred.shape[0] == 0:
            raise Exception('There are not parsed predicted annotations')
        elif gs.shape[0] == 0:
            raise Exception('There are not parsed Gold Standard annotations')
        
    elif subtask=='ner':
        gs = ann_parsing.main(gs_path, ['ENFERMEDAD'], codes_path)
        pred = ann_parsing.main(pred_path, ['ENFERMEDAD'], codes_path)
        
        if pred.shape[0] == 0:
            raise Exception('There are not parsed predicted annotations')
        elif gs.shape[0] == 0:
            raise Exception('There are not parsed Gold Standard annotations')

    else:
        raise Exception('Error! Subtask name not properly set up')

    # Get ANN files in Gold Standard
    ann_list_gs = set(gs['filename'].tolist())
    
    # Remove predictions for files not in Gold Standard
    pred_gs_subset = pred.loc[pred['filename'].isin(ann_list_gs),:]
    
    # Compute metrics
    P_per_cc, P, R_per_cc, R, F1_per_cc, F1 = calculate_metrics(gs, pred_gs_subset, 
                                                                subtask=subtask)
        
    ###### Show results ######  
    print('\n-----------------------------------------------------')
    print('Clinical case name\t\t\tPrecision')
    print('-----------------------------------------------------')
    for index, val in P_per_cc.items():
        print(str(index) + '\t\t' + str(round(val, 4)))
        print('-----------------------------------------------------')
    '''if any(P_per_cc.isna()):
        warnings.warn('Some documents do not have predicted codes, ' + 
                      'document-wise Precision not computed for them.')'''
        
    
    
    print('\n-----------------------------------------------------')
    print('Clinical case name\t\t\tRecall')
    print('-----------------------------------------------------')
    for index, val in R_per_cc.items():
        print(str(index) + '\t\t' + str(round(val, 4)))
        print('-----------------------------------------------------')
    '''if any(R_per_cc.isna()):
        warnings.warn('Some documents do not have Gold Standard codes, ' + 
                      'document-wise Recall not computed for them.')'''
    
    
    print('\n-----------------------------------------------------')
    print('Clinical case name\t\t\tF-score')
    print('-----------------------------------------------------')
    for index, val in F1_per_cc.items():
        print(str(index) + '\t\t' + str(round(val, 4)))
        print('-----------------------------------------------------')
    '''if any(P_per_cc.isna()):
        warnings.warn('Some documents do not have predicted codes, ' + 
                      'document-wise F-score not computed for them.')
    if any(R_per_cc.isna()):
        warnings.warn('Some documents do not have Gold Standard codes, ' + 
                      'document-wise F-score not computed for them.')'''
        
    print('\n-----------------------------------------------------')
    print('Micro-average metrics')
    print('-----------------------------------------------------')
    print('\nMicro-average precision = {}\n'.format(round(P, 4)))
    print('\nMicro-average recall = {}\n'.format(round(R, 4)))
    print('\nMicro-average F-score = {}\n'.format(round(F1, 4)))
    
    print('{}|{}|{}|{}'.format(pred_path,round(P, 4),round(R, 4),round(F1, 4)))


def calculate_metrics(gs, pred, subtask=['ner','norm']):
    '''       
    Calculate task Coding metrics:
    
    Two type of metrics are calculated: per document and micro-average.
    It is assumed there are not completely overlapping annotations.
    
    Parameters
    ---------- 
    gs : pandas dataframe
        with the Gold Standard. Columns are those defined in main function.
    pred : pandas dataframe
        with the predictions. Columns are those defined in main function.
    subtask : str
        subtask name
    
    Returns
    -------
    P_per_cc : pandas series
        Precision per clinical case (index contains clinical case names)
    P : float
        Micro-average precision
    R_per_cc : pandas series
        Recall per clinical case (index contains clinical case names)
    R : float
        Micro-average recall
    F1_per_cc : pandas series
        F-score per clinical case (index contains clinical case names)
    F1 : float
        Micro-average F1-score
    '''
    
    # Predicted Positives:
    Pred_Pos_per_cc = \
        pred.drop_duplicates(subset=['filename', "offset"]).\
        groupby("filename")["offset"].count()
    Pred_Pos = pred.drop_duplicates(subset=['filename', "offset"]).shape[0]

    # Gold Standard Positives:
    GS_Pos_per_cc = \
        gs.drop_duplicates(subset=['filename', "offset"]).\
        groupby("filename")["offset"].count()
    GS_Pos = gs.drop_duplicates(subset=['filename', "offset"]).shape[0]
    
    # Eliminate predictions not in GS (prediction needs to be in same clinical
    # case and to have the exact same offset to be considered valid!!!!)
    df_sel = pd.merge(pred, gs, 
                      how="right",
                      on=["filename", "offset", "label"])
    
    if subtask=='norm':
        # Check if codes are equal
        df_sel["is_valid"] = \
            df_sel.apply(lambda x: (x["code_x"] == x["code_y"]), axis=1)
    elif subtask=='ner':
        is_valid = df_sel.apply(lambda x: x.isnull().any()==False, axis=1)
        df_sel = df_sel.assign(is_valid=is_valid.values)
    else:
        raise Exception('Error! Subtask name not properly set up')

        
    # True Positives:
    TP_per_cc = (df_sel[df_sel["is_valid"] == True]
                 .groupby("filename")["is_valid"].count())
    TP = df_sel[df_sel["is_valid"] == True].shape[0]
    
    # Add entries for clinical cases that are not in predictions but are present
    # in the GS
    cc_not_predicted = (pred.drop_duplicates(subset=["filename"])
                        .merge(gs.drop_duplicates(subset=["filename"]), 
                              on='filename',
                              how='right', indicator=True)
                        .query('_merge == "right_only"')
                        .drop('_merge', 1))['filename'].to_list()
    for cc in cc_not_predicted:
        TP_per_cc[cc] = 0
    
    # Remove entries for clinical cases that are not in GS but are present
    # in the predictions
    cc_not_GS = (gs.drop_duplicates(subset=["filename"])
                .merge(pred.drop_duplicates(subset=["filename"]), 
                      on='filename',
                      how='right', indicator=True)
                .query('_merge == "right_only"')
                .drop('_merge', 1))['filename'].to_list()
    Pred_Pos_per_cc = Pred_Pos_per_cc.drop(cc_not_GS)

    # Calculate Final Metrics:
    P_per_cc =  TP_per_cc / Pred_Pos_per_cc
    P = TP / Pred_Pos
    R_per_cc = TP_per_cc / GS_Pos_per_cc
    R = TP / GS_Pos
    F1_per_cc = (2 * P_per_cc * R_per_cc) / (P_per_cc + R_per_cc)
    if (P+R) == 0:
        F1 = 0
        warnings.warn('Global F1 score automatically set to zero to avoid division by zero')
        return P_per_cc, P, R_per_cc, R, F1_per_cc, F1
    F1 = (2 * P * R) / (P + R)
    
    
    if ((any([F1, P, R]) > 1) | any(F1_per_cc>1) | any(P_per_cc>1) | any(R_per_cc>1) ):
        warnings.warn('Metric greater than 1! You have encountered an undetected bug, please, contact antonio.miranda@bsc.es!')
                                            
    return P_per_cc, P, R_per_cc, R, F1_per_cc, F1