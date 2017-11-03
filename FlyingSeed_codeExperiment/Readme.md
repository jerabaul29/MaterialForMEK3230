The data can be quite heavy. Put all the videos on an external hard disk that you use also for extracting the pictures, and execute in this order:

- **generate_data**: this can take time, process all pictures and extract seed position, wing tips position.
- **select_valid_range**: select by hand the frames range that should be used for analysis.
- **process_valid_range_data**: apply calibration on valid range data and extract mean vertical velocity and angular velocity.
- **collect_all_data**: collect all data into one results folder on your own computer hard disk. This way, the heavy files are still on the external HDD but you have the light processed data locally.
- **analyze_collected_data**: do additional processing of the collected data. This is also the file in which you will have to write your personal code and scripts.

Note that you will have to adapt the code to your exact needs. In particular, you will have to:

- set up the paths to correspond to your hard disks, computer folders tree etc.
- set up the arguments of the *fnmatch* function calls to select the right folders
- write your own code for plotting the data

In case of doubt, go through the source code.
