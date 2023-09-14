# REQUIREMENTS
#
# Synchronization must be one-way: after the synchronization content of the replica folder should be modified to
# exactly match content of the source folder;
#
# Synchronization should be performed periodically;
#
# File creation/copying/removal operations should be logged to a file and to the console output;
#
# Folder paths, synchronization interval and log file path should be provided using the command line arguments;
#
# It is undesirable to use third-party libraries that implement folder synchronization;
#
# It is allowed (and recommended) to use external libraries implementing other well-known algorithms. For example,
# there is no point in implementing yet another function that calculates MD5 if you need it for the task – it is
# perfectly acceptable to use a third-party (or built-in) library.

# MY SOLUTION
import os
import shutil
import hashlib
import time


def sync_folders(source, replica, log):
    log_action(f'Starting synchronisation\n'
               f'-------------------------------------------------------------------', log_file_path)

    # Create source folder if it doesn't exist
    if not os.path.exists(source):
        os.makedirs(f'{source}')

    # Create replica folder if it doesn't exist
    if not os.path.exists(replica):
        os.makedirs(f'{replica}')

    # Create log file if it doesn't exist
    if not os.path.isfile(f'{log}'):
        with open(log, "w") as f:
            f.write("")

    # Get list of files in source folder
    source_files = [os.path.join(source, f) for f in os.listdir(source)]

    # Get list of files in replica folder
    replica_files = [os.path.join(replica, f) for f in os.listdir(replica)]

    # Copy missing or updated files from source to replica
    # For each file in source
    for source_file in source_files:
        # Assume the current file is also in the replica folder with the same name
        replica_file = os.path.join(replica, os.path.basename(source_file))
        # Check if there is a file with the same filename in replica
        if replica_file in replica_files:
            # If there is, check contents to see if they are the same or not
            source_hash = get_md5(source_file)
            replica_hash = get_md5(replica_file)
            # If the contents are not the same copy the file from source to replica (by default replacing it)
            if source_hash != replica_hash:
                shutil.copy2(source_file, replica_file)
                log_action(f'Updated "{source_file}"', log)
            # In the contents are the same, skip. Optional line to provide info on existing files, we could remove it
            # else:
            #     log_action(f'File "{source_file}" in replica is identical. Skipping...', log)
        # If the current file is not in the replica folder, copy it
        else:
            # Catch the exception where user creates a folder in the source folder, as this will throw an exception
            try:
                shutil.copy2(source_file, replica)
                log_action(f'Copied "{source_file}"', log)
            except PermissionError as e:
                log_action(f'{e}', log)

    # Remove files from replica that don't exist in source
    for replica_file in replica_files:
        if replica_file not in [os.path.join(replica, f) for f in os.listdir(source)]:
            os.remove(replica_file)
            log_action(f'Removed "{replica_file}"', log)

    log_action(f'Synchronisation finished\n'
               f'-------------------------------------------------------------------', log_file_path)


def get_md5(file_path):
    with open(file_path, 'rb') as f:
        md5 = hashlib.md5()
        while chunk := f.read(8192):
            md5.update(chunk)
        return md5.hexdigest()


def log_action(action, log_file):
    with open(log_file, 'a') as f:
        f.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {action}\n')
    print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {action}')


s_folder = input("Enter source folder path: ")
r_folder = input("Enter replica folder path: ")
log_file_path = input("Enter log file path: ")
t_interval = int(input("Enter synchronization interval in seconds: "))

while True:
    sync_folders(s_folder, r_folder, log_file_path)
    time.sleep(t_interval)
