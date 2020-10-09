#!/bin/bash

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

name=${TEST_TARGET_NAME}
TEST_TIMEOUT=${TEST_TIMEOUT}

if [[ ${name}"x" == "x" ]]; then
    echo "can't find ${name}, please set ${TEST_TARGET_NAME} first"
    exit 1
fi

if [[ ${TEST_TIMEOUT}"x" == "x" ]]; then
    echo "can't find ${TEST_TIMEOUT}, please set ${TEST_TIMEOUT} first"
    exit 1
fi

# rm flag file
rm -f "${name}"_*.log

# start the unit test
run_time=$(( TEST_TIMEOUT - 10 ))
echo "run_time: ${run_time}"

timeout -s SIGKILL ${run_time} "${PYTHON_EXECUTABLE}" -u "${name}.py" > "${name}_run.log" 2>&1
exit_code=$?

echo "${name} faild with ${exit_code}"
if [[ $exit_code -eq 0 ]]; then
    exit 0
fi

echo "${name} log"
for log in ./"${name}"_*.log
do
    printf "\ncat %s\n", "${log}"
    cat -n "${log}"
done

exit 1
