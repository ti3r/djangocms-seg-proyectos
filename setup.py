# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from seg_proyectos import __version__


REQUIREMENTS = [
    'django>=2.0',
    'django-cms>=3.5',
    #'aldryn-boilerplates>=0.7.5',
    #'django-emailit',
    #'djangocms-text-ckeditor',
    #'djangocms-attributes-field>=1.0.0',
    #'django-tablib',
    #'tablib',
    #'pillow',
    #'django-filer',
    #'django-sizefield',
    #'six>=1.0',
]


CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Framework :: Django',
    'Framework :: Django :: 2.2',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
]


setup(
    name='seg-proyectos',
    version=__version__,
    author='Alex Blanco',
    author_email='ti3r.bubblenet@gmail.com',
    url='https://github.com/ti3r/djangocms-seg-proyectos.git',
    license='BSD',
    description='Modulo simple para registrar proyectos y seguir las horas trabajadas',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests']),
    package_data={'': ['templates/*']},
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    extras_require={},
    classifiers=CLASSIFIERS,
    test_suite='tests.settings.run',
)