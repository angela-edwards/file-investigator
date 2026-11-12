import os
import hashlib
import csv
import datetime

def examine_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"error: the path '{folder_path}' doesn't exist.")
        return

    print(f"opening folder: {os.path.abspath(folder_path)}\n" + "-" * 50)

    seen_hashes = {}
    report_data = []

    report_data.append([
        "filename",
        "file path",
        "file type",
        "extension mismatch?",
        "file size",
        "SHA-256",
        "last accessed",
        "last modified",
        "duplicate?"
    ])

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                access_time = os.path.getatime(file_path)
                modified_time = os.path.getmtime(file_path)

                readable_access = datetime.datetime.fromtimestamp(access_time)
                readable_modified = datetime.datetime.fromtimestamp(modified_time)

                file_type = identify_file_type(file_path)

                if file_type == "PNG":
                    expected_extension = ".png"
                elif file_type == "JPEG":
                    expected_extension = ".jpeg"
                elif file_type == "PDF":
                    expected_extension = ".pdf"
                else:
                    expected_extension = ""

                name, extension = os.path.splitext(file)

                if expected_extension == "":
                    extension_mismatch = "unknown"
                elif file_type == "JPEG":
                    if extension.lower() == ".jpg" or extension.lower() == ".jpeg":
                        extension_mismatch = "no"
                    else:
                        extension_mismatch = "yes"
                elif extension.lower() == expected_extension:
                    extension_mismatch = "no"
                else:
                    extension_mismatch = "yes"

                # calculate SHA-256 hash
                with open(file_path, "rb") as f:
                    digest = hashlib.file_digest(f, "sha256")

                file_hash = digest.hexdigest()

                if file_hash in seen_hashes:
                    print("\nDUPLICATE FOUND")
                    print(f"  duplicate: {file_path}")
                    print(f"  original: {seen_hashes[file_hash]}")
                    is_duplicate = "yes"
                else:
                    seen_hashes[file_hash] = file_path
                    is_duplicate = "no"

                # add results to list
                report_data.append([
                    file,
                    file_path,
                    file_type,
                    extension_mismatch,
                    file_size,
                    file_hash,
                    readable_access,
                    readable_modified,
                    is_duplicate
                ])

                # display results
                print(f"\nfile: {file}")
                print(f"  path: {file_path}")
                print(f"  type: {file_type}")
                print(f"  extension mismatch: {extension_mismatch}")
                print(f"  size: {file_size} bytes")
                print(f"  SHA-256: {file_hash}")
                print(f"  last accessed: {readable_access}")
                print(f"  last modified: {readable_modified}")

            except OSError as e:
                print(f"could not examine {file_path}: {e}")
    try:    
        with open("forensic_report.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(report_data)

        print("\nreport saved as forensic_report.csv")

    except OSError as e:
        print(f"could not create CSV report: {e}")


def identify_file_type(file_path):
    # pass file path into func
    # open file in binary mode
    # read first eight bytes
    # compare bytes against signatures:
    # PNG: 89 50 4E 47 0D 0A 1A 0A
    # PDF: 25 50 44 46 2D
    # JPEG: FF D8 FF
    # return file type or "unknown" if no match
    PNG_SIG = bytes.fromhex("89504E470D0A1A0A")
    JPEG_SIG = bytes.fromhex("FFD8FF")
    PDF_SIG = bytes.fromhex("255044462D")

    with open(file_path, "rb") as f:
        file_bytes = f.read(8)

        if file_bytes.startswith(PNG_SIG):
            return "PNG"
        elif file_bytes.startswith(JPEG_SIG):
            return "JPEG"
        elif file_bytes.startswith(PDF_SIG):
            return "PDF"
        else:
            return "unknown"

def main():
    folder_path = "sample/"
    examine_folder(folder_path)
    
main()
