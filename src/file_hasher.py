import hashlib
import logging



class FileHasher:
    def __init__(self, hash_type: str):
        self.hash_type = hash_type.upper()
        self.logger = logging.getLogger(__name__)

        self.hash_functions = {
            'MD5': hashlib.md5,
            'SHA1': hashlib.sha1,
            'SHA224': hashlib.sha224,
            'SHA256': hashlib.sha256,
            'SHA384': hashlib.sha384,
            'SHA512': hashlib.sha512,
            'SHA3_224': hashlib.sha3_224,
            'SHA3_256': hashlib.sha3_256,
            'SHA3_384': hashlib.sha3_384,
            'SHA3_512': hashlib.sha3_512
        }


        if self.hash_type not in self.hash_functions:
            self.logger.error(f"Unsupported hash type: {self.hash_type}")
            raise ValueError(f"Unsupported hash type: {self.hash_type}")
        
    def _get_hash_function(self):
        return self.hash_functions[self.hash_type]()

    def hash_file(self, file):
        hash_function = self._get_hash_function()
        try:
            with open(file, 'rb') as f:
                for byte_block in iter(lambda: f.read(8192), b""):
                    hash_function.update(byte_block)
            return hash_function.hexdigest()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file}")
        except Exception as e:
            raise Exception(f"Error hashing file {file}: {e}")
            
if __name__ == "__main__":
    file_hasher = FileHasher('SHA256')
    file_path = 'example.txt'
    try:
        file_hash = file_hasher.hash_file(file_path)
        print(f"The SHA256 hash of the file is: {file_hash}")
    except Exception as e:
        print(e)