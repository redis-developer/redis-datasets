from setuptools import setup, find_packages
import io


def read_all(f):
    with io.open(f, encoding="utf-8") as io_file:
        return io_file.read()


requirements = list(map(str.strip, open("requirements.txt").readlines()))


setup(
    name='redisgraph-bulk-loader',
    version='0.9.1',
    description='RedisGraph Bulk Import Tool',
    long_description=read_all("README.md"),
    long_description_content_type='text/markdown',
    url='https://github.com/redisgraph/redisgraph-bulk-loader',
    python_requires='>=3',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.0',
        'Topic :: Database'
    ],
    keywords='Redis Graph Extension',
    author='RedisLabs',
    author_email='oss@redislabs.com',

    entry_points='''
        [console_scripts]
        redisgraph-bulk-loader=redisgraph_bulk_loader.bulk_insert:bulk_insert
    '''
)
