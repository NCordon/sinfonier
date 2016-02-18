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
        self.returninfo=self.getParam("returninfo")

    def userprocess(self):
        archivequery = self.getField(self.archivequery)
        returninfo=map(str,(self.getField(self.returninfo)))



        try:
            query = "https://archive.org/advancedsearch.php?q=" + archivequery

            for param in returninfo:
                query = query + "&fl[]=" + param

            query = query + "&output=json"

            t = requests.get(query).text
            data = json.loads(t)["response"]

            self.addField("response", data)

        except Exception,e:
            addField("status", "error")
            addField("exception", str(e))

        self.emit()

    def userclose(self):

        pass

GetInfoArchive().run()
