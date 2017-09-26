#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
from fnmatch import fnmatch
from setuptools import setup


def readme():
    with open('README.rst', 'r') as f:
        return f.read()

def read_license():
    with open('LICENSE') as f:
        return f.read()

app_name = "phantasy"
app_description = 'Physics high-level applications and toolkit for accelerator system'
app_long_description = readme() + '\n\n'
app_platform = ["Linux"]
app_author = "Tong Zhang"
app_author_email = "zhangt@frib.msu.edu"
app_license = read_license()
app_url = "https://archman.github.io/phantasy/"
app_keywords = "phantasy FRIB HLA high-level python FLAME IMPACT"
installrequires = [
    'numpy',
    'scipy',
    'matplotlib',
    'xlrd',
#    'tornado',
#    'motor==0.4',
#    'jinja2',
#    'humanize',
#    'jsonschema',
#    'cothread',
#    'nose',
#    'nose-exclude',
#    'coverage',
]
extrasrequire = {
    "LMS": [
        'tornado',
        'humanize',
        'motor==0.4',
        'jinja2',
        'jsonschema',
    ]
}

app_scripts = [i for i in glob.glob("scripts/*") if not fnmatch(i, "scripts/softIoc")]

def get_all_dirs(des_root, src_root):
    ret = []
    for r,d,f in os.walk(src_root):
        ret.append(
                (os.path.join(des_root, r), [os.path.join(r, fi) for fi in f])
        )
    return ret

kns = ('channelfinder', 'operation', 'lattice', 'layout', 'settings',
       'physics', 'pv', 'scan', 'model', 'parser')
d_pkg = {'{0}.{1}'.format(app_name, kn):'{0}/{1}/{2}'.format(
            app_name, 'library', kn) for kn in kns}

setup(
        name=app_name,
        version="0.6.6",
        description=app_description,
        long_description=app_long_description,
        author=app_author,
        author_email=app_author_email,
        url = app_url,
        platforms=app_platform,
        license=app_license,
        keywords=app_keywords,
        scripts=app_scripts,
        packages=d_pkg.keys(),
        package_dir=d_pkg,
        data_files = get_all_dirs('/etc/phantasy/config', 'frib'),
        classifiers=[
            'Programming Language :: Python :: 2.7',
            'Topic :: Software Development :: Libraries :: Python Modules', 
            'Topic :: Scientific/Engineering :: Physics'],
        tests_require=['nose'],
        test_suite='nose.collector',
        #install_requires=installrequires,
        #extras_require=extrasrequire, 
)
