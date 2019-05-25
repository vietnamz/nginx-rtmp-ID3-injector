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

import os
import json
from flask import Flask
from flask import make_response
from flask import request, Response
from id3v2tag_utils import *
from rtmp_utils import *

app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to NGTV AD API SERVER\n"

@app.route("/version")
def version():
    return "Welcome to NGTV AD API SERVER v1\n"

@app.route("/api")
def api():
    return "Welcome to NGTV AD API SERVER\n"

@app.route("/api/v1")
def apiV1():
    return "API V1\n"


@app.route("/api/v1/adSession", methods=["POST"])
def adInsertion1():
    req = request.get_json(silent=True, force=True)
    action = req.get("action")
    if action == "startAd":
        return format_response( insert_ads(req) )
    else:
        return format_response( { "result": "incomplete", 
            "displayText": "Please provide action type"} )


def format_response(res):
    res= json.dumps(res, indent = 4)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r


def insert_ads(req):
    ad_server = req.get("adServer")
    ad_name = req.get("adName")
    stream = req.get("stream")
    displayText = ""
    state = ""
    if ad_server == None and ad_name == None:
        displayText = "Please provide adServer and adName please!!!"
        state = "incomplete"
    if ad_server == None: 
        displayText = "Please provide the adServer Please!!!"
        state = "incomplete"
    elif ad_name == None:
        displayText = "Please provide the adName Please!!!"
        state = "incomplete"
    elif stream == None:
        displayText = "Please provide the stream ID you want to insert"
        state = "incomplete"
    else:
        url = "{}".format("/".join((ad_server,ad_name))) #FIXME
        adID = "adID" # description
        id3tag = generate_txxx(adID,url)
        if  id3tag is not None:
            rt, displayText = inject(stream, id3tag)    
            if rt == 0:
                state = "complete"
            else:
                state = "incomplete"

        else:
            state = "incomplete"
            displayText = "There is an error when generating id3v2tag"
    return {
        "result" : state,
        "displayText" : displayText
        }


if __name__ == "__main__":
    app.run(host='0.0.0.0')
