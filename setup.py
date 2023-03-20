from setuptools import setup, find_packages

import traxis

setup(
    name='traxis',
    version=traxis.__version__,
    url='https://gitlab.physics.utoronto.ca/advanced-lab/traxis',
    author='Syed Haider Abidi, Nooruddin Ahmed, Christopher Dydul',
    maintainer='John Ladan',
    maintainer_email='jladan@physics.utoronto.ca',
    # Package info
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'PyQt5'],
    package_data={
        "": ["README.md", '*.png']
    },
    license='GPL3',
    description='An application to measure bubble-chamber images for the UofT advanced physics lab.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    scripts=['runtraxis'],
    entry_points={
        "gui_scripts": [
            "traxis = traxis.__main__:main"
        ]
    }, 
)
