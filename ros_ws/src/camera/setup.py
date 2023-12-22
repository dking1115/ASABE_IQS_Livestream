from setuptools import setup
import os


package_name = 'camera'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name,os.path.join(package_name,"submodules")],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='david',
    maintainer_email='david@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_controller = camera.camera_controller:main'
        ],
    },
)
