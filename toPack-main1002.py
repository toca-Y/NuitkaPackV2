from NuitkaPack.to_pack import to_pack_main

from NuitkaPack import set_save_dir

set_save_dir(r'OutputDir')

# # to_pack_main('main-1002.py', ['numpy', 'requests', 'pandas'], 'OutputDir')
# # to_pack_main('main-1002.py', ['numpy', 'requests'], 'OutputDir')
to_pack_main('main-1002.py', ['requests'], 'OutputDir', mingw=True, standalone=True,
             windows_icon_from_ico='ringtones.ico')
