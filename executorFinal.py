import os  # Importing os module to perform operating system operations
import shutil  # Importing shutil module for file operations
import logging  # Importing logging module for logging purposes
from abc import ABC, abstractmethod  # Importing ABC and abstractmethod for abstract base class definition
import json  # Importing json module for JSON file operations
import argparse  # Importing argparse module for command-line argument parsing

# Setup logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')  # Configuring logging format

# Create a file handler
debug_file_handler = logging.FileHandler('CommandDebugger.log', mode='w')
debug_file_handler.setLevel(logging.DEBUG)  # Set the level to capture all messages

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
debug_file_handler.setFormatter(formatter)

# Add the file handler to the root logger so we can refer to it
logging.getLogger('').addHandler(debug_file_handler)


# Command base class
class Command(ABC):  # Defining an abstract base class for commands
    @abstractmethod
    def execute(self):  # Abstract method for command execution
        raise NotImplementedError("You should implement this method.")


#------------------------------------------------ # Command class for moving the last modified file --------------------------------------------------------------------

class MvLastCommand(Command):
    def __init__(self, src_directory, dest_directory):
        self.src_directory = src_directory  # Source directory path
        self.dest_directory = dest_directory  # Destination directory path

    def execute(self):
        try:
            files = [os.path.join(self.src_directory, f) for f in
                     os.listdir(self.src_directory)]  # Getting list of files in source directory
            files = [f for f in files if os.path.isfile(f)]  # Filtering out only files

            files = [f for f in files if not os.path.basename(f).startswith('.')]  # Filtering out any unhidden files
            print(files)

            if not files:  # If no files found
                raise FileNotFoundError("No files found in source directory")
            latest_file = max(files, key=os.path.getctime)
            shutil.move(latest_file, self.dest_directory)  # Finding the latest file based on creation time
            return f"Mv_last: Moved {os.path.basename(latest_file)} to {self.dest_directory}", "Passed"
        except Exception as e:  # Catching any exceptions
            return f"Mv_last: Failed with error {e}", "Failed"


#------------------------------------------------ # Command class for categorizing files based on size --------------------------------------------------------------------

class CategorizeCommand(Command):
    def __init__(self, directory, threshold_size):
        self.directory = directory  # Directory path
        self.threshold_size = threshold_size  # Threshold size for categorization

    def execute(self):
        try:
            small_dir = os.path.join(self.directory, "small_files")  # Directory for small files
            large_dir = os.path.join(self.directory, "large_files")  # Directory for large files



            os.makedirs(small_dir, exist_ok=True)  # Creating small files directory if not exists
            os.makedirs(large_dir, exist_ok=True)  # Creating large files directory if not exists


            for file in os.listdir(self.directory):
                file_path = os.path.join(self.directory, file)


                # Skip hidden files like
                if file.startswith('.'):
                    print(f"Skipping hidden file: {file}")
                    continue


                if os.path.isfile(file_path):  # If it's a file
                    if os.path.getsize(file_path) < self.threshold_size:  # If file size is less than threshold
                        shutil.move(file_path, small_dir)
                    else:
                        shutil.move(file_path, large_dir)
            return f"Categorize: Files categorized in {self.directory}", "Passed"
        except Exception as e:
            return f"Categorize: Failed with error : {e}", "Failed"


#------------------------------------------------ # Command class for counting files in a directory --------------------------------------------------------------------

class CountCommand(Command):
    def __init__(self, directory):
        self.directory = directory

    def execute(self):
        try:
            count = len([f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))])
            return f"Count: {count} files in {self.directory}", "Passed"
        except Exception as e:
            return f"Count: Failed with error {e}", "Failed"


#--------------------------------------------------------------- # Command class for deleting a file--------------------------------------------------------------------

class DeleteCommand(Command):
    def __init__(self, file_name, directory):
        self.file_name = file_name
        self.directory = directory  # Directory path

    def execute(self):
        try:
            file_path = os.path.join(self.directory, self.file_name)
            os.remove(file_path)  # Removing the file
            return f"Delete: {self.file_name} deleted from {self.directory}", "Passed"
        except Exception as e:
            return f"Delete: Failed with error {e}", "Failed"


#---------------------------------------------------------------# Command class for renaming a file --------------------------------------------------------------------

