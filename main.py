import os
import hashlib
import csv
import datetime

def examine_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"error: the path '{folder_path}' doesn't exist.")
        return

    print(f"opening folder: {os.path.abspath(folder_path)}\n" + "-" * 50)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                access_time = os.path.getatime(file_path)
                modified_time = os.path.getmtime(file_path)

                readable_access = datetime.datetime.fromtimestamp(access_time)
                readable_modified = datetime.datetime.fromtimestamp(modified_time)

                # calculate SHA-256 hash
                with open(file_path, "rb") as f:
                    digest = hashlib.file_digest(f, "sha256")

                # display results
                print(f"\nfile: {file}")
                print(f"  path: {file_path}")
                print(f"  size: {file_size} bytes")
                print(f"  SHA-256: {digest.hexdigest()}")
                print(f"  last accessed: {readable_access}")
                print(f"  last modified: {readable_modified}")
            
            except OSError as e:
                print(f"could not examine {file_path}: {e}")

            with open(file_path, "rb") as f:
                digest = hashlib.file_digest(f, "sha256")

            print(f"hash = {digest.hexdigest()}")

            timestamp = os.path.getatime(file_path)

            readable_time = datetime.datetime.fromtimestamp(timestamp)

            print(f"unix timestamp: {timestamp}")
            print(f"last modified: {readable_time}\n")

def main():
    folder_path = "sample/"

    examine_folder(folder_path)

    # filename = "angry-face-emoticon-9.png"

    # rb means read file as binary data
    # file = open(filename, "rb")

    # read first 8 bytes
    # first_bytes = file.read(8)

    # file.close()

    # print(first_bytes)

    # print(first_bytes.hex())

main()
