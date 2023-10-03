import time

from NuFaster.to_pack import to_pack_main

from NuFaster import set_save_dir

set_save_dir(r'OutputDir')

# # to_pack_main('main-1002.py', ['numpy', 'requests', 'pandas'], 'OutputDir')
# # to_pack_main('main-1002.py', ['numpy', 'requests'], 'OutputDir')
a_time = time.time()
to_pack_main('main-1002.py', ['flask'], 'OutputDir', mingw=True, standalone=True,
             windows_icon_from_ico='ringtones.ico', include_module=['werkzeug'])

print(time.time() - a_time)
