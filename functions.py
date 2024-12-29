#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 07:00:52 2024

@author: apschram
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy
import ast
import os
import pitch

def load_metadata(folder_path, game_id):
    """
    This function loads the associated metadata for a specific game into two pandas DataFrames.
    
    :param folder_path (str): The directory in which the tracking data is stored locally.
    :param game_id (int): The unique game identifier.
    """
    
    # Load roster metadata into pandas 
    df_rosters = pd.read_csv(os.path.join(folder_path, 'metadata', 'rosters.csv'))
    df_rosters = df_rosters[df_rosters['gameId'] == game_id].copy()
    df_rosters['player'] = df_rosters['player'].apply(ast.literal_eval)
    df_rosters[['playerId','playerName']] = df_rosters['player'].apply(pd.Series, dtype = 'object')
    df_rosters['team'] = df_rosters['team'].apply(ast.literal_eval)
    df_rosters[['teamId','teamName']] = df_rosters['team'].apply(pd.Series, dtype = 'object')
    df_rosters['jerseyNum'] = df_rosters['shirtNumber'].astype(str)
    
    # Load game metadata into pandas 
    df_metadata = pd.read_csv(os.path.join(folder_path, 'metadata', 'metadata.csv'))
    df_metadata = df_metadata[df_metadata['gameId'] == game_id].copy()
    
    # Make dict columns readable
    dict_cols = ['stadium','videos','homeTeamKit','homeTeam','awayTeamKit','awayTeam','competition']
    for dict_col in dict_cols:
        df_metadata[dict_col] = df_metadata[dict_col].apply(ast.literal_eval)
    
    # Retrieve fps from metadata
    df_metadata['fps'] = df_metadata['videos'].apply(lambda x: x.get('fps', None) if isinstance(x, dict) else None)

    # Retrieve team colors from metadata
    df_metadata[['homeTeamKitName','homeTeamKitPrimaryColor','homeTeamKitPrimaryTextColor','homeTeamKitSecondaryColor','homeTeamKitSecondaryTextColor']] = df_metadata['homeTeamKit'].apply(pd.Series, dtype='object')
    df_metadata[['awayTeamKitName','awayTeamKitPrimaryColor','awayTeamKitPrimaryTextColor','awayTeamKitSecondaryColor','awayTeamKitSecondaryTextColor']] = df_metadata['awayTeamKit'].apply(pd.Series, dtype='object')
    
    # Retrieve team information from metadata
    df_metadata[['homeTeamId','homeTeamName','homeTeamShortName']] = df_metadata['homeTeam'].apply(pd.Series, dtype='object')
    df_metadata[['awayTeamId','awayTeamName','awayTeamShortName']] = df_metadata['awayTeam'].apply(pd.Series, dtype='object')
    
    # Retrieve competition information from metadata
    df_metadata[['competitionId','competitionName']] = df_metadata['competition'].apply(pd.Series, dtype='object')
    
    # Retrieve stadium information from metadata
    df_metadata['pitches'] = df_metadata['stadium'].apply(lambda x: x.get('pitches', None) if isinstance(x, dict) else None)
    df_metadata['pitches'] = df_metadata['pitches'].apply(pd.Series, dtype='object')
    df_metadata['pitchLength'] = df_metadata['pitches'].apply(lambda x: x.get('length', None) if isinstance(x, dict) else None)
    df_metadata['pitchWidth'] = df_metadata['pitches'].apply(lambda x: x.get('width', None) if isinstance(x, dict) else None)

    return df_rosters, df_metadata

