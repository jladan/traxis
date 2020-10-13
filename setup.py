from setuptools import setup, find_packages

import traxis

setup(
    name='traxis',
    version=traxis.__version__,
    url='https://gitlab.physics.utoronto.ca/advanced-lab/traxis',
    author='Syed Haider Abidi, Nooruddin Ahmed, Christopher Dydul',
    maintainer='David Bailey',
    maintainer_email='dbailey@physics.utoronto.ca',
    # Package info
    packages=find_packages(),
    install_requirements=['numpy', 'scipy', 'qt'],
    package_data={
        "": ["README.md", '*.png']
    },
    license='GPL3',
    description='An application to measure bubble-chambre images for the UofT advanced physics lab.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    scripts=['runtraxis'],
    entry_points={
        "gui_scripts": [
            "traxis = traxis.__main__:main"
        ]
    }, 
)
