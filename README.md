# Script Executor README

## Overview
This script is a command-line tool that executes a series of file operations based on a provided input script. It supports various commands such as moving files, categorizing files, counting files, deleting files, renaming files, listing files, and sorting them. The operations are executed sequentially, and the results are logged for later review. 

The script uses the **Factory Design Pattern** to generate different command objects dynamically, and it utilizes the **Strategy Design Pattern** for executing those commands.

### Features:
- **Move Files**: Move the last modified file from one directory to another.
- **Categorize Files**: Move files based on their size (large or small).
- **Count Files**: Count the number of files in a specified directory.
- **Delete Files**: Delete a specified file from a directory.
- **Rename Files**: Rename a file in the directory.
- **List Files**: List all files in a directory.
- **Sort Files**: Sort files by name, size, or creation date.
- **Logging**: The execution results are logged in either CSV or log format for traceability.
- **Configurable Output**: Choose the output format (CSV or log) and the output directory.

## Prerequisites
- **Python 3.x** (The script is compatible with Python 3.x and above)
- The following Python modules:
  - `os`
  - `shutil`
  - `logging`
  - `abc`
  - `json`
  - `argparse`

Make sure to have them installed before running the script.

## Setup and Execution

1. **Download the script**: Download the Python script `executorFinal.py`.

2. **Create a configuration file** (`config.json`):
   - The configuration file must contain the following fields:
     ```json
     {
         "Threshold_size": "5KB",
         "Max_commands": 10,
         "Max_log_files": 5,
         "Same_dir": true,
         "Output": "csv"
     }
     ```
   - **Threshold_size**: The threshold size (in KB) for categorizing files into small and large.
   - **Max_commands**: Maximum number of commands to execute from the script.
   - **Max_log_files**: Maximum number of log files to keep.
   - **Same_dir**: If set to `true`, logs will be stored in the same directory; if `false`, logs will be stored in a separate directory (`PassedDirectory` or `FailedDirectory`).
   - **Output**: Choose between `"csv"` or `"log"` for the log file format.

3. **Run the script**:
   - Use the command below to run the script:
     ```bash
     python executorFinal.py -i <input_script_file> -o <output_directory>
     ```
   - Replace `<input_script_file>` with the path to your script that contains the list of commands to execute.
   - Replace `<output_directory>` with the directory where the output log files will be stored.

## Command Script Format

The input script file should contain a list of commands, one command per line, as shown below:

```plaintext
Mv_last /path/to/source /path/to/destination
Categorize /path/to/directory 1024KB
Count /path/to/directory
Delete file.txt /path/to/directory
Rename old_file.txt new_file.txt /path/to/directory
List /path/to/directory
Sort /path/to/directory name
