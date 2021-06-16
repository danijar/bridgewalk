import setuptools
import pathlib


setuptools.setup(
    name='bridgewalk',
    version='0.1.0',
    description='Visual reinforcement learning benchmark for controllability.',
    url='http://github.com/danijar/bridgewalk',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=['bridgewalk'],
    package_data={'bridgewalk': ['data.yaml', 'assets/*']},
    entry_points={'console_scripts': ['bridgewalk=bridgewalk.run_gui:main']},
    install_requires=['numpy', 'imageio', 'pillow', 'ruamel.yaml'],
    extras_require={'gui': ['pygame']},
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
