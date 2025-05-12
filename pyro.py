import os
import hashlib
import json
from datetime import datetime

def init():

    """
    Initialize a new minigit repository.
    """

    dir = os.getcwd()
    print(f"Path: {dir}")
    file = '.minigit'
    print(f"File: {file}")

    """
    Check if the current directory is already a minigit repository.
        /
    Create the necessary directories for the minigit repository.
    """

    if os.path.isdir(file):
        print(os.listdir(dir))
        print("Repository already initialized.")
        return
    else:
        os.mkdir(os.path.join(dir, '.minigit'))
        os.mkdir(os.path.join(file, 'refs'))
        os.mkdir(os.path.join(file, 'refs', 'heads'))
        os.mkdir(os.path.join(file, 'objects'))
        os.mkdir(os.path.join(file, 'commits'))
        os.mkdir(os.path.join(file, 'status'))
        os.mkdir(os.path.join(file, 'logs'))
        print("Initialized empty minigit repository.")

        # if os.path.isdir(file):
        files = []
        for f in os.listdir(dir):
            if f == '.minigit' or f == '.git':
                continue
            files.append(f)

        with open(os.path.join(file, 'status', 'stat.json'), 'w') as stat:
            pre_data = {'tracked files': [], 'untracked files': files}
            stat.write(json.dumps(pre_data))

        with open(os.path.join(file, 'logs', 'logs.json'), 'a+') as log:
            data = {'logger': []}
            log.write(json.dumps(data))
            

def add(*args):
    dir = os.getcwd()
    file = '.minigit'
    print(f"File: {file}")

    """
    Add files to the staging area.
    """

    if os.path.isdir(file):
        """
        Check if the files exist in the current directory.
        """
        files = set([])
        if args:
            
            for f in args:
                if f in os.listdir(dir):
                    if f == '.minigit' or f == '.git':
                        continue
                    with open(os.path.join(file, 'logs', 'logs.json'), 'r+') as log:
                        log.seek(0)
                        logger_data = json.load(log)
                        data = {'file name': f, 'latest': datetime.now().isoformat(), 'status': 'added', 'commited': False}
                        logger_data['logger'].append(data)
                        log.seek(0)
                        log.truncate()
                        log.write(json.dumps(logger_data))

                    files.add(f)
 
                else:
                    print(f"File {f} not found in the current directory.")
                    # return
            
        else:
            """
            If no files are specified, add all files in the current directory.
            """
            for f in os.listdir(dir):
                if f == '.minigit' or f == '.git':
                    continue

                with open(os.path.join(file, 'logs', 'logs.json'), 'r+') as log:
                    log.seek(0)
                    logger_data = json.load(log)
                    data = {'file name': f, 'latest': datetime.now().isoformat(), 'status': 'added', 'commited': False}
                    logger_data['logger'].append(data)
                    print(data)
                    log.seek(0)
                    log.truncate()
                    log.write(json.dumps(logger_data))
                    
                files.add(f)

        with open(os.path.join(file, 'status', 'stat.json'), 'r+') as stat:
            data = json.load(stat)
            data['untracked files'] = set(data['untracked files'])
            data['tracked files'] = set(data['tracked files'])

            acceptable_files = data['untracked files'] & files
            if len(acceptable_files) != 0:
                data['tracked files'] = data['tracked files'] | acceptable_files
                print(f"Tracked files: {data['tracked files']}")
                data['untracked files'] = data['untracked files'] - acceptable_files
                print(f"Untracked files: {data['untracked files']}")
                data = {'tracked files': list(data['tracked files']), 'untracked files': list(data['untracked files'])}

                stat.seek(0)
                stat.truncate()
                stat.write(json.dumps(data))

    else:
        print("Repository not initialized. Please run 'init' first.")
        return

def status():
    """
    Show the status of the repository.
    """
    MODIFICATION = False
    dir = os.getcwd()
    file = '.minigit'
    # print(f"Path: {dir}")
    # print(f"File: {file}")

    if os.path.isdir(file):
        files = set([])
        for f in os.listdir(dir):
            if f == '.minigit' or f == '.git':
                continue
            files.add(f)

        """
        Read the tracked and untracked files from the stat.json file.
        Output the current status of the repository. If there are any changes, update the stat.json file.
        Not accounted for any direct creation of files in Dir.
        """
        
        with open(os.path.join(file, 'status', 'stat.json'), 'r+') as stat:
            data = json.load(stat)
            print(f"Tracked files: {data['tracked files']}")
            print(f"Untracked files: {data['untracked files']}")

            data['untracked files'] = set(data['untracked files'])
            data['tracked files'] = set(data['tracked files'])

            data['untracked files'] = (data['untracked files'] - files) | (files - ((data['tracked files'] & files) | (data['untracked files'] & files))) | (data['untracked files'] & files)
            MODIFICATION = True
            # if len(data['untracked files']) != 0:
            #     untracked_deleted_files = data['untracked files'] - files
            #     untracked_added_files = files - data['untracked files']

            #     if untracked_deleted_files or untracked_added_files:
            #         MODIFICATION = True
            #         print(f"Untracked data modified")
            #         data['untracked files'] = (data['untracked files'] - untracked_deleted_files) | untracked_added_files

            # if len(data['tracked files']) != 0:
            #     tracked_deleted_files = data['tracked files'] - files
            #     tracked_added_files = files - data['tracked files']

            #     if len(tracked_deleted_files) != 0 or len(tracked_added_files) != 0:
            #         MODIFICATION = True    
            #         print(f"Tracked data modified:")
            #         data['tracked files'] = (data['tracked files'] - tracked_deleted_files)
            #         # data['untracked files'] = (data['untracked files'] | tracked_added_files)

            if MODIFICATION:
                data = {'tracked files': list(data['tracked files']), 'untracked files': list(data['untracked files'])}
                print(f"Tracked files: {data['tracked files']}")
                print(f"Untracked files: {data['untracked files']}")
                stat.seek(0)
                stat.truncate()
                stat.write(json.dumps(data))
                MODIFICATION = False

    else:
        print("Repository not initialized. Please run 'init' first.")
        return


if __name__ == "__main__":
    init()
    print("\n")
    add('pyro.py', 'test.txt')
    print("\n")
    status()
    print("\n")
    with open(os.path.join(os.getcwd(), 'bison.txt'), 'w+') as txt:
        txt.write('This is a test file.')
    status()
    print("\n")
    add()
    print("\n")
    status()
    # Add more functionality as needed
    # For example, you can add functions to add files, commit changes, etc.
