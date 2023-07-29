import os
import shutil

def reset_cloud():
    shutil.rmtree("./cloud")
    os.mkdir("./cloud")