import filecmp
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from pack.setting import Default_build_dir
from pack.tools import copy

pack_py = f'{__file__}/../pack_library.py'
Build_dir = Default_build_dir


def run_cmd(cmd):
    cmd = cmd.strip().replace('\t', ' '). \
        replace('\n', ' ').replace('  ', ' '). \
        replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
    # print(cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    a_time = time.time()
    while process.poll() is None:
        # 读取标准输出和标准错误流的输出
        stdout_line = process.stdout.readline()
        # stderr_line = process.stderr.readline()
        
        if stdout_line:
            print(f"\rCMD Running: \033[91m{stdout_line.strip()}\033[0m"[:200], end=' ')
    print()
    b_time = time.time() - a_time
    print(f'CMD Run Complete: \033[91m{round(b_time, 2)}s\033[0m')


def get_base_dir():
    p_dir = Path(Build_dir).joinpath('Base')
    if not p_dir.exists():
        print('Packing Base .....')
        base_file = f'{pack_py}/../base.py'
        Path(base_file).parent.mkdir(parents=True, exist_ok=True)
        with open(base_file, 'w') as f:
            f.write(f'print("Is Base")')
        dist_dir = to_pack(Build_dir, base_file, )
        dist_dir.rename(p_dir)
        if Path(base_file).exists():
            try:
                Path(base_file).unlink(missing_ok=True)
            except:
                pass
    return p_dir


def get_dll_file(library_name, reload=False):
    from pack.get_library_dll import Library
    library = Library(library_name)
    library_name = library.name
    
    Path(pack_py).parent.mkdir(parents=True, exist_ok=True)
    with open(pack_py, 'w') as f:
        f.write(f'import {library_name}\n')
        f.write(f'print("import {library_name}")')
    
    dll_dir = Path(Build_dir, ).joinpath(library.name, library.version, 'Dll')
    if dll_dir.exists() and not reload:
        return dll_dir
    other_cmd = f' \n --include-module={library_name} --nofollow-imports'
    if library.dependencies:
        other_cmd += f'\n--nofollow-import-to={",".join(library.dependenciesName)},{library_name}.tests,{library_name}.*.tests '
    
    dist_dir = to_pack(Build_dir, pack_py, other_cmd=other_cmd)
    
    if Path(pack_py).exists():
        try:
            Path(pack_py).unlink(missing_ok=True)
        except:
            pass
    
    base_dir = get_base_dir()
    file_list = compare_folders(base_dir, dist_dir)
    for file in file_list[:]:
        if file.endswith('.exe'):
            file_list.remove(file)
        elif file in ['python3.dll']:
            file_list.remove(file)
    # print(file_list)
    
    for file in file_list:
        p_file = Path(dist_dir).joinpath(file)
        p_dll_file = Path(dll_dir).joinpath(file)
        if not p_dll_file.exists():
            p_dll_file.parent.mkdir(parents=True, exist_ok=True)
            # print(p_file, p_dll_file)
            copy(p_file, p_dll_file)
    
    return dll_dir


def get_pyd_file(library_name):
    return to_pack_library_pyd(library_name)


def get_library_init_import(library_name):
    res_list = []
    __import__(library_name)
    modules = sys.modules
    for name, path in modules.items():
        if name.startswith(f'{library_name}.'):
            res_list.append(name)
    return res_list


def get_library_imports(library_name):
    from pack.get_library_dll import Library
    library = Library(library_name)
    
    library_file = Path(library.library_file)
    if library_file.name == '__init__.py':
        library_file = library_file.parent
    
    else:
        pass


def to_pack(output_dir, pack_file, other_cmd=None):
    pack_res_dir = Path(output_dir).joinpath(Path(pack_file).stem + '.dist')
    
    pack_cmd = f"""
        nuitka
        --mingw
        --standalone
        --show-progress
        --output-dir={output_dir}
        {pack_file}
    """
    if other_cmd:
        pack_cmd += '\n' + str(other_cmd)
    pack_cmd = pack_cmd.replace('\n', ' ')
    
    run_cmd(pack_cmd)
    return pack_res_dir


def to_pack_main(main_py, dependent_libs=None, output_dir=None):
    dependent_list = []
    dependent_names = []
    from pack.get_library_dll import Library
    
    if dependent_libs:
        for lib in dependent_libs:
            dependent_list.append(Library(lib))
    
    for lib in dependent_list:
        print(f'加载库文件{lib}')
        dll = lib.dll_dir
        pyd = lib.pyd
        lib.check_dependencies()
        dependent_names.append(lib.name)
    
    other_cmd = r' '
    if dependent_names:
        other_cmd += f'\n --nofollow-import-to={",".join(dependent_names)} '
    if not output_dir:
        output_dir = Path(main_py).parent
    dist_dir = to_pack(output_dir, main_py, other_cmd)
    for lib in dependent_list:
        dll = lib.dll_dir
        pyd = lib.pyd
        copy(pyd, dist_dir.joinpath(pyd.name))
        if not dll.exists():
            continue
        copy(dll, dist_dir)
    
    os.startfile(dist_dir)


def to_pack_library_pyd(library_name):
    from pack.get_library_dll import Library
    library = Library(library_name)
    library_name = library.name
    library_file = Path(library.library_file)
    if library_file.name == '__init__.py':
        library_file = library_file.parent
    else:
        pass
    output_dir = Path(Build_dir).joinpath(str(library_name), library.version)
    return pack_module(library_file, library_name, output_dir)
    # pyd_name = f'{library_name}.cp{sys.winver.replace(".", "")}*.pyd'
    #
    # pack_cmd = f"""
    #             nuitka
    #             --mingw
    #             --module
    #             --show-progress
    #             --output-dir={output_dir}
    #             --include-module={library_name}
    #             --nofollow-import-to={library_name}.tests,{library_name}.*.tests
    #             {library_file.as_posix()}
    # """
    #
    # pack_cmd = pack_cmd.replace('\n', ' ')
    #
    # run_cmd(pack_cmd)
    # files = list(output_dir.glob(pyd_name))
    # if not files:
    #     raise Exception('打包失败')
    # return files[0]


def pack_module(file, module_name=None, output_dir=None, with_mingw=True, remove_build=False):
    if not module_name:
        module_name = Path(file).stem
    if not output_dir:
        output_dir = Path('NuitkaPackDir').joinpath(module_name)
    
    pyd_name = f'{module_name}.cp{sys.winver.replace(".", "")}*.pyd'
    
    pack_cmd = f"""
                nuitka
                {"--mingw" if with_mingw else ""}
                {"--remove-output" if remove_build else ""}
                --module
                --show-progress
                --output-dir={output_dir}
                --include-module={module_name}
                --nofollow-import-to={module_name}.tests,{module_name}.*.tests
                {file}
    """
    
    pack_cmd = pack_cmd.replace('\n', ' ')
    
    run_cmd(pack_cmd)
    files = list(Path(output_dir).glob(pyd_name))
    if not files:
        raise Exception('打包失败')
    return files[0]


def compare_folders(folder1, folder2):
    # 使用 filecmp 模块来比较两个文件夹
    dcmp = filecmp.dircmp(folder1, folder2)
    # dcmp.report()
    # 获取不同的文件列表
    different_files = dcmp.right_only
    
    return different_files


def get_dir_difference(dir1, dir2, out1=False, out2=False, ):
    for file in Path(dir1).iterdir():
        pass
    pass


if __name__ == '__main__':
    """
    Main run
    """
    get_dll_file('urllib3', reload=True)
    # to_pack_library_pyd('numpy')