class RenameCommand(Command):
    def __init__(self, old_name, new_name, directory):
        self.old_name = old_name
        self.new_name = new_name
        self.directory = directory

    def execute(self):
        try:
            old_path = os.path.join(self.directory, self.old_name)  # Old file path
            new_path = os.path.join(self.directory, self.new_name)  # New file path
            os.rename(old_path, new_path)
            return f"Rename: {self.old_name} renamed to {self.new_name} in {self.directory}", "Passed"
        except Exception as e:
            return f"Rename: Failed with error {e}", "Failed"


#------------------------------------------------ # Command class for moving the last modified file --------------------------------------------------------------------

class ListCommand(Command):
    def __init__(self, directory):
        self.directory = directory

    def execute(self):
        try:
            files = os.listdir(self.directory)  # Getting list of files
            return f"List: Files in {self.directory} - {files}", "Passed"
        except Exception as e:
            return f"List: Failed with error {e}", "Failed"


#------------------------------------------------ # Command class for moving the last modified file --------------------------------------------------------------------

class SortCommand(Command):
    def __init__(self, directory, criteria):
        self.directory = directory
        self.criteria = criteria

    def execute(self):
        try:
            files = os.listdir(self.directory)
            if self.criteria == "name":
                files.sort()  # Sort files by name
            elif self.criteria == "date":
                files.sort(key=lambda x: os.path.getctime(os.path.join(self.directory, x)))  # Sort files by date
            elif self.criteria == "size":
                files.sort(key=lambda x: os.path.getsize(os.path.join(self.directory, x)))  # Sort files by size
            else:
                return f"Sort: Unsupported criteria {self.criteria}", "Failed"
            return f"Sort: Files in {self.directory} sorted by {self.criteria}", "Passed"
        except Exception as e:
            return f"Sort: Failed with error {e}", "Failed"


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------# Class to implement Focatory design Pattern---------------------------------------------------------------

