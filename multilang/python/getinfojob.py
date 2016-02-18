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

class GetInfoJob(basesinfonierbolt.BaseSinfonierBolt):

    def __init__(self):

        basesinfonierbolt.BaseSinfonierBolt().__init__()

    def userprepare(self):
        self.job = self.getParam("job")
        self.location = self.getParam("location")


    def userprocess(self):
        location = str(self.getField(self.location))

        job = self.getField(self.job)
        place=""

        # Si location no está vacío definimos el lugar
        if location:
            place = "&location="+location


        # Queremos extraer el id
        get_locationid = re.compile("[^:]*\:[^:]*$")
        get_location = re.compile("locationId\"\:[^\}]*")


        try:
            query = "https://www.linkedin.com/jobs/search?keywords=" + job + place
            query_rseponse = requests.get(query)

            # Obtenemos el identificador (por ejemplo es:5086
            locationId = get_location.search(query_response.text).group(0)

            # Lo normalizamos
            locationId = locationId.replace('"','').replace("locationId:",'')
            start = 0
            scrap = True
            setOffers = True
            # Diccionario de ofertas
            offers={}

            while scrap:
                try:
                    query = "https://www.linkedin.com/jobs/search?keywords=" + job + '&locationId=' + locationId + '&start=' + str(start) + '&count=25'

                    # Extraemos los nombres de los trabajos y los enlaces
                    page = html.fromstring(requests.get(query).content)
                    offersNames = page.xpath('//span[@class="job-title-text"]/text()')
                    offersLinks = page.xpath('//a[@class="job-title-link"]/@href')


                    for name,link in zip(offersNames, offersLinks):
                        offers[name]=link

                    # Scrapearemos la siguiente página
                    start = start+25

                    if not offersNames:
                        scrap = False

                except Exception,e:
                    addField("status", "error")
                    addField("exception", str(e))
                    scrap = False
                    setOffers = False


            if setOffers:
                # Creamos el json a partir del dicciolnario de ofertas
                json_data = json.dumps(offers)
                self.addField("ofertas", offers)

        except Exception,e:
            addField("status", "error")
            addField("exception", str(e))

        self.emit()

    def userclose(self):

        pass

GetInfoJob().run()