def unpack_frames(dataframe, smoothed_players = False, smoothed_ball = False):    
    """
    This function unpacks the tracking data. The resulting pandas DataFrame contains a player or ball with its x/y coordiantes per row.
    
    :param dataframe (DataFrame): The directory in which the tracking data is stored locally.
    :param smoothed_players (bool): Uses smoothed player locations when True.
    :param smoothed_ball (bool): Uses smoothed ball locations when True.
    """
    
    game_event = dataframe['game_event'].apply(pd.Series, dtype = 'object')
    dataframe['shirt_number'] = game_event['shirt_number']
    dataframe['game_event_type'] = game_event['game_event_type']
    dataframe['home_ball'] = game_event['home_ball']
    dataframe['sequence'] = game_event['sequence']
    
    dataframe['home_ball'] = dataframe['home_ball'].mask(dataframe['home_ball'].ffill() == dataframe['home_ball'].bfill(), dataframe['home_ball'].ffill())
    dataframe['home_ball'] = dataframe['home_ball'].mask(dataframe['game_event_type'].ffill() != 'OUT', dataframe['home_ball'].ffill())

    dataframe['sequence'] = dataframe['sequence'].mask(dataframe['sequence'].ffill() == dataframe['sequence'].bfill(), dataframe['sequence'].ffill())
    dataframe['sequence'] = dataframe['sequence'].mask(dataframe['game_event_type'].ffill() != 'OUT', dataframe['sequence'].ffill())
    
    possession_event = dataframe['possession_event'].apply(pd.Series, dtype = 'object')
    dataframe['possession_event_type'] = possession_event['possession_event_type']

    dataframe['frameNum'] = dataframe['frameNum'].astype(int)
    
    if smoothed_ball == True:
        fill_dict = {'visibility': np.nan, 'x': np.nan, 'y': np.nan, 'z': np.nan}
        dataframe['ballsSmoothed'] = dataframe['ballsSmoothed'].apply(lambda x: fill_dict if x is None else x)
        dataframe['ballsSmoothed'] = dataframe['ballsSmoothed'].apply(lambda x: [x] if isinstance(x, dict) else x)
    
    # Create a dictionary to store player information by frame
    frames_dict = {frame: {'homePlayers': [], 'awayPlayers': [], 'balls': []} for frame in dataframe['frameNum'].unique()}
    
    # Add player and ball data to dictionary
    for _, row in dataframe.iterrows():
        frame_num = row['frameNum']
        if smoothed_players == False and smoothed_ball == False:
            frames_dict[frame_num]['homePlayers'].append(copy.deepcopy(row['homePlayers']))
            frames_dict[frame_num]['awayPlayers'].append(copy.deepcopy(row['awayPlayers']))
            frames_dict[frame_num]['balls'].append(copy.deepcopy(row['balls']))
        if smoothed_players == True and smoothed_ball == False:
            frames_dict[frame_num]['homePlayers'].append(copy.deepcopy(row['homePlayersSmoothed']))
            frames_dict[frame_num]['awayPlayers'].append(copy.deepcopy(row['awayPlayersSmoothed']))
            frames_dict[frame_num]['balls'].append(copy.deepcopy(row['balls']))
        if smoothed_players == False and smoothed_ball == True:
            frames_dict[frame_num]['homePlayers'].append(copy.deepcopy(row['homePlayers']))
            frames_dict[frame_num]['awayPlayers'].append(copy.deepcopy(row['awayPlayers']))
            frames_dict[frame_num]['balls'].append(copy.deepcopy(row['ballsSmoothed']))
        if smoothed_players == True and smoothed_ball == True:
            frames_dict[frame_num]['homePlayers'].append(copy.deepcopy(row['homePlayersSmoothed']))
            frames_dict[frame_num]['awayPlayers'].append(copy.deepcopy(row['awayPlayersSmoothed']))
            frames_dict[frame_num]['balls'].append(copy.deepcopy(row['ballsSmoothed']))
            
    # Remove last frame if smooth player coordinates are used
    if smoothed_players == True:
        frames_dict.popitem()
    
    # Create a list of dictionaries to store player information by frame
    frames_list = []

    # Add player and ball data to list
    for frame, data in frames_dict.items():
        for column, information in data.items():
            for info in information:
                for inf in info:
                    inf['frameNum'] = frame
                    inf['column'] = column

                    frames_list.append(inf)
                        
    # Convert list of dictionaries to dataframe
    df_frames = pd.DataFrame(frames_list).drop_duplicates()
    
    # Create ball indicator
    df_frames['isBall'] = df_frames['column'] == 'balls'
    
    # Create home team indicator
    df_frames['homeTeam'] = df_frames['column'] == 'homePlayers'
    
    # Merge with original dataframe to get sequence and game event information
    df_frames = df_frames.merge(dataframe[['frameNum','period','periodElapsedTime','periodGameClockTime','shirt_number','game_event_type','possession_event_type','home_ball','sequence']].drop_duplicates(), on='frameNum', how='left')
    
    return df_frames

