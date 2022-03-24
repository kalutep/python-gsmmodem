# -*- coding: utf8 -*-
import math
from .modem import GsmModem
from gsmmodem.util import lineMatching


class GPS:
    EarthRadius = 6371e3  # meters

    @staticmethod
    def calculate_delta_p(position1, position2):
        phi1 = position1.Latitude * math.pi / 180.0
        phi2 = position2.Latitude * math.pi / 180.0
        delta_phi = (position2.Latitude - position1.Latitude) * math.pi / 180.0
        delta_lambda = (position2.Longitude - position1.Longitude) * math.pi / 180.0

        a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(phi1) * math.cos(phi2) * math.sin(
            delta_lambda / 2) * math.sin(delta_lambda / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = GPS.EarthRadius * c  # in meters

        return d

    def __init__(self):
        self.GNSS_status = None
        self.Fix_status = None
        self.UTC = None  # yyyyMMddhhmmss.sss
        self.Latitude = None  # ±dd.dddddd            [-90.000000,90.000000]
        self.Longitude = None  # ±ddd.dddddd           [-180.000000,180.000000]
        self.Altitude = None  # in meters
        self.Speed = None  # km/h [0,999.99]
        self.Course = None  # degrees [0,360.00]
        self.HDOP = None  # [0,99.9]
        self.PDOP = None  # [0,99.9]
        self.VDOP = None  # [0,99.9]
        self.GPS_satellites = None  # [0,99]
        self.GNSS_satellites = None  # [0,99]
        self.Signal = None  # %      max = 55 dBHz

    def __str__(self):
        return 'GNSS_status: {}\nFix_status: {}\nUTC: {}\nLatitude: {}\nLongitude: {}\nAltitude: {}\nSpeed: {}\nCourse: {}\nHDOP: {}\nPDOP: {}\nVDOP: {}\nGPS_satellites: {}\nGNSS_satellites: {}\nSignal: {}'.format(
            str(self.GNSS_status), str(self.Fix_status), str(self.UTC), str(self.Latitude), str(self.Longitude),
            str(self.Altitude), str(self.Speed), str(self.Course), str(self.HDOP), str(self.PDOP), str(self.VDOP),
            str(self.GPS_satellites), str(self.GNSS_satellites), str(self.Signal))


class GnssModem(GsmModem):

    def gnssOn(self):
        return self.write('AT+CGNSPWR=1')[0]

    def gnssOff(self):
        return self.write('AT+CGNSPWR=0')[0]

    def gpsOn(self):
        return self.write('AT+CGNSTST=1')[0]

    def gpsOff(self):
        return self.write('AT+CGNSTST=1')[0]

    def getGpsData(self):
        copsMatch = lineMatching(
            '^\+CGNSINF: (\d),(\d),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),$',
            self.write('AT+CGNSINF'))  # response format: +COPS: mode,format,"operator_name",x
        if copsMatch:
            newGPS = GPS()
            try:
                newGPS.GNSS_status = int(copsMatch.group(1))
            except:
                newGPS.GNSS_status = None
            try:
                newGPS.Fix_status = int(copsMatch.group(2))
            except:
                newGPS.Fix_status = None
            try:
                newGPS.UTC = copsMatch.group(3)
            except:
                newGPS.UTC = None
            try:
                newGPS.Latitude = float(copsMatch.group(4))
            except:
                newGPS.Latitude = None
            try:
                newGPS.Longitude = float(copsMatch.group(5))
            except:
                newGPS.Longitude = None
            try:
                newGPS.Altitude = float(copsMatch.group(6))
            except:
                newGPS.Altitude = None
            try:
                newGPS.Speed = float(copsMatch.group(7))
            except:
                newGPS.Speed = None
            try:
                newGPS.Course = float(copsMatch.group(8))
            except:
                newGPS.Course = None
            try:
                newGPS.HDOP = float(copsMatch.group(11))
            except:
                newGPS.HDOP = None
            try:
                newGPS.PDOP = float(copsMatch.group(12))
            except:
                newGPS.PDOP = None
            try:
                newGPS.VDOP = float(copsMatch.group(13))
            except:
                newGPS.VDOP = None
            try:
                newGPS.GPS_satellites = int(copsMatch.group(15))
            except:
                newGPS.GPS_satellites = None
            try:
                newGPS.GNSS_satellites = int(copsMatch.group(16))
            except:
                newGPS.GNSS_satellites = None
            try:
                newGPS.Signal = float(copsMatch.group(19))
            except:
                newGPS.Signal = None

            return newGPS
