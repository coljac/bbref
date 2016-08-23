from setuptools import setup
from setuptools import find_packages

setup(
        name='BBReference',
        version='0.1.0',
        py_modules=['bbref'],
        install_requires=['Click', 'texttable', 'pysqlite'],
        # packages=['bbref'],
        data_files=[('crp', ['./crp.db'])],
        # package_data={
            # 'bbref': ['data/crp.db'],
        # },
        # include_package_data=True,
        entry_points='''
        [console_scripts]
        bbref=bbref:cli
        '''
     )
