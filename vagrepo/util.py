import hashlib
import pathlib

def file_sha1(file_path):
    '''Compute the hash of a file'''
    hasher = hashlib.sha1()

    with pathlib.Path(file_path).open('rb') as file_fp:
        while True:
            # Read 1K blocks
            block_data = file_fp.read(2**10)
            if not block_data:
                break
            hasher.update(block_data)

    return hasher.hexdigest()
