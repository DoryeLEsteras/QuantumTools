from setuptools import setup, find_packages

__version__ = '0.0'

setup(
    name='QuantumTools',
    version=__version__,
    description='',
    author='Dorye L. Esteras',
    author_email='dorye.esteras@uv.es',
    packages=['QuantumTools'],
    # scripts=[
    #     'scripts/tb2j_plotter.py'
    # ],
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)