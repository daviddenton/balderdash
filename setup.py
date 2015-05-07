from distutils.core import setup

version = '0.1'
setup(
    name='forge',
    packages=['forge'],
    version=version,
    description='Monitoring dashboard generators',
    author='David Denton',
    author_email='denton.david+pypi@@gmail.com',
    url='https://github.com/daviddenton/forger',
    download_url='https://github.com/peterldowns/daviddenton/tarball/'+version,
    keywords=['dashboard', 'generator', 'kibana', 'grafana'],
    classifiers=[]
)