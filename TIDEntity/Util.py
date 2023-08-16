import nvector as nv
import collections.abc
from dotdict import dotdict
from math import *
from pygame import math, sprite, Surface, draw, SRCALPHA, font
wgs84 = nv.FrameE(name='WGS84')
OWN_AC = math.Vector2(200,390)
TID_RANGE_VALUES = [25, 50, 100, 200, 400]

EL_BARS_VALUES = [2.3, 3.6, 6.3, 11.5]
EL_CONTROL_RANGE = [-76, 54]
EL_CONTROL_MIN = -76
EL_CONTROL_MAX = 54
AZ_SCAN_VALUES = [10, 20, 40, 65]
AZ_CONTROL_RANGE = [-66, 66]
AZ_CONTROL_MIN = -65
AZ_CONTROL_MAX = 65

def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in overrides.items():
        if isinstance(value, collections.abc.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source

def BRAA(OWNSHIP, track):
    pointA = wgs84.GeoPoint(latitude=OWNSHIP.lat,longitude=OWNSHIP.lon, z=OWNSHIP.alt/3.281, degrees=True)
    pointB = wgs84.GeoPoint(latitude=track.lat, longitude=track.lon, z=track.alt/3.281, degrees=True)
    p_AB_N = pointA.delta_to(pointB)
    rng, azi1, azi2 = pointA.distance_and_azimuth(pointB)
    return dotdict({"brg": p_AB_N.azimuth_deg, "rng": rng/1852, "alt": track.alt, "asp": ((azi1 - 180) - track.hdg) % 180})

def BULLS(BULLSEYE, track):
    pointA = wgs84.GeoPoint(latitude=BULLSEYE.lat, longitude=BULLSEYE.longitude, z=0,  degrees=True)
    pointB = wgs84.GeoPoint(latitude=track.lat, longitude=track.lon, z=track.alt/3.281, degrees=True)
    p_AB_N = pointA.delta_to(pointB)
    rng, azi1, azi2 = pointA.distance_and_azimuth(pointB)
    return dotdict({"brg": p_AB_N.azimuth_deg, "rng": rng/1852, "alt": track.alt})

def angle_diff(b1, b2):
	r = (b2 - b1) % 360.0
	# Python modulus has same sign as divisor, which is positive here,
	# so no need to consider negative case
	if r >= 180.0:
		r -= 360.0
	return r
    
def mag(deg):
    return (270 + deg) % 360
