#   Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserved.
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

from paddle.fluid.layers import lod_rank_table, data
from paddle.fluid.executor import Executor
import paddle.fluid.core as core
import numpy
import unittest


class TestLoDRankTable(unittest.TestCase):
    def test_lod_rank_table(self):
        x = data(name='x', shape=[100])
        cpu = core.CPUPlace()
        rank_table = lod_rank_table(x=x, level=1)
        rank_table.persistable = True
        exe = Executor(cpu)
        scope = core.Scope()

        tensor = core.LoDTensor()
        tensor.set(numpy.random.random(size=(17, 100)), cpu)
        tensor.set_lod([[0, 1, 3], [0, 5, 6, 7], [0, 3, 4, 9, 10, 13, 16, 17]])
        exe.run(scope=scope, feed={'x': tensor})
        var = scope.find_var(rank_table.name)
        table = var.get_lod_rank_table()
        self.assertEqual([(0, 5), (1, 1), (2, 1)], table.items())


if __name__ == '__main__':
    unittest.main()
