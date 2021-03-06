from setuptools import setup, find_packages

setup(
    name="EPyQ",
    version="0.1",
    author="EPC Power Corp.",
    classifiers=[
        ("License :: OSI Approved :: "
         "GNU General Public License v2 or later (GPLv2+)")
    ],
    packages=find_packages(),
    entry_points={'gui_scripts': ['epyq = epyq.__main__:main']},
    install_requires=[
        'PyQt5==5.8.2',
        'PyQtChart==5.8.0',
        'SIP==4.19.2',
    ],
    extras_require={
        ':sys_platform == "win32"': ['pyqt5-tools'],
    },
    setup_requires=[
        'vcversioner==2.16.0.0',
    ],
    vcversioner={
        'version_module_paths': ['epyq/_version.py'],
        'vcs_args': ['git', '--git-dir', '%(root)s/.git', 'describe',
                     '--tags', '--long', '--abbrev=999']
    },
)