def plot_frame(df_frames, frame_number, df_metadata):
    """
    This function plots a given frame to a pitch plot.
    
    :param df_frames (DataFrame): The pandas DataFrame with unpacked frames.
    :param frame_number (int): The frame number to plot.
    :param df_metadata (DataFrame): The pandas DataFrame with associated metadata.
    """
        
    pitch_length = df_metadata['pitchLength'].iloc[0]
    pitch_width = df_metadata['pitchWidth'].iloc[0]
    home_color1 = df_metadata['homeTeamKitPrimaryColor'].iloc[0]
    home_color2 = df_metadata['homeTeamKitPrimaryTextColor'].iloc[0]
    away_color1 = df_metadata['awayTeamKitPrimaryColor'].iloc[0]
    away_color2 = df_metadata['awayTeamKitPrimaryTextColor'].iloc[0]
    
    df_frames['jerseyNum'] = df_frames['jerseyNum'].fillna(-1)
    
    df_plot = (
        df_frames[df_frames['frameNum'] == frame_number]
        .copy()
        .sort_values(by=['column', 'jerseyNum', 'frameNum'])
        .groupby(['column', 'jerseyNum'], as_index=False)
        .tail(1)
        )
        
    df_plot['x_new'] = df_plot['x'] + (pitch_length / 2)
    df_plot['y_new'] = df_plot['y'] + (pitch_width / 2)
    
    dft0 = df_plot[df_plot['isBall'] == True].reset_index(drop = True)
    
    df_plot = df_plot[df_plot['isBall'] == False]
    
    df_plot['jerseyNum'] = df_plot['jerseyNum'].astype(int)
    
    dft1 = df_plot[(df_plot['homeTeam'] == True) & (df_plot['visibility'] == 'VISIBLE')].reset_index(drop = True)
    dft2 = df_plot[(df_plot['homeTeam'] == False) & (df_plot['visibility'] == 'VISIBLE')].reset_index(drop = True)
    dft3 = df_plot[(df_plot['homeTeam'] == True) & (df_plot['visibility'] == 'ESTIMATED')].reset_index(drop = True)
    dft4 = df_plot[(df_plot['homeTeam'] == False) & (df_plot['visibility'] == 'ESTIMATED')].reset_index(drop = True)
    
    fig, ax = pitch.drawPitch(ax = None, x = pitch_length, y = pitch_width)
    
    plt.scatter(dft1['x_new'], dft1['y_new'], marker = 'o', s = 300, edgecolor = home_color2, linewidth = 2, facecolor = home_color1, label = 'home visible', zorder = 3)
    plt.scatter(dft2['x_new'], dft2['y_new'], marker = 'o', s = 300, edgecolor = away_color2, linewidth = 2, facecolor = away_color1, label = 'away visible', zorder = 3)
    plt.scatter(dft3['x_new'], dft3['y_new'], marker = 'h', s = 300, edgecolor = home_color2, linewidth = 2, facecolor = home_color1, label = 'home estimated', zorder = 3)
    plt.scatter(dft4['x_new'], dft4['y_new'], marker = 'h', s = 300, edgecolor = away_color2, linewidth = 2, facecolor = away_color1, label = 'away estimated', zorder = 3)
    
    plt.scatter(dft0['x_new'], dft0['y_new'], marker = 'o', s = 100, edgecolor = 'black', linewidth = 2, facecolor = 'yellow', label = 'ball', zorder = 5)
    
    plt.legend(loc = 'lower center', bbox_to_anchor = (.5, -0.025, 0, 0), ncol = 3, markerscale = .75, frameon = False)
    
    for i, txt in enumerate(dft1['jerseyNum']):
        plt.annotate(txt, (dft1['x_new'][i], dft1['y_new'][i]), ha='center', va='center', color=home_color2, fontsize=9, weight='bold', zorder=4)
    for i, txt in enumerate(dft2['jerseyNum']):
        plt.annotate(txt, (dft2['x_new'][i], dft2['y_new'][i]), ha='center', va='center', color=away_color2, fontsize=9, weight='bold', zorder=4)
    for i, txt in enumerate(dft3['jerseyNum']):
        plt.annotate(txt, (dft3['x_new'][i], dft3['y_new'][i]), ha='center', va='center', color=home_color2, fontsize=9, weight='bold', zorder=4)
    for i, txt in enumerate(dft4['jerseyNum']):
        plt.annotate(txt, (dft4['x_new'][i], dft4['y_new'][i]), ha='center', va='center', color=away_color2, fontsize=9, weight='bold', zorder=4)
        
    return fig