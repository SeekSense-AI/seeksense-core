from setuptools import setup

package_name = 'seeksense_sim'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='M. Swalihu',
    maintainer_email='m.swalihu@hotmail.com',
    description='ROS2 integration client for SeekSense semantic search API (placeholder).',
    license='Proprietary',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'semantic_search_client = seeksense_sim.semantic_search_client:main',
        ],
    },
)