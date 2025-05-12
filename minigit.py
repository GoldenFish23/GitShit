import os
import sys
import hashlib
import shutil
import time
import argparse

def hash_file(filename):
    hash_sha1 = hashlib.sha1()
    with open(filename, 'rb') as f:
        while chunk := f.read(8192):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()

def init():
    if os.path.exists('.minigit'):
        print("Repository already initialized.")
        return 
    os.makedirs('.minigit/objects', exist_ok=True)
    os.makedirs('.minigit/commits', exist_ok=True)
    os.makedirs('.minigit/refs', exist_ok=True)
    os.makedirs('.minigit/index', exist_ok=True)

    # with open('.minigit/refs/heads/master', 'w') as f:
    #     f.write('')

    print("Repo initialized. You can now start using minigit.")

def add(file):
    file_hash = hash_file(file)
    with open('.minigit/index', 'a') as index:
        index.write(f"{file_hash} {file}\n")
    print(f"Added {file} to staging.")

# Commit staged changes
def commit(message):
    if not os.path.exists('.minigit/index') or os.stat('.minigit/index').st_size == 0:
        print("No files staged for commit.")
        return
    
    commit_hash = hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest()  # Unique commit ID
    commit_path = f'.minigit/commits/{commit_hash}'
    
    with open(commit_path, 'w') as commit_file:
        commit_file.write(f"Commit Hash: {commit_hash}\n")
        commit_file.write(f"Timestamp: {time.time()}\n")
        commit_file.write(f"Message: {message}\n")
        commit_file.write("Files:\n")
        with open('.minigit/index', 'r') as index:
            for line in index:
                commit_file.write(f"{line}")
    
    # with open('.minigit/refs/heads/master', 'w') as ref:
    #     ref.write(commit_hash)
    
    print(f"Commit successful with message: {message}")
    
    # Clear the index after commit
    open('.minigit/index', 'w').close()

# Status to show staged files
def status():
    if not os.path.exists('.minigit/index') or os.stat('.minigit/index').st_size == 0:
        print("No files staged for commit.")
        return
    
    print("Staged files:")
    with open('.minigit/index', 'r') as index:
        for line in index:
            print(line.strip())

# Main function to handle commands
def main():
    command = input("Enter command (init, add, commit, status): ").strip()
    
    if command == 'init':
        init()
    elif command == 'add':
        file = input("Enter file to add: ").strip()
        if os.path.exists(file):
            add(file)
        else:
            print(f"File {file} does not exist.")
    elif command == 'commit':
        message = input("Enter commit message: ").strip()
        commit(message)
    elif command == 'status':
        status()
    else:
        print("Unknown command.")

if __name__ == "__main__":
    main()