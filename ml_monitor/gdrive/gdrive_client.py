import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from ml_monitor.gdrive import GDriveFile


class GDriveClient:
    def __init__(self, settings_file=None):
        if settings_file is None:
            settings_file = os.path.join(os.path.dirname(__file__), "settings.yaml")
        GoogleAuth.DEFAULT_SETTINGS["client_config_backend"] = "settings"
        gauth = GoogleAuth(settings_file=settings_file)
        gauth.CommandLineAuth()

        self.drive = GoogleDrive(gauth)
        self.root = GDriveFile("/", "root")
        self._load_dir(self.root)

    def get(self, path):
        path_parts = filter(None, path.split("/"))
        file_handler = self.root
        for part in path_parts:
            if not file_handler.contains(part):
                self._load_dir(file_handler)
            file_handler = file_handler.get_subfile(part)
            if file_handler is None:
                break
        return file_handler

    def get_dir(self, path):
        dir_handler = self.get(path)
        self._load_dir(dir_handler)
        return dir_handler

    def download(self, path, filename=None):
        file_handler = self.get(path)
        gdrive_file = self.drive.CreateFile({"id": file_handler.id})
        if filename is None:
            filename = gdrive_file["title"]
        gdrive_file.GetContentFile(filename)

    def create(self, path, directory=False):
        path_parts = list(filter(None, path.split("/")))
        dirs, filename = path_parts[:-1], path_parts[-1]
        file_handler = self.root
        for dir_name in dirs:
            if not file_handler.contains(dir_name):
                self._create_file(dir_name, file_handler, directory=True)
            file_handler = file_handler.get_subfile(dir_name)
        if not file_handler.contains(filename):
            self._create_file(filename, file_handler, directory=directory)
        return file_handler.get_subfile(filename)

    def upload(self, src, dst):
        dst_file_handler = self.create(dst)
        gdrive_file = self.drive.CreateFile({"id": dst_file_handler.id})
        gdrive_file.SetContentFile(src)
        gdrive_file.Upload()
        return dst_file_handler

    def _load_dir(self, dir_file):
        dir_file_list = self.drive.ListFile(
            {"q": f"'{dir_file.id}' in parents and trashed=false"}
        ).GetList()
        for file in dir_file_list:
            dir_file.append(GDriveFile(file["title"], file["id"]))

    def _create_file(self, filename, parent_handler, directory=False):
        gdrive_file_data = {
            "title": filename,
            "parents": [{"id": parent_handler.id}],
        }
        if directory:
            gdrive_file_data["mimeType"] = "application/vnd.google-apps.folder"
        gdrive_file = self.drive.CreateFile(gdrive_file_data)
        gdrive_file.Upload()
        file_id = gdrive_file["id"]
        parent_handler.append(GDriveFile(filename, file_id))
