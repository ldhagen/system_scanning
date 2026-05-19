# system_scanning
Python system scanning tools for file metadata analysis and chronological file management.

## Tools

### 1. `system_file_scan.py`
A high-performance scanner that traverses a directory tree and generates a Pandas DataFrame containing file metadata.

- **Features:**
  - Uses native Python `os.walk` for efficient traversal.
  - Calculates MD5 hashes using chunked reading (memory-efficient).
  - Captures structured metadata: path, size, mtime (modification), ctime (creation), and mode.
  - Persists data as a compressed Pickle file for analysis in Jupyter Notebooks.
  - **Dynamic Defaults:** If no output filename is provided, it defaults to `ldh_scan_YYYYMMDD_HHMMSS.pkl` using the current time.

- **Usage:**
  ```bash
  python3 system_file_scan.py [start_path] [output_filename]
  ```

### 2. `walk_id.py`
A utility for identifying and managing files with specific chronological naming conventions (e.g., `ldh<DTG>.jpg`).

- **Features:**
  - Filters files by prefix, suffix, and fixed length.
  - Parses Date-Time Groups (DTG) from filenames into Python `datetime` objects.
  - **Filesystem Boundary Awareness:** Stays within the initial filesystem. It will not traverse into mounted drives (e.g., `/proc`, `/sys`, external volumes) when scanning the host, but can still scan those drives if they are explicitly passed as the `<start_dir>`.
  - Includes a `copy_files` function to chronologically sequence files with adjustable time spacing.
  - **Dynamic Defaults:** If no output filename is provided, it defaults to `DTGscan_YYYYMMDD_HHMMSS.pkl` using the current time.

- **Usage:**
  ```bash
  python3 walk_id.py [start_dir] [output_pickle]
  ```

### 3. `filesystem_hash_review.ipynb`
A Jupyter Notebook designed to analyze the output from `system_file_scan.py`. It allows for easy filtering, hash collision detection, and statistical analysis of the scanned filesystem.

## Data Structure
The `system_file_scan.py` tool generates a DataFrame with the following columns:
- `filename_full_path`: Absolute or relative path to the file.
- `md5_hash`: MD5 checksum of the file content.
- `size`: File size in bytes.
- `mtime`: Last modification time (Unix timestamp).
- `ctime`: File creation time (Unix timestamp).
- `mode`: File permissions and type.
