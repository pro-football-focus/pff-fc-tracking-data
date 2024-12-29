# pff-fc-tracking-data
This repo contains some basic functions that help with unpacking and analyzing PFF FC's broadcast tracking data.
- Function `load_metadata` loads the associated metadata for a specific game into two pandas DataFrames.
- Function `unpack_frames` unpacks the tracking data. The resulting pandas DataFrame contains a player or ball with its x/y coordiantes per row.
- Function `plot_frame` plots a given frame to a pitch plot.

To see an example of how to use the functions, see `run.py`. Note that the code is currently running on two example games stored in subfolder `./data`, with associated metadata stored in `./data/metadata`. To run other games, please make sure to add their tracking data files and metadata to their respective subfolders.
