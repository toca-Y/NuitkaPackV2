from setuptools import setup, find_packages

setup(
        name='NuitkaPackV2',  # 包的名称
        version='0.0.1',  # 版本号
        author='toca-Y',  # 作者名字
        author_email='1459229119@qq.com',  # 作者邮箱
        description='借助nuitka更快的打包(分模块打包)',  # 包的简短描述
        long_description='使用nuitka先打包模块,最后打包主程序',  # 包的详细描述
        url='',  # 包的主页或仓库链接
        packages=find_packages(),  # 寻找和包含所有的 Python 包
        install_requires=[
            'nuitka==1.5.8'
        ],  # 依赖项列表，如果有的话
        classifiers=[  # 包的分类
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
)

