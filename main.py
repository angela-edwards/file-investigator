import os
import hashlib
import csv
import datetime

def examine_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"error: the path '{folder_path}' doesn't exist.")
        return

    print(f"opening folder: {os.path.abspath(folder_path)}\n" + "-" * 50)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)

                print(f"file: {file}")
                print(f"  path: {file_path}")
                print(f"  size: {file_size}")
            except OSError as e:
                print(f"could not examine {file_path}: {e}")

            with open(file_path, "rb") as f:
                digest = hashlib.file_digest(f, "sha256")

            print(f"hash = {digest.hexdigest()}")

            timestamp = os.path.getatime(file_path)

            readable_time = datetime.datetime.fromtimestamp(timestamp)

            print(f"unix timestamp: {timestamp}")
            print(f"last modified: {readable_time}")

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
