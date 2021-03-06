# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
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

from threading import Lock, Thread
import time
from utils import logger
from paddle_edl.discovery.etcd_client import EtcdClient
import json
import collections


class Watcher(object):
    def __init__(self, etcd_endpoints, job_id):
        self._etcd = EtcdClient(edl_env.etcd_endpoints, root=job_id)
        self._job_id = job_id
        self._changed = False

        # servers in etcd
        self._ranks = None  # {rank:pod_json}

        self._cluster = Cluster()
        self._lock = Lock()

    def watch(self):
        self._t_watcher = Threading(selt._watcher)
        self._t_watcher.start()

    def _watcher(self):
        begin = time.time()
        while True:
            servers = self._etcd._get_server("pod")
            ranks = {}
            with self._lock:
                for s in servers:
                    ranks[s.server] = s.info

                if self._ranks is None:
                    self._ranks = ranks
                    with self._lock:
                        self._cluster.from_json(ranks)
                else:
                    if self._is_rank_changed(self._ranks, ranks):
                        with self._lock:
                            self._changed = True
                        logger.info(
                            "train world changed, old  is {} new is {}",
                            self._ranks, ranks)
                        break

            time.sleep(1)

    def _is_rank_changed(self, old, new):
        for k, v in six.iteriterms(old):
            if v == new[k]:
                continue

            old_pod = Pod()
            old_pod.from_json(old[k])

            new_pod = Pod()
            new_pod.from_json(new[k])

            if new_pod != old_pod:
                return True

        return False

    def get_cluster(self):
        with self._lock:
            return self._cluster

    def is_changed(self):
        with self._lock:
            return self._changed

    def stop(self):
        self._stop.set()
        self._t_watcher.join()
