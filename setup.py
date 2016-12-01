from setuptools import setup, find_packages
import netmon
setup(
    name='netmon',
    packages=find_packages(),
    version=netmon.__version__,
    install_requires=['scapy', 'netifaces', 'ipaddress'],
    author="raf",
    description="Provide some network discovery functions",
    long_description=open('README.md').read(),
    include_package_data=True,
    url='https://github.com/rafBizos/netmon',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Communications",
    ],
    license="GNU")

