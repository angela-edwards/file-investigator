Investigator goals:
1. what type of file is it regardless of filename?
2. how large is it?
3. when was it last modified according to the file system?
4. can I calculate a unique fingerprint for its contents?
5. are any files identical?
6. is a file's extension inconsistent with its contents?

Python program will scan a folder, analyze each file, and generate a report of findings (CSV).

select evidence folder --> find each file --> examine file --> compare findings --> generate report

modules:
os -- lists files and obtains file info
haslib -- calculates SHA-256 hashes
csv -- write results to CSV report
datetime -- format timestamps into readable dates