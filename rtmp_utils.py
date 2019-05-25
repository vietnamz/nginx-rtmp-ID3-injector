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

from librtmp.rtmp import RTMP
from librtmp.packet import RTMPPacket, PACKET_TYPE_INVOKE, PACKET_SIZE_MEDIUM
from librtmp.amf import encode_amf
from librtmp.exceptions import *
from id3v2tag_utils import *
import os

DEFAULT_STREAM = "rtmp://localhost:1935/hls" #FIXME, this should come from env in container.
def inject(stream, id3tag):
	state = 0
	text = "Injected Successful"
	url_prefix = os.getenv("STREAM_URL", "")
	if url_prefix == "":
		url_prefix = DEFAULT_STREAM
	try:
		stream_url = "/".join((url_prefix , stream))
		conn = RTMP(stream_url, live=True)
		conn.connect()
		method = "onIDTag3v2" # Define in nginx-rtmp too
		# encode the new method
		method_encoded = encode_amf(method)
		# forward stream name
		stream = stream.encode()
		print ( stream )
		length = len(stream)
		print ( length )
		lenghtByte = length.to_bytes(2, 'little')
		stream = lenghtByte + stream
		# forward data byte
		length = len(id3tag)
		lenghtByte = length.to_bytes(2, 'little')
		id3tag = lenghtByte + id3tag
		body =  method_encoded + stream + id3tag
		packet = RTMPPacket(type=PACKET_TYPE_INVOKE, format=PACKET_SIZE_MEDIUM, channel=0x03, body=body)
		conn.send_packet(packet)
	except RTMPError as e:
		text = "{}".format(e)
		state = 1
	except RTMPTimeoutError as e:
		text = "{}".format(e)
		state = 1
	return state, text
	
if __name__ == "__main__":
	stream = "mystream"
	stream = "/".join((DEFAULT_STREAM,stream))
	print (stream)
	test_file = "test.id3"
	ad_server = "https://pubads.g.doubleclick.net"
	ad_test = 'gampad/ads?' + 'sz=640x480&iu=/124319096/external/single_ad_samples&ciu_szs=300x250&' + 'impl=s&gdfp_req=1&env=vp&output=vast&unviewed_position_start=1&' + 'cust_params=deployment%3Ddevsite%26sample_ct%3Dlinear&correlator='
	ad_server1 = "http://localhost"
	ad_test1 = "google_ads.xml"
	url = "{}".format("/".join((ad_server,ad_test)))
	adID = "adID"
	id3tag = generate_txxx(adID,url)
	print ( id3tag )
	length = len(id3tag)
	print (length)
	lenghtByte = length.to_bytes(2, 'little')
	print (lenghtByte)
	id3tag = lenghtByte + id3tag
	print(id3tag)

	state, text = inject(stream, id3tag)
	print (state, text)



