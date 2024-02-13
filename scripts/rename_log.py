# we will be browsing folders 
# we will need current sys
import sys
print(f"Current versions {sys.version}")
from datetime import datetime
from pathlib import Path
import os

import gzip
import re
import shutil

def read_gz_file(path):
    with gzip.open(path, 'rt') as f:  # 'rt' mode opens the file in text mode
        file_content = f.readlines()
    return file_content



# folders to combine
folders = ["logs_o26", "logs_j4", "n120224"]
dst = "all_logs"
new_file_suffix = "access_log.gz"

# Create dst directory if it doesn't exist
dst_path = Path(os.path.expanduser("~")) / dst
os.makedirs(dst_path, exist_ok=True)

needle = "*.gz"

files_copied_cnt = 0
conflicts = 0
# print how many files we have in each folder which contain needle
for folder in folders:
    p = Path(os.path.expanduser("~")) / folder
    files = list(p.glob(needle))
    print(f"There are {len(files)} matching {needle} in {p}")
    # first line
    for file in files:
        first_line = read_gz_file(file)[0]
        # print(first_line)
        match = re.search(r'\[(\d{2}/\w{3}/\d{4}):', first_line)
        if match:
            day_month_year = match.group(1)
            day_month_year = day_month_year.replace("/", "_")
            print(day_month_year)
            new_file_name = f"{day_month_year}.{new_file_suffix}"
            file_dst = dst_path / new_file_name
            print(f"Ready to copy to {file_dst}")
            if not file_dst.exists():
                shutil.copy2(file, file_dst)
                files_copied_cnt += 1
            else:
                conflicts += 1
        else:
            print(f"No match on {file}")

print(f"Copied {files_copied_cnt} files to {dst}")
print(f"There were {conflicts} duplicates")


