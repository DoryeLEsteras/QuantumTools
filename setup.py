from setuptools import setup, find_packages

__version__ = '0.0'

setup(
    name='QuantumTools',
    version=__version__,
    description='',
    author='Dorye L. Esteras',
    author_email='dorye.esteras@uv.es',
    packages=find_packages(),
    package_data={'QuantumTools':['*.cluster','kmesh.pl']},
    include_package_data=True,
    scripts=[
         'scripts/create_wannier.py',
         'scripts/create_bands.py',
         'scripts/create_projected.py',
         'scripts/create_charge_density.py',
         'scripts/create_spin_density.py',
         'scripts/create_bader.py',
         'scripts/create_work_function.py',
         'scripts/create_ft.py',
         'scripts/create_run.py',
         'scripts/create_template.py',
         'scripts/create_hubbard_scan.py',
         'scripts/create_updated_optimization.py',
         'scripts/create_cutoff_convergence.py',
         'scripts/create_kp_convergence.py',
         'scripts/extract_vasp_bands.py',
         'scripts/extract_repaired_bands.py',     
         'scripts/extract_fatbands.py',
         'scripts/extract_wan_h.py'
     ],
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
