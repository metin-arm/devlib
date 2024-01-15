#!/usr/bin/env python
#
#    Copyright 2024 ARM Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Module for testing different targets.
Forked from tests/test_target.py.
"""

import os
from unittest import TestCase
from devlib import AndroidTarget, LinuxTarget, LocalLinuxTarget, QEMULinuxTarget
from devlib.utils.misc import get_random_string

class TestReadTreeValues(TestCase):
    """ Class testing Target.read_tree_values_flat() """

    def test_read_multiline_values(self, target):
        """ Test Target.read_tree_values_flat() """
        method_name = self.__class__.test_read_multiline_values.__qualname__

        data = {
            'test1': '1',
            'test2': '2\n\n',
            'test3': '3\n\n4\n\n',
        }

        dirname = os.path.join(target.working_directory,
                               f'devlib-test-{get_random_string(12)}')
        print(f'{method_name}: creating {dirname}...')
        target.makedirs(dirname)

        for key, value in data.items():
            path = os.path.join(dirname, key)
            print(f'{method_name}: writing {value!r} to {path}...')
            target.write_value(path, value, verify=False, as_root=target.conn.connected_as_root)

        print(f'{method_name}: reading values from target...')
        raw_result = target.read_tree_values_flat(dirname)
        result = {os.path.basename(k): v for k, v in raw_result.items()}

        print(f'{method_name}: removing {dirname}...')
        target.remove(dirname)

        self.assertEqual({k: v.strip()
                          for k, v in data.items()},
                         result)


if __name__ == '__main__':
    a_target = AndroidTarget(connection_settings={'device': '0123456789A'},
                             working_directory='/data/local/tmp/devlib-target')
    print(f'{a_target.__class__.__name__}: {a_target.os}/{a_target.hostname}')
    TestReadTreeValues().test_read_multiline_values(a_target)
    print(f'{a_target.__class__.__name__}: removing {a_target.working_directory}...')
    a_target.remove(a_target.working_directory)

    l_target = LinuxTarget(connection_settings={'host': 'example.com',
                                                'username': 'username',
                                                'password': 'password'},
                           working_directory='/tmp/devlib-target')
    print(f'{l_target.__class__.__name__}: {l_target.os}/{l_target.hostname}')
    TestReadTreeValues().test_read_multiline_values(l_target)
    print(f'{l_target.__class__.__name__}: removing {l_target.working_directory}...')
    l_target.remove(l_target.working_directory)

    ll_target = LocalLinuxTarget(connection_settings={'unrooted': True},
                                 working_directory='/tmp/devlib-target')
    print(f'{ll_target.__class__.__name__}: {ll_target.os}/{ll_target.hostname}')
    TestReadTreeValues().test_read_multiline_values(ll_target)
    print(f'{ll_target.__class__.__name__}: removing {ll_target.working_directory}...')
    ll_target.remove(ll_target.working_directory)

    q_target = QEMULinuxTarget(kernel_image='/home/user/devlib/tools/buildroot/buildroot-aarch64-v2023.11.1/output/images/Image',
                               connection_settings={'host': '127.0.0.1',
                                                    'port': 8022,
                                                    'username': 'root',
                                                    'password': 'root',
                                                    'strict_host_check': False},
                               working_directory='/tmp/devlib-target')
    print(f'{q_target.__class__.__name__}: {q_target.os}/{q_target.hostname}')
    TestReadTreeValues().test_read_multiline_values(q_target)
    print(f'{q_target.__class__.__name__}: removing {q_target.working_directory}...')
    q_target.remove(q_target.working_directory)
    q_target.execute('poweroff')
