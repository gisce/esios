# -*- coding: utf-8 -*-
from __future__ import absolute_import

from io import BytesIO
import zipfile
import json
import os.path
from lxml import etree, objectify
from lxml.etree import XMLSyntaxError
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pytz import timezone

from .archives import P48Cierre

_ROOT = os.path.abspath(os.path.dirname(__file__))

XSD_PATH = os.path.join(_ROOT, 'data')
CIERRE_XSD = ['urn-sios-ree-es-p48cierre-1-0.xsd', 'P48Cierre-esios-MP.xsd']
PROVISIONAL_XSD = ['urn-sios-ree-es-p48-1-0.xsd', 'P48-esios-MP.xsd']

LOCAL_TZ = timezone('Europe/Madrid')
UTC_TZ = timezone('UTC')


class P48CierreParser(P48Cierre):

    def get_filename(self):
        return 'p48cierre'

    def config_validators(self, pos):

        xmlschema_doc = etree.parse(os.path.join(XSD_PATH, CIERRE_XSD[pos]))
        xmlschema = etree.XMLSchema(xmlschema_doc)

        self.cierre_parser = objectify.makeparser(schema=xmlschema)

        xmlschema_doc = etree.parse(os.path.join(XSD_PATH, PROVISIONAL_XSD[pos]))
        xmlschema = etree.XMLSchema(xmlschema_doc)

        self.provisional_parser = objectify.makeparser(schema=xmlschema)

    def get_data_json(self, program_unit, start, end):
        res = self.download(start, end)
        return self.parse_to_json(res, program_unit)

    def get_data_json_from_file(self, program_unit, filepath):
        with open(filepath, 'rb') as filereader:
            res = filereader.read()
        return self.parse_to_json(res, program_unit)

    def parse_to_json(self, file_content, program_unit):
        """
        Returns a json from file. it may be a zip fail containing several fails (p48cierre or p48)
        :param content: the file content
        :param program_unit: The Program Unit to parse
        :return: a json list of dicts
        """
        for pos in [0, 1]:
            try:
                self.config_validators(pos)

                content = BytesIO(file_content)

                try:
                    zf = zipfile.ZipFile(content)
                    if zf.testzip() is None:
                        # Multiple files in one zip
                        zip_filenames = zf.namelist()
                except zipfile.BadZipfile as e:
                    # single file XML
                    result = self.parse_cierre(file_content, program_unit)
                    return json.dumps(result, default=str)

                data = []
                for filename in zip_filenames:
                    content = zf.read(filename)
                    data.extend(self.parse_cierre(content, program_unit))
                return json.dumps(data, default=str)
            except:
                # try old format if new fails
                continue

    def parse_cierre(self, content, program_unit):
        """
        Returns a list of registers , one per hour of the program_unit selected from de XML content.
        It validates de file previously
        :param content: XML to parse
        :param program_unit: Program unit to get
        :return: A list of registers:
        {
            "hour":             Hour in the XML field
            "up":               Program_unit: "SOMEC01",
            "value":            Float: Quantity of Energy programmed in MWh
            "cierre":           Boolean:
                                 * True: definitve close (past)
                                 * False: current day, no definitivo
            "utc_timestamp":    UTC timestamp of the register
            "local_timestamp":  Local timestamp calculated,
        },
        """
        is_cierre = self.is_cierre_type(content)

        # padrsing
        xmlobj = etree.XML(content)
        # Search UP
        e = xmlobj.xpath('//*[@v="{}"]'.format(program_unit))

        # SeriesTemporales Node
        st = e[0].getparent()
        # Periodo
        periodo = st[4]
        # Curve:
        curve = []
        for e in periodo:
            if 'IntervaloTiempo' in e.tag:
                value = e.get('v')
                start_str, end_str = value.split('/')
                start = UTC_TZ.localize(datetime.strptime(start_str, '%Y-%m-%dT%H:%MZ'))
                end = UTC_TZ.localize(datetime.strptime(end_str, '%Y-%m-%dT%H:%MZ'))
                # print("P48 for UP {} from {} to {}".format(program_unit, start, end))
            elif 'Intervalo' not in e.tag:
                continue
            else:
                hour = int(e[0].get('v'))
                value = float(e[1].get('v'))
                utc_timestamp = start + relativedelta(hours=hour)
                local_timestamp = LOCAL_TZ.normalize(utc_timestamp.astimezone(LOCAL_TZ))
                curve.append({
                    'up': program_unit,
                    'hour': hour,
                    'value': value,
                    'utc_timestamp': utc_timestamp,
                    'local_timestamp': local_timestamp,
                    'cierre': is_cierre,
                })

        return curve

    def is_cierre_type(self, content):
        """
        P48 contains 2 file types:
        * p48_cierreYYYYMMDD.xml: Definitve close (past)
        * p48_YYYYMMDDHH.xml:     Current day,
        Every file has diferent schema to be parsed
        :param content:
        :return: True: Cierre , False: Current day
        """
        try:
            objectify.fromstring(content, self.cierre_parser)
            return True
        except XMLSyntaxError as e:
            try:
                objectify.fromstring(content, self.provisional_parser)
                return False
            except XMLSyntaxError:
                raise e
