import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GDriveFile:
    def __init__(self, name, id, subfiles=[]):
        self.name = name
        self.id = id
        self._subfiles = list(subfiles)

    def __getitem__(self, index):
        return self._subfiles[index]

    def append(self, file):
        self._subfiles.append(file)

    def contains(self, filename):
        subfile_names = set(subfile.name for subfile in self._subfiles)
        return filename in subfile_names

    def get_subfile(self, filename):
        subfile = (s for s in self._subfiles if s.name == filename)
        return next(subfile, None)

class GDrive:

    def __init__(self, settings_file=None):
        if settings_file is None:
            settings_file = os.path.join(os.path.dirname(__file__), "settings.yaml")
        GoogleAuth.DEFAULT_SETTINGS["client_config_backend"] = "settings"
        gauth = GoogleAuth(settings_file=settings_file)
        gauth.CommandLineAuth()

        self.drive = GoogleDrive(gauth)
        self.fs = GDriveFile("/", "root")
        self._load_dir(self.fs)

    def get_file(self, path):
        path_parts = filter(None, path.split("/"))
        fs = self.fs
        for part in path_parts:
            if not fs.contains(part):
                self._load_dir(fs)
            fs = fs.get_subfile(part)
        return fs

    def get_dir(self, path):
        dir_fs = self.get_file(path)
        self._load_dir(dir_fs)
        return dir_fs

    def _load_dir(self, dir_file):
        dir_file_list = self.drive.ListFile({"q": f"'{dir_file.id}' in parents and trashed=false"}).GetList()
        for file in dir_file_list:
            dir_file.append(GDriveFile(file["title"], file["id"]))



gdrive = GDrive()
print(gdrive.fs.name)
master_thesis = gdrive.get_dir('master_thesis/')
print(master_thesis.name, '!!')
for file in master_thesis:
    print(file.name)

