# Synchronizer
Python tool for one-way folder synchronization with change logging.

# Description
User is asked to input the path to the Source folder, Replica folder, Log file and the synchronization time interval.
There is no error or exception handling implemented at this step - user must enter valid paths to folders, log file and time interval.
The scripts runs in a infinite while loop until it is terminated and synchronizes the two folders (source and replica).
