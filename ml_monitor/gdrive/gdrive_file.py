class GDriveFile:
    def __init__(self, name, id, subfiles=None):
        if subfiles is None:
            subfiles = []
        self.name = name
        self.id = id
        self._subfiles = list(subfiles)

    def __getitem__(self, index):
        if type(index) is str:
            return next(s for s in self._subfiles if s.name == index)
        return self._subfiles[index]

    def append(self, file):
        self._subfiles.append(file)

    def contains(self, filename):
        subfile_names = set(subfile.name for subfile in self._subfiles)
        return filename in subfile_names

    def get_subfile(self, filename):
        subfile = (s for s in self._subfiles if s.name == filename)
        return next(subfile, None)
