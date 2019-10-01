from setuptools import setup

package_name = 'sound_system'

setup(
    name=package_name,
    version='0.0.1',
    packages=[],
    py_modules=[
        'sound_system'
    ],
    install_requires=['setuptools'],
    data_files=[
        ('lib/' + package_name, ['package.xml']),
        ('lib/' + package_name+'/module',
         ['module/module_pico.py',
          'module/module_follow.py',
          'module/module_take.py',
          'module/module_arm.py',
          'module/module_make_map.py',
          'module/module_beep.py'
          ]),
        ('lib/sound_system/dictionary/',
         ['dictionary/yes_no.dict',
          'dictionary/yes_no.gram',
          'dictionary/follow_me.dict',
          'dictionary/follow_me.gram',
          'dictionary/take_bag.dict',
          'dictionary/take_bag.gram',
          'dictionary/map_test.dict',
          'dictionary/map_test.gram'
          ]),
        ('lib/sound_system/beep/',
         ['beep/speech.wav',
          'beep/start.wav',
          'beep/stop.wav'
          ]),
        ('lib/sound_system/log',
            ['log/log.txt'])
    ],
    zip_safe=True,
    author='HiroseChihiro',
    author_email='rr0111fx@ed.ritsumei.ac.jp',
    maintainer='ItoMasaki,MatsudaYamto',
    maintainer_email='is0449sh@ed.ritsumei.ac.jp,is0476hv@ed.ritsumei.ac.jp',
    keywords=['ROS2'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='sound package for SPR',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sound_system = sound_system:main',
        ],
    },
)
