import vaex
import os

cwd = os.getcwd()
files = os.listdir(os.path.join(cwd,'zelensky_en'))

df = vaex.open_many([os.path.join('zelensky_en', file) for file in files])

df.export_hdf5("zelensky_en.hdf5")