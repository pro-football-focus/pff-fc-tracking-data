#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 07:02:07 2024

@author: apschram
"""
from functions import load_metadata, unpack_frames, plot_frame
import pandas as pd
import os

# Set local path to where tracking data files are stored
path = os.path.join(os.getcwd(), 'data')

# Set game identifier
game_id = 27822

# Load metadata
df_rosters, df_metadata = load_metadata(folder_path = path, game_id = game_id)

# Load tracking data
df = pd.read_json(f'{path}/{game_id}.jsonl.bz2', lines = True)

# Unpack frames
df_frames = unpack_frames(df, smoothed_players = True, smoothed_ball = True)

# Find all shots
df_shots = df[df['possession_event_type'] == 'SH']
df_shots = df_shots[['frameNum','period','periodElapsedTime','periodGameClockTime','game_event_id','possession_event_id','shirt_number','game_event_type','home_ball','sequence','possession_event_type']].drop_duplicates()

# Plot all shot frames
for frame in df_shots['frameNum'].unique():
    fig = plot_frame(df_frames, frame, df_metadata)
    os.makedirs(os.path.join(os.getcwd(), 'png', f'{game_id}'), exist_ok = True)
    fig.savefig(os.path.join(os.getcwd(), 'png', f'{game_id}', f'{frame}.png'), dpi=300)