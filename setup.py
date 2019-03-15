from setuptools import find_packages, setup

setup(
    name='django-grafana',
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    license='MIT License',
    description='Management app for Grafana',
    url='https://github.com/kfdm/django-grafana',
    author='Paul Traylor',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'pytz',
        'requests',
    ],
    entry_points={
        'powerplug.apps': ['grafana = grafana'],
        'powerplug.urls': ['grafana = grafana.urls'],
        'grafana.mutator': [
            'refresh = grafana.mutators.refresh:Refresh',
            'null = grafana.mutators.null:Null',
        ],
    },
)