class CommandFactory():

    @staticmethod
    def get_command(command_type, *args):
        # used *args because there are different number of argument for each command
        if command_type == "Move":
            return MvLastCommand(args[0], args[1])
        elif command_type == "Categorize":
            return CategorizeCommand(args[0], args[1])
        elif command_type == "Count":
            return CountCommand(args[0])
        elif command_type == "Delete":
            return DeleteCommand(args[0], args[1])
        elif command_type == "Rename":
            return RenameCommand(args[0], args[1], args[2])
        elif command_type == "List":
            return ListCommand(args[0])
        elif command_type == "Sort":
            return SortCommand(args[0], args[1])
        else:
            logging.debug(f"{command_type} is undefined")


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------# Class for executing a script----------------------------------------------------------------------
class ScriptExecutor:
    def __init__(self, config_path, outputDirectory):

        logging.info("New Script Executor Created")

        self.commands = []  # List to store commands
        self.load_config(config_path)  # Loading configuration

        # Set Output Directory, create it if it does not exist
        os.makedirs(outputDirectory, exist_ok=True)
        self.outputDirectory = outputDirectory


        # Set the command debugger log file path
        self.command_debugger_log_file_path = debug_file_handler.baseFilename

        logging.info("---------------------------------------------------------")

    def load_config(self, config_path):  # Method to load configuration
        with open(config_path, 'r') as f:  # Opening config file
            self.config = json.load(f)  # Loading JSON configuration
            logging.info(f"Configuration file opened at: {config_path}")  # Writing Info to log file

        self.threshold_size = int(self.config["Threshold_size"].replace('KB', '')) * 1024  # Setting threshold size
        self.max_commands = self.config["Max_commands"]  # Maximum number of commands to execute
        self.max_log_files = self.config["Max_log_files"]  # Maximum number of log files to keep
        self.same_dir = self.config["Same_dir"]  # Whether to save logs in the same directory
        self.output = self.config["Output"]  # Output format (csv or log)

    def parse_script(self, script_path):  # Method to parse the script
        with open(script_path, 'r') as f:
            lines = f.readlines()  # Reading lines from script
        for line in lines[:self.max_commands]:
            parts = line.rstrip().split()
            cmd = parts[0]  # Command name
            command = None

            # use command factory to get objects of each command
            if cmd == "Mv_last":
                command = CommandFactory.get_command("Move", parts[1], parts[2])
            elif cmd == "Categorize":
                command = CommandFactory.get_command("Categorize", parts[1], self.threshold_size)
            elif cmd == "Count":
                command = CommandFactory.get_command("Count", parts[1])
            elif cmd == "Delete":
                command = CommandFactory.get_command("Delete", parts[1], parts[2])
            elif cmd == "Rename":
                command = CommandFactory.get_command("Rename", parts[1], parts[2], parts[3])
            elif cmd == "List":
                command = CommandFactory.get_command("List", parts[1])
            elif cmd == "Sort":
                command = CommandFactory.get_command("Sort", parts[1], parts[2])

            self.commands.append(command)

        # The rest are unreached
        for line in lines[self.max_commands:]:
            if line.rstrip():  # check if not empty line or just (\n) character
                self.commands.append(line.rstrip())

    def execute_script(self):

        results = {}  # Dictionary to store command results
        all_passed = True  # Flag to track if all commands passed

        i: int = 1

        for command in self.commands[:self.max_commands]:

            logging.info(f"Executing Command Number: {i}")  # Writing Info to log file

            result, status = command.execute()
            results[result] = status  # Storing result and status
            if status == "Failed":
                all_passed = False  # Set all_passed to False
            # Log the result
            logging.debug(f"{result}: {status}")
            logging.info("---------------------------------------------------------")

            i += 1


        # The rest are unreached
        for unreachedLine in self.commands[self.max_commands:]:
            logging.info(f"Executing Command Number: {i}")  # Writing Info to log file
            logging.debug(f"{unreachedLine}, Couldn't Execute Command, Exceeds Max Commands")
            logging.info("---------------------------------------------------------")
            i += 1

        self.log_results(results, all_passed, self.outputDirectory)

    def get_next_log_file_name(self, log_dir, prefix):

        existing_files = [f for f in os.listdir(log_dir) if
                          # Ensure it is a file and not a directory
                          os.path.isfile(os.path.join(log_dir, f)) and f.startswith(
                              prefix)]  # Existing log files with the same prefix

        if not existing_files:
            return f"{prefix}1.csv" if self.output == "csv" else f"{prefix}1.log"  # Return first file name

        existing_files.sort(key=lambda x: int(x[len(prefix):-4]) if x[len(prefix):-4].isdigit() else float('inf'))
        last_file = existing_files[-1]  # Last file
        last_num_str = last_file[len(prefix):-4]  # Remove prefix and extension
        if not last_num_str.isdigit():
            return f"{prefix}1.csv" if self.output == "csv" else f"{prefix}1.log"
        last_num = int(last_num_str)  # Converting last number to integer
        next_num = last_num + 1  # Incrementing number
        return f"{prefix}{next_num}.csv" if self.output == "csv" else f"{prefix}{next_num}.log"  # Return next file name

    def log_results(self, results, all_passed, outputDirectory):
        prefix = "Passed" if all_passed else "Failed"  # Log prefix based on overall script result

        if not self.same_dir:  # If not saving logs in the same directory
            log_dir = os.path.join(outputDirectory,
                                   "PassedDirectory" if all_passed else "FailedDirectory")  # Log directory
            os.makedirs(log_dir, exist_ok=True)  # Creating log directory if not exists
        else:
            log_dir = "./" + outputDirectory  # Use current directory for logging

        log_file = self.get_next_log_file_name(log_dir, prefix)  # Get next log file name

        if self.output == "csv":  # If output format is csv
            with open(os.path.join(log_dir, log_file), 'w') as f:
                for result, status in results.items():
                    f.write(f"{result},{status}\n")  # Writing result to csv file
        else:
            # copy command debugger to new log file
            shutil.copyfile(self.command_debugger_log_file_path, os.path.join(log_dir, log_file))

        # Manage log files
        log_files = [f for f in os.listdir(log_dir) if
                     # Ensure it is a file and not a directory
                     os.path.isfile(os.path.join(log_dir, f)) and f.startswith(
                         prefix)]  # Existing log files with the same prefix

        #print(len(log_files))
        if len(log_files) > self.max_log_files:  # If number of log files exceeds maximum
            log_files.sort(key=lambda x: int(x[len(prefix):-4]) if x[len(prefix):-4].isdigit() else float('inf'))
            excess_files = len(log_files) - self.max_log_files  # Calculate the number of excess files
            for log_file in log_files[:excess_files]:
                os.remove(os.path.join(log_dir, log_file))  # Remove excess files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script Executor')
    parser.add_argument('-i', '--input', required=True, help='Input script file path')
    parser.add_argument('-o', '--outputDirectory', required=True, help='Output folder name')
    args = parser.parse_args()

    # Creating ScriptExecutor instance with config file and with specified output directory
    executor = ScriptExecutor("config.json",
                              args.outputDirectory)
    executor.parse_script(args.input)  # Parsing the input script file
    executor.execute_script()  # Executing the parsed script
