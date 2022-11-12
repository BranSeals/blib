#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A personal library of (old) Python functions.

These are old and should not be used. Modernize and move into separate modules
and test each function thoroughly.
"""

import datetime
import os
import pathlib
import pwd
import re
import sys
import zipfile
from typing import List

__version__ = "0.1.0"
__author__ = "Bran Seals"
__copyright__ = "Copyright 2021"
__email__ = "bran.seals.dev@gmail.com"
__status__ = "Development"

SCRIPT_NAME = os.path.basename(__file__)
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
SCRIPT_NAME_NO_EXT = pathlib.Path(SCRIPT_PATH).stem
USER = pwd.getpwuid(os.getuid()).pw_name
LOG_PATH = pathlib.Path('Users', USER, 'Desktop', SCRIPT_NAME_NO_EXT + '.log')
LOG_QUIET = False    # quiet mode (dot output)
LOG_SILENT = False   # silent mode (no output)
DT_FILE_FORMAT = '%Y-%m-%d_%H-%M-%S'
DELIM = ';'

# Errors during runtime are appended and mailed to system USER
script_errors = []

# Files excluded from processing errors
ignored_errors = ['errors', '_test_error', '.DS_Store', '.git']


## Strings ##############################################################################


def replace_str(old_new: List[tuple], content: str) -> str:
    """Replace a list of fixes in a given string.

    Using a list of tuples that describe fixes (old string, new string), return the given
    string with these replacements.
    """
    # TODO: handle escape chars
    for i in old_new:
        # TODO: how to use r'i[0]' here? do I need that?
        content = re.sub(i[0], i[1], content)
    return content


def split_string(str_: str, delimiter: str = DELIM) -> List[str]:
    """Split a string based on a delimiter DELIM.
    """
    contents = []
    if str_:
        contents = str_.split(delimiter)
    return contents


def get_rating(content: str) -> int:
    """Find and return a star rating for a given string.

    Questions:
        * Is it faster to check if stars are present using an if statement, or to always
          iterate through the string?
        * Does 'if' also iterate behind the scenes? I want to avoid double iteration
          checks if so.
    """
    stars = 0
    # TODO: get method for formatting star emoticon: filled star vs. empty star
    # TODO: take into account total of filled + empty stars; return float instead?
    # * this might be necessary if for some reason a file doesn't use 4 stars like I do
    if '★' in content:
        for c in content:
            if c == '★':
                stars += 1
    return stars


def has_version(str_):
    """Return whether or not string contains a version number.
    """
    log('ok', "checking if '{}' contains a version number...".format(str_))
    if re.search(r'\d+(\.\d+)+', str_):
        found = True
        log('ok', "'{}' contains a version number".format(str_))
    else:
        found = False
        log('warn', "'{}' does not contain a version number".format(str_))
    return found


def get_version(str_):
    """Return version extracted from string.
    """
    log('ok', "extracting version from '{}'...".format(str_))
    if has_version(str_):
        version = re.search(r'\d+(\.\d+)+', str_).group(0)
    else:
        version = None
    log('ok', "extracted version number: '{}'".format(version))
    return version


def str_in_file(file_, str_):
    """Return whether or not string is found in file."""
    found = str_ in open(file_).read()
    if not found:
        log('warn', "string is not in {}: \"{}\"".format(file_, str_))
    else:
        log('ok', "string is in {}: \"{}\"".format(file_, str_))
    return found


## File Management ######################################################################


def load_file(filepath: pathlib.Path) -> str:
    """Returns a file's content as a string.
    """
    content = None
    if filepath.exists():
        with open(filepath, 'r') as f:
            content = f.read()
    return content


def create_dir(directory: pathlib.PosixPath) -> None:
    """Create a directory if one does not exist.
    """
    if not directory.exists():
        print(f'creating dir: {directory}')
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


def create_file(filename: str, content: str) -> pathlib.PosixPath:
    """Create a file with the given content at the target filepath.
    """
    filepath = pathlib.Path(TEST_WORK_DIR, filename)
    if content:
        with open(filepath, 'w+') as f:
            f.write(content)
    else:
        pathlib.Path(filepath).touch()
    return filepath


def list_files(filepath: pathlib.PosixPath) -> List[str]:
    """Return list of files in a given directory.

    Questions:
        * What do folders look like here, and would they get in the way?
    """
    return os.listdir(filepath)


def list_filepaths(path: str) -> List[pathlib.PosixPath]:
    """List full filepaths from a directory in pathlib format."""
    filenames = os.listdir(path)
    filepaths = []
    if filenames:
        for f in filenames:
            filepaths.append(pathlib.Path(path, f))
    return filepaths


def remove_dir(pth):
    """Remove a directory and its children.

    Question:
        * What happens if the directory is not empty? Is there a useful error?

    Author: rami
    https://stackoverflow.com/questions/50186904/pathlib-recursively-remove-directory
    """
    pth = pathlib.Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


# TEST
def compress(target, destination=None):
    """Compress a target file or folder into optional destination.

    If no destination, target will be compressed in same location.
    """
    log('ok', "compressing '{}'...".format(target))
    if os.path.exists(target):
        destination = destination or path(os.path.dirname(target), os.path.basename(target))
        with zipfile.ZipFile(destination, 'w') as z:
            if os.path.isfile(target):
                log('ok', "recognized as file: '{}'".format(target))
                z.write(target, os.path.basename(target))
            else:
                log('ok', "recognized as folder: '{}'".format(target))
                for file_ in os.listdir(target):
                    z.write(os.path.join(target, file_), os.path.join(os.path.basename(target), file_))
    else:
        log('fail', "does not exist: '{}'".format(target))
        sys.exit(1)
    log('ok', "finished compressing '{}'".format(target))


# TEST
def decompress(target, destination=None):
    """Decompress a target file or folder to optional destination.

    If no destination, target will be decompressed in same location.
    """
    log('ok', "decompressing '{}'...".format(target))
    if zipfile.is_zipfile(target):
        destination = destination or os.path.dirname(target)
        z = zipfile.ZipFile(target, 'r')
        z.extractall(destination)
        z.close()
    else:
        log('fail', "'{}' is not an archive".format(target))
        sys.exit(1)
    log('ok', "finished decompressing '{}' into '{}'".format(target, destination))


# TESTING - DO NOT USE; NEED TO REWRITE
# TODO: use path function to combine stuff
def move(target, destination, auto_remove=False):
    """Move a target file or folder to destination.

    If target already exists at this location, user will be prompted to
    remove it and try again. If auto_remove supplied, removal and
    replacement will occur without user input.
    """
    log('ok', "moving '{}' to '{}'".format(target, destination))
    if not os.path.exists(destination):
        log('warn', "does not exist: '{}'".format(destination))
        os.makedirs(destination)
        log('ok', "created: '{}'".format(destination))
    if os.path.exists(os.path.join(destination, os.path.basename(target))):
        log('warn', "'{}' already exists".format(destination))
        if auto_remove \
           or ask_yn("> Remove and replace '{}'?".format(os.path.join(destination, os.path.basename(target)))):
            delete(os.path.join(destination, os.path.basename(target)))
            log('ok', "removed '{}'".format(destination))
        else:
            log('ok', "not removing '{}'".format(destination))
            return
    shutil.move(target, destination)
    log('ok', "finished moving '{}' to '{}'".format(target, destination))


# TESTING - DO NOT USE; REWRITE OR USE BUILT_IN
# TODO: is it useful to *not* have auto_remove be set as True?
# TEST: seems to be working, but be wary
# TEST use of auto_remove
def delete(target, auto_remove=None):
    """Delete a target file or folder.

    Empty folders immediately removed. If target is folder with content,
    user will be prompted for removal. If auto_remove is True, removal
    will occur without user input.
    """
    log('ok', "deleting '{}'...".format(target))
    if os.path.isdir(target):
        log('ok', "recognized as folder: '{}'".format(target))
        if len(os.listdir(target)):
            log('warn', "folder not empty: '{}'".format(target))
            if auto_remove or ask_yn("> Remove '{}'?".format(target)):
                shutil.rmtree(target)
            else:
                log('ok', "not removing '{}'".format(target))
                return
        else:
            log('ok', "folder is empty: '{}'".format(target))
            os.rmdir(target)
    elif os.path.isfile(target):
        log('ok', "recognized as file: '{}'".format(target))
        os.remove(target)
    else:
        log('fail', "cannot determine file/folder type: '{}'".format(target))
        sys.exit(1)
    log('ok', "finished deleting '{}'".format(target))


# TEST rename; file and folder rename method same?
# TODO: add rename section
def rename(current_filename, new_filename):
    """Rename a target file or folder in-place.

    Return if no name change detected."""
    log('ok', "renaming '{}' as '{}'...".format(current_filename, new_filename))
    if os.path.basename(current_filename) == new_filename:
        log('ok', "no name change")
        return
    os.rename(current_filename, path(os.path.dirname(current_filename), new_filename))


# TODO: add verification / recursion? by checking permissions afterwards
# TODO: check and log that file exists before attempting to change
# TODO: discuss recursive flag use
def chown(target, user, group=None):
    """Change ownership of a target file or folder (Unix-only).

    Return if no target detected. Be careful, as this function is recursive.
    Future option can be added to specify recursion when called. If no group is
    specified, then only the user will be modified."""
    log('ok', "changing ownership of '{}'...".format(target))

    if not os.path.exists(target):
        log('warn', "cannot find chown target: '{}'".format(target))
        return

    if not group:
        shell('chown -R {} "{}"'.format(user, target))
        return

    if group:
        shell('chown -R {}:{} "{}"'.format(user, group, target))
        return

    log('ok', "changed ownership of '{}'".format(target))


# TODO: add verification / recursion? by checking permissions afterwards
# TODO: check and log that file exists before attempting to change
def chmod(target, octal_value):
    """Change mode of a target file or folder (Unix-only).

    Return if no target detected. Be careful, as this function is recursive.
    Future option can be added to specify recursion when called."""
    log('ok', "changing mode of '{}'...".format(target))

    if not os.path.exists(target):
        log('warn', "cannot find chmod target: '{}'".format(target))
        return

    shell('chmod -R {} "{}"'.format(octal_value, target))
    log('ok', "changed mode of '{}'".format(target))


## Command Execution ####################################################################


def run_cmd(list_: List[str], str_: str = None):
    """Run console command using a list of components.

    Assign this function to a value for stdout and stderr.

    Future:
        Accept a string with a normal command format, then break it up
        into a list within this function. It would have to be safe to
        use with spaces intact where required (i.e. ignored in quotes).
    """
    return subprocess.run(list_, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
          text=True, input=str_)


## Logging ##############################################################################


def report_error(error: str) -> None:
    """Add an entry to the error report.
    """
    global script_errors
    script_errors.append(error)


def mail(body: str, subject: str = SCRIPT_NAME, user: str = USER) -> None:
    """Send system mail to the user.
    """
    run(['mail', '-s', subject, user], body)


def send_report(errors: List[str]) -> None:
    """Send a formatted error report to a system user.

    Removes lines containing elements from ignored_errors. Be careful if you
    use substrings that appear in error messages, such as "error".

    Future:
        Is there a better way than O(n^2)?

    Questions:
        * Does this work well for other scripts using this library?
    """
    if errors:
        # Collect the indices to remove
        remove_n = []
        for n, line in enumerate(errors):
            for file in ignored_errors:
                if file in line:
                    remove_n.append(n)

        # Remove indices backwards to avoid re-indexing issues
        for i in sorted(remove_n, reverse=True):
            del errors[i]

    # Check again, because list could now be empty
    if errors:
        mail(format_report(errors))


def _write_log(log_message):
    """Write script runtime events to LOG_PATH.

    For helping log() rather than being called explicitly by user.
    Name of calling script is used with the .py extension removed.
    """
    try:
        if LOG_PATH:
            try:
                with open(LOG_PATH, "a+") as f:
                    f.writelines(datetime.datetime.now()
                                .strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]
                                + " " + f"[{SCRIPT_NAME_NO_EXT}]"
                                + " " + log_message + "\n")
            except PermissionError:
                print('[warn] no permissions for the given log file')
    except:
        return


def log(status, log_message):
    """Output message and write to log based on given status.

    Call with status and a descriptive message. If no log file is set, output
    will only appear in console. If SILENT is set, output will be logged to
    file but will not appear in console. If QUIET is set, output will be dots.
    """
    if len(status) == 2:  # center 2-character statuses (ok, qa)
        message = "[ {} ] {}".format(status, log_message)
    else:
        message = "[{}] {}".format(status, log_message)

    # Respect quiet and silent modes
    if not LOG_QUIET and not LOG_SILENT:
        print(message)
    elif not LOG_SILENT:
        sys.stdout.write('.')
    _write_log(message)


# Wrapper for assert
def require_value(variable_name, variable, error_message="item has no value"):
    log('ok', "checking required value '{}'...".format(variable_name))
    try:
        assert variable, error_message
    except AssertionError:
        log('fail', "required value does not exist: '{}'; exiting...".format(variable_name))
        sys.exit(1)
    log('ok', "value exists for '{}': '{}'".format(variable_name, variable))


## Menus ################################################################################


def ask_yn(yn_message):
    """Returns True if user confirms message, otherwise False."""
    return input("{} [y/n] ".format(yn_message)).lower() in ('y', 'yes')


# TEST
def _menu_list(menu_list):
    """Display numbered list of options.

    Best used with _menu_ui()."""
    for i, option in enumerate(menu_list, 1):
        print("[{}] {}".format(i, option))


# TEST
def _menu_ui(title, menu_list):
    """Display numbered list of options with header and footer.

    Best used with menu_input()."""
    print("\n-- {} --\n".format(title))
    _menu_list(menu_list)
    print("\n--------------------------")


# TEST
# Get selected file from menu
def _menu_input(title, options):
    """Return integer representing the index of the selected option.

    Returned value takes into account the starting value of the
    displayed number (1) and the index (0). For example, user inputs 2
    to select options[1]. Best used with menu_get_item().
    """
    if not len(options):
        log('fail', "no options in '{}' menu".format(title))
        sys.exit(1)
    user_selection = True
    while user_selection:
        _menu_ui(title, options)
        try:
            user_selection = input("> Select [#] or [q]uit: ")
            if (int(user_selection) <= len(options)
                    and (int(user_selection) > 0)):
                break
            else:
                log('warn', "selection out of range: '{}'".format(user_selection))
        except ValueError:
            if user_selection == 'q':
                log('ok', "user exit from '{}' menu".format(title))
                sys.exit(0)
            else:
                log('warn', "selection invalid: '{}'".format(user_selection))
    return int(user_selection) - 1


# TEST
# Display menu of options using menu_input()
def menu(title, options):
    """Return item from options list presented to user as menu.

    Call with a custom menu() function to handle what happens as a
    result of the selection. This could be as simple as selecting a
    particular file, or branching conditionals based on a list of
    choices. See _menu() for example usage.
    """
    option = options[_menu_input(title, options)]
    log('ok', "menu item selected by user: '{}'".format(option))
    return option


## Networking ###########################################################################


# TEST
def get_ip(host):
    """Return IP address of given hostname."""
    log('ok', "checking IP address for '{}'...".format(host))
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        log('warn', "could not connect to '{}'".format(host))
        return None
    if ip == host:
        log('ok', "'{}' already an IP address".format(host))
    else:
        log('ok', "resolved '{}' as '{}'".format(host, ip))
    return ip


def get_local_ip():
    """Return IP address of local machine."""
    log('ok', "checking IP address for local machine...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
    except:  # TODO: get specific exception
        log('warn', "could not get local address")
        return None
    log('ok', "IP address for local machine: '{}'".format(ip))
    return ip


def is_local_machine(address):
    """Return whether or not given address is a local machine."""
    is_local = get_ip(address) == get_local_ip()
    if is_local:
        log('ok', "'{}' is a local machine".format(address))
    else:
        log('ok', "'{}' is a remote machine".format(address))
    return is_local


## Testing ##############################################################################


# TEST
def has_value(str_, variable):
    """Return Boolean of whether or not given variable contains a value.

    Provide string of variable name for logging purposes. This will print a string of the variable's Boolean value, and not its value specifically.
    """
    log('ok', "{}: {}".format(str_, str(bool(variable))))
    return bool(variable)


def equate(a, b):
    """Return whether or not inputs are equal."""
    equal = a == b
    if not equal:
        log('warn', "{} not equal to {}".format(a, b))
    else:
        log('ok', "{} equal to {}".format(a, b))
    return equal


if __name__ == "__main__":

    # Test get_rating:
    stars2 = "I give it ★★☆☆ stars."
    assert get_rating(stars2) == 2
