#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()

def read_license():
    with open('LICENSE') as f:
        return f.read()


app_version="1.8.9"
app_name = "phantasy"
app_description = 'Physics high-level applications and toolkit for ' \
        'accelerator system'
app_long_description = readme() + '\n\n'
app_platform = ["Linux"]
app_author = "Tong Zhang"
app_author_email = "zhangt@frib.msu.edu"
app_license = read_license()
app_url = "https://archman.github.io/phantasy/"
app_keywords = "phantasy FRIB HLA high-level python FLAME IMPACT"
app_install_requires = [
    'numpy',
    'matplotlib',
    'xlrd',
    'lmfit',
    'scipy',
    'cothread',
    'pyepics',
]
app_extras_require = {
    'test': ['nose', 'nose-exclude', 'coverage'],
}

def get_all_dirs(des_root, src_root):
    ret = []
    for r,d,f in os.walk(src_root):
        ret.append(
                (os.path.join(des_root, r), [os.path.join(r, fi) for fi in f])
        )
    return ret

def set_entry_points():
    r = {}
    r['console_scripts'] = [
        'phytool=phantasy.tools.phytool:main',
        'plot_orbit=phantasy.tools.plot_orbit:main',
        'correct_orbit=phantasy.tools.correct_orbit:main',
        'test_phantasy=phantasy.tests:main',
        'pm_dat2json=phantasy.apps.wire_scanner.converter:main',
    ]

    r['gui_scripts'] = [
        'unicorn_app=phantasy.apps.unicorn:run',
        'lattice_viewer=phantasy.apps.lattice_viewer:run',
        'trajectory_viewer=phantasy.apps.trajectory_viewer:run',
        'correlation_visualizer=phantasy.apps.correlation_visualizer:run',
        'quad_scan=phantasy.apps.quad_scan:run',
        'va_launcher=phantasy.apps.va:run',
        'orm=phantasy.apps.orm:run',
        'wire_scanner=phantasy.apps.wire_scanner:run',
        'settings_manager=phantasy.apps.settings_manager:run',
    ]
    return r

setup(
    name=app_name,
    version=app_version,
    description=app_description,
    long_description=app_long_description,
    author=app_author,
    author_email=app_author_email,
    url=app_url,
    platforms=app_platform,
    license=app_license,
    keywords=app_keywords,
    packages=find_packages(),
    include_package_data=True,
    data_files=get_all_dirs('/etc/phantasy/config', 'demo_mconfig'),
    entry_points=set_entry_points(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Physics'],
    tests_require=['nose'],
    test_suite='nose.collector',
    install_requires=app_install_requires,
    extras_require=app_extras_require,
)
