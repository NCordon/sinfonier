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

class GetInfoOffer(basesinfonierbolt.BaseSinfonierBolt):

    def __init__(self):

        basesinfonierbolt.BaseSinfonierBolt().__init__()

    def userprepare(self):
        self.url=self.getParam("url")


    def userprocess(self):
        url = self.url

        # Extraemos los nombres de los trabajos y los enlaces
            # Simulando un navegador, ya que Linkedin por defecto no deja hacer
            # scraping a páginas personales
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        page = html.fromstring(requests.get(url, headers=headers).content)

        # Obtenemos la información de la oferta
        info = page.xpath('//code[@id="decoratedJobPostingModule"]/comment()')[0]
        enterprise = page.xpath('//code[@id="topCardV2Module"]/comment()')[0]

        # Creamos el json a partir del dicciolnario de ofertas
        info_json = json.loads(info.text)
        url_json = json.loads(enterprise.text)

        company_json = info_json['decoratedJobPosting']['decoratedCompany']

        self.addField("companyName", company_json['canonicalName'])
        self.addField("sector", company_json['formattedIndustries'])
        self.addField("desciption", [company_json['localizedDescription']])
        self.addField("offerViews", url_json["viewCount"])
        self.addField("registrationUrl", url_json["registrationUrl"])
        self.addField("companyLinkedin", url_json["companyPageNameLink"])
        self.emit()

    def userclose(self):

        pass

GetInfoOffer().run()
