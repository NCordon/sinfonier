#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    The MIT License (MIT)

    Copyright (c) 2014 sinfonier-project

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""


import basesinfonierbolt
import datetime
import os
import requests
from lxml import html
import json
import re

class GetInfoArchive(basesinfonierbolt.BaseSinfonierBolt):

    def __init__(self):

        basesinfonierbolt.BaseSinfonierBolt().__init__()

    def userprepare(self):
        self.archivequery=self.getParam("archivequery")


    def userprocess(self):
        #location = str(self.getField("location"))
        archivequery = self.archivequery.replace(" ", "+")
        print archivequery
        try:
            query = "https://archive.org/advancedsearch.php?q=" + archivequery + "&fl[]=avg_rating&fl[]=call_number&fl[]=collection&fl[]=contributor&fl[]=coverage&fl[]=creator&fl[]=date&fl[]=description&fl[]=downloads&fl[]=external-identifier&fl[]=foldoutcount&fl[]=format&fl[]=headerImage&fl[]=identifier&fl[]=imagecount&fl[]=language&fl[]=licenseurl&fl[]=mediatype&fl[]=members&fl[]=month&fl[]=num_reviews&fl[]=oai_updatedate&fl[]=publicdate&fl[]=publisher&fl[]=related-external-id&fl[]=reviewdate&fl[]=rights&fl[]=scanningcentre&fl[]=source&fl[]=subject&fl[]=title&fl[]=type&fl[]=volume&fl[]=week&fl[]=year&sort[]=&sort[]=&sort[]=&rows=50&page=1&output=json&callback=callback&save=yes"
            t = requests.get(query).text

            t = t.replace("callback(","",1)[:-1]
            data = json.loads(t)["response"]

            self.addField("response", data)
        except Exception,e:
            addField("status", "error")
            addField("exception", str(e))

        self.emit()

    def userclose(self):

        pass

GetInfoArchive().run()
