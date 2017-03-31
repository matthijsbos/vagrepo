import json
import os
import os.path
import pathlib
import shutil

class Repository:

    PATH_DEFAULT = os.path.expanduser(os.path.join('~', '.vagrepo'))
    METADATA_FN = 'metadata.json'

    def __init__(self, path=None):
        if path is None:
            self.path = Repository.PATH_DEFAULT
        else:
            self.path = path

        if not os.path.exists(self.path):
            os.makedirs(self.path)
        elif not os.path.isdir(self.path):
            raise ValueError('path %s is not a directory' % self.path)

    @property
    def box_names(self):
        pattern = '**/%s' % Repository.METADATA_FN
        matches = pathlib.Path(self.path).glob(pattern)
        paths = [m.parent.relative_to(self.path) for m in matches]
        return ['/'.join(p.parts) for p in paths]

    def create(self, name, description=None):
        '''Create a new box'''
        name_parts = name.split('/')
        box_dir = pathlib.Path(self.path, *name_parts)
        metadata_path = pathlib.Path(box_dir, Repository.METADATA_FN)

        try:
            box_dir.mkdir(parents=True)
        except FileExistsError as err:
            raise ValueError('box %s already exists' % name) from err

        with metadata_path.open('w') as f:
            json.dump({'name': name, 'versions': []}, f)

    def add(self, name, file, version, provider):
        '''Add a box file to an existing box'''
        file_src_path = pathlib.Path(file)
        name_parts = name.split('/')
        box_dir = pathlib.Path(self.path, *name_parts)
        meta_path = pathlib.Path(box_dir, Repository.METADATA_FN)
        file_dest_dir = pathlib.Path(box_dir, version)
        file_dest_path = pathlib.Path(file_dest_dir, '%s.box' % provider)
        file_dest_dir.mkdir(parents=True)
        shutil.copy(str(file_src_path), str(file_dest_path))

        with meta_path.open() as meta_fp:
            meta_json = json.load(meta_fp)

        meta_json['versions'].append({
            "version": version,
            "providers": [
                {
                    "name": provider,
                    "url": file_dest_path.as_uri(),
                    "checksum_type": "sha1",
                    "checksum": "HASH"
                }
            ]
        })

        with meta_path.open('w') as meta_fp:
            json.dump(meta_json, meta_fp)