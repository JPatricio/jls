import os
import stat
from datetime import datetime

from grp import getgrgid
from pwd import getpwuid
from utils.ansi_color_sequences import BColors


class DiskObject(object):
    def __init__(self, full_path, is_file):
        self.full_path = full_path
        # Everything after the last / is the file name
        self.name = full_path.split('/')[-1]
        self.is_file = is_file

    def __str__(self, length: int = None, detailed: bool = False) -> str:
        if detailed:
            details = os.stat(self.full_path)
            mod_timestamp = datetime.fromtimestamp(details.st_mtime)
            return f"{stat.filemode(details.st_mode)} " \
                   f"{str(details.st_nlink).rjust(2, ' ')} " \
                   f"{getpwuid(details.st_uid).pw_name} " \
                   f"{getgrgid(details.st_gid)[0]} " \
                   f"{str(details.st_size).rjust(4, ' ')} " \
                   f"{mod_timestamp.strftime('%b')} " \
                   f"{mod_timestamp.strftime('%d')} " \
                   f"{mod_timestamp.strftime('%H:%M')} " \
                   f"{BColors.OKCYAN if not self.is_file else ''}" \
                   f"{BColors.BOLD if not self.is_file else ''}" \
                   f"{self.name}{BColors.ENDC if not self.is_file else ''}"

        if not length:
            length = len(self.name)+1

        # Directories should show blue
        return f"{BColors.OKCYAN if not self.is_file else ''}" \
               f"{BColors.BOLD if not self.is_file else ''}" \
               f"{self.name.ljust(length, ' ')}{BColors.ENDC if not self.is_file else ''}"
