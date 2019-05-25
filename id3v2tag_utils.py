# Copyright 2017 delgemoon Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import stagger
from stagger.id3 import *

#There is no error should occur here

def generate_txxx(adId, value):
	txxx_frame = stagger.id3.TXXX(encoding=0, description=adId, value=value)
	tag_v3 = stagger.Tag23()
	tag_v3[TXXX] = txxx_frame
	tag_v3.padding_max = 0
	tag_v3.padding_default = 0
	id3tagv2 = None
	id3tagv2 = tag_v3.encode()
	return id3tagv2


if __name__  == "__main__":
	adId = "http://localhost"
	value = "test/ad0"

	id3tagv2 = generate_txxx(adId, value)
	if id3tagv2 is not None:
		print ( id3tagv2 )
	