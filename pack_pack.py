import sys

from pack.to_pack import pack_module

print(pack_module('pack', output_dir='packPyds', with_mingw=False, remove_build=True))
