# python setup.py --dry-run --verbose install

from distutils.core import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='pyNetatmoHue',
    version='0.1.2',
    classifiers=[        
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
        ],
    author='Steve de Peijper',
    author_email='steve.depeijper@gmail.com',
    py_modules=['pyNetatmoHue'],
    scripts=[],
    install_requires=['python-dateutil',
      ],
    data_files=[],
    url='https://github.com/stevedep/Netatmo_PPM_Hue',    
    license='GPL V3',
    description='Package that colours your lights as the PPM in your room change.',
    long_description=long_description,
    long_description_content_type="text/markdown"    
)
