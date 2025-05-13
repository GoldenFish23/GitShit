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
        # os.mkdir(os.path.join(file, 'refs'))
        # os.mkdir(os.path.join(file, 'refs', 'heads'))
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

        with open(os.path.join(file, 'commits', 'commits.json'), 'w') as commit:
            data = {'commits': []}
            commit.write(json.dumps(data))
            

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
                        log.write(json.dumps(logger_data, indent=3))

                    files.add(f)
 
                else:
                    print(f"File {f} not found in the current directory.")
            
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
                    log.write(json.dumps(logger_data, indent=3))
                    
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

def hash_file(filename):
    """
    Generate a hash for the file.
    """
    sha256 = hashlib.shake_128()
    h = hashlib.sha1()
    with open(filename, 'rb') as f:
        context = f.read()
        sha256.update(context)
        return sha256.hexdigest(10)


def commit(message):
    """
    Commit the changes to the repository.
    """
    dir = os.getcwd()
    file = '.minigit'

    if os.path.isdir(file):
        with open(os.path.join(file, 'status', 'stat.json'), 'r+') as stat:
            data = json.load(stat)
            files = data['tracked files']

            """
            Get the tracked files and update thier log to commited
            """

            for f in files:
                with open(os.path.join(file, 'logs', 'logs.json'), 'r+') as log:
                    log.seek(0)
                    logger_data = json.load(log)
                    data = {
                        'file name': f,
                        'latest': datetime.now().isoformat(),
                        'status': 'commited',
                        'commited': True
                    }
                    logger_data['logger'].append(data)
                    print(data)
                    log.seek(0)
                    log.truncate()
                    log.write(json.dumps(logger_data, indent=3))

            files_commit_map = {}
            for f in files:
                hash_val = hash_file(f)

                objects_dir = os.path.join(file, 'objects', f)
                os.makedirs(objects_dir, exist_ok=True)
                with open(f, 'rb') as original_file:
                    content = original_file.read()
                with open(os.path.join(objects_dir, hash_val), 'wb') as hashed_file:
                    hashed_file.write(content)

                files_commit_map[f] = hash_val

            with open(os.path.join(file, 'commits', 'commits.json'), 'r+') as commit:
                commit.seek(0)
                commit_data = json.load(commit)
                data = {
                    'timestamp': datetime.now().isoformat(),
                    'message': message,
                    'files':files_commit_map
                }
                commit_data['commits'].append(data)
                print(data)
                commit.seek(0)
                commit.truncate()
                commit.write(json.dumps(commit_data, indent=3))


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
    print("H!")
    add()
    print("H!!")
    print("\n")
    status()
    print("\n")
    commit('First commit')
    print("\n")
    status()
    with open(os.path.join(os.getcwd(), 'bison1.txt'), 'w+') as txt:
        txt.write('This is a test file.')
    print("\n")
    status()
    print("\n")
    add()
    print("\n")
    commit('Second commit')
    print("\n")
    with open(os.path.join(os.getcwd(), 'bison1.txt'), 'r+') as txt:
        data = txt.read()
        # print(data)
        data = data + 'Some updated content'
        txt.seek(0)
        txt.truncate()
        txt.write(data)
    print("\n")
    status()
    print("\n")
    add()
    print("\n")
    commit('Last commit')
    print("\n")
    # Add more functionality as needed
    # For example, you can add functions to add files, commit changes, etc.
