# -*- coding: utf-8 -*-

import PIL.Image, uuid, os
from PIL.ExifTags import TAGS

import dateutil.parser as dp
from datetime import datetime as dt
import pytz

from app.utils.dict import filter_dict
from app.utils.dir import uuid2dir

class Photoupload:

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __init__(self, fn):
        self._img = PIL.Image.open(fn)
        self.tags = {}

        try:
            self.tags = ({TAGS[k]: v for k, v in self._img._getexif().items() if k in PIL.ExifTags.TAGS})
        except AttributeError:
            # pngs have no exif
            pass

    def __getattr__(self, key):
        """
        delegate any call to self._img
        https://stackoverflow.com/questions/5165317/how-can-i-extend-image-class
        """
        if key == "_img":
            raise AttributeError()
        return getattr(self._img, key)

    @staticmethod
    def __coord2dec(coord_ref, coord):
        dd, mm, ss = coord
        degrees, x = dd
        minutes, x = mm
        seconds, divider = ss
        seconds /= divider

        decimal = degrees + minutes/60 + seconds/3600

        modifier = -1 if coord_ref.lower() == 'w' or coord_ref.lower() == 's' else 1

        return decimal * modifier

    def get_latlon(self):
        try:
            lat = Photoupload.__coord2dec(self.tags["GPSInfo"][1], self.tags["GPSInfo"][2])
            lon = Photoupload.__coord2dec(self.tags["GPSInfo"][3], self.tags["GPSInfo"][4])

            return lat, lon
        except (KeyError, AttributeError):
            return None, None

    def get_created_human(self):
        """
        return datetime when photo was shot from GPS
        UTC time
        """
        try:
            hh, mm, ss = self.tags["GPSInfo"][7]
            h, x = hh
            m, x = mm
            s, x = ss
            d = self.tags["GPSInfo"][29]

            return "{date}T{h}:{m}:{s}Z".format(h=h, m=m, s=s, date=d.replace(":", "-"))
        except (KeyError, AttributeError):
            return None

    def get_created(self):
        """
        return seconds since epoch when photo was shot from GPS
        """
        ts = self.get_created_human()
        if ts:
            epoch = dt(1970, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
            return str(round((dp.parse(ts) - epoch).total_seconds()))
        else:
            return None

    def save(self):
        # print("*"*10, self._img.filename)
        id = str(uuid.uuid4())
        data = {"id": id}
        ending = self._img.format.lower()
        destdir = uuid2dir(id)

        lat, lon = self.get_latlon()
        if (lat and lon):
            data["lat"] = round(lat, 4)
            data["lon"] = round(lon, 4)
            # data["geometry"] = {"type": "Point", "coordinates": [round(elem, 4) for elem in [lat, lon]]}

        for tag in ["created", "created_human"]:
            tag_data = getattr(self, "get_"+tag)()
            if tag_data:
                data[tag] = tag_data

        # physically save it
        if not os.path.exists(destdir):
            os.makedirs(destdir)

        dest = os.path.join(destdir, "{id}.orig.{ending}".format(id=id, ending=ending))
        data["url"] = os.path.join("/", dest)
        self._img.save(dest)

        if os.path.isfile(dest):
            return data
        else:
            return False

