import json
import os
import os.path
import pathlib
import shutil

class Repository:

    PATH_DEFAULT = os.path.expanduser(os.path.join('~', '.vagrepo'))
    METADATA_FN = 'metadata.json'
    VAGRANT_SLASH = '-VAGRANTSLASH-'

    def __init__(self, path=None):
        if path is None:
            self.path = Repository.PATH_DEFAULT
        else:
            self.path = path

        if not os.path.exists(self.path):
            os.makedirs(self.path)
        elif not os.path.isdir(self.path):
            raise ValueError('path %s is not a directory' % self.path)

    def _box_dir_path(self, box_name):
        box_dir_name = str(box_name).replace('/', Repository.VAGRANT_SLASH)
        return pathlib.Path(self.path, box_dir_name)

    def _box_metadata_path(self, box_name):
        return pathlib.Path(self._box_dir_path(box_name), \
                            Repository.METADATA_FN)

    def _box_version_dir_path(self, box_name, box_version):
        return pathlib.Path(self._box_dir_path(box_name), box_version)

    def _box_file_path(self, box_name, box_version, box_provider):
        return pathlib.Path(self._box_version_dir_path(box_name, box_version), \
                            '%s.box' % box_provider)

    @property
    def box_names(self):
        pattern = '**/%s' % Repository.METADATA_FN
        matches = pathlib.Path(self.path).glob(pattern)
        paths = [m.parent.relative_to(self.path) for m in matches]
        return [str(p).replace(Repository.VAGRANT_SLASH, '/') for p in paths]

    def create(self, name, description=None):
        '''Create a new box'''

        try:
            self._box_dir_path(name).mkdir(parents=True)
        except FileExistsError as err:
            raise ValueError('box %s already exists' % name) from err

        with self._box_metadata_path(name).open('w') as box_metadata_fp:
            json.dump({'name': name, 'versions': []}, box_metadata_fp)


    def add(self, name, file, version, provider):
        '''Add a box file to an existing box'''
        file_src_path = pathlib.Path(file)

        self._box_version_dir_path(name, version).mkdir(parents=True)

        shutil.copy(str(file_src_path), \
                    str(self._box_file_path(name, version, provider)))

        with self._box_metadata_path(name).open() as meta_fp:
            meta_json = json.load(meta_fp)

        meta_json['versions'].append({
            "version": version,
            "providers": [
                {
                    "name": provider,
                    "url": self._box_file_path(name, version, provider).as_uri(),
                    "checksum_type": "sha1",
                    "checksum": "HASH"
                }
            ]
        })

        with self._box_metadata_path(name).open('w') as box_metadata_fp:
            json.dump(meta_json, box_metadata_fp)
