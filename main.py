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

def identify_file_type(folder_path):
    # pass file path into func
    # open file in binary mode
    # read first eight bytes
    # compare bytes against signatures:
    # PNG: 89 50 4E 47 0D 0A 1A 0A
    # PDF: 25 50 44 46 2D
    # JPEG: FF D8 FF
    # return file type or "unknown" if no match
    if not os.path.isdir(folder_path):
        print(f"error: the path '{folder_path}' doesn't exist.")
        return

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                PNG_SIG = bytes.fromhex("89504E470D0A1A0A")
                JPEG_SIG = bytes.fromhex("FFD8FF")
                PDF_SIG = bytes.fromhex("255044462D")

                with open(file_path, "rb") as f:
                    file_bytes = f.read(8)

                    if file_bytes.startswith(PNG_SIG):
                        file_type = "PNG"
                    elif file_bytes.startswith(JPEG_SIG):
                        file_type = "JPEG"
                    elif file_bytes.startswith(PDF_SIG):
                        file_type = "PDF"
                    else:
                        file_type = "unknown"

                print(f"{file}: {file_type}")

                if file_type == "PNG":
                    expected_extension = ".png"
                elif file_type == "JPEG":
                    expected_extention = ".jpeg"
                elif file_type == "PDF":
                    expected_extension = ".pdf"
                else:
                    expected_extension = ""

                name, extension = os.path.splitext(file)

                if expected_extension != "":
                    if file_type == "JPEG":
                        if extension.lower() == ".jpg" or extension.lower() == ".jpeg":
                            print("extensions match.")
                        else:
                            print("extensions don't match.")
                    elif extension.lower() == expected_extension:
                        print("extensions match.")
                    else:
                        print("extensions don't match")
                else:
                    print("couldn't determine file type.")

            except OSError as e:
                print(f"could not examine {file_path}: {e}")

def main():
    folder_path = "sample/"

    examine_folder(folder_path)

    identify_file_type(folder_path)
main()
