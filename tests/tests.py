#!/usr/bin/env python3
import csv
import itertools
import re
import sys
import unittest
from pathlib import Path

from parameterized import param, parameterized

thisDir = Path(__file__).parent

sys.path.insert(0, str(thisDir.parent))

from collections import OrderedDict

dict = OrderedDict

import FullingMotorModelDecoder
from FullingMotorModelDecoder import decodeModel


def tryIntoNum(v: str):
	try:
		return int(v)
	except ValueError:
		try:
			return float(v)
		except ValueError:
			return v


typeMapping = {
	"t": "three_phase",
	"b": "brushless",
	"p": "permanent",
	"s": "stepper",
}

stepperSeriesMapping = {
	"t": "standard",
	"h": "hybrid",
}

shapeMapping = {
	"s": "square",
	"r": "round",
	"sr1": "square with 1 rounded side",
}

boolsKeys = {"price_performance", "hybrid", "gyro", "encoder", "flat", "high_torque", "hyper_torque", "screwed_shaft", "key_way", "electronics"}


def decodeTsvRow(rd: dict) -> dict:
	res = {}
	res.update(rd)
	res["type"] = typeMapping[res["type"]]
	res["shape"] = shapeMapping[res["shape"]]

	if res["type"] == "stepper" and "series" in res:
		res["series"] = stepperSeriesMapping[res["series"]]

	res = {k: tryIntoNum(v) for k, v in res.items()}
	res = {k: (bool(v) if k in boolsKeys else v) for k, v in res.items()}
	res = {k: v for k, v in res.items() if v != "" and v is not None}

	if "angle_step" in res:
		res["steps_per_revolution"] = 360 / res["angle_step"]

	return res


def genTestCases():
	tests = list(csv.DictReader((thisDir / "motors.tsv").read_text().splitlines(), dialect=csv.excel_tab))
	for etalon in tests:
		#print("etalon tsv:", etalon)
		etalon = decodeTsvRow(etalon)
		#print("etalon:", etalon)
		modelName = etalon["name"]
		yield {"modelName": modelName, "etalon": etalon}


cases = genTestCases()


class Tests(unittest.TestCase):

	lengthIncons = None
	decodedProps = None

	@classmethod
	def setUpClass(cls):
		cls.lengthIncons = []
		cls.decodedProps = set()

	@classmethod
	def tearDownClass(cls):
		from icecream import ic

		ic(cls.lengthIncons)
		ic(cls.decodedProps)

	@parameterized.expand((param(**case) for case in cases), name_func=lambda func, num, param: func.__name__ + ":" + param.kwargs["modelName"])
	def testParse(self, modelName: str, etalon: dict):
		parsed = decodeModel(modelName)
		#print("parsed:", parsed)
		#print()
		self.__class__.decodedProps |= set(parsed)

		etalonCopy = type(etalon)(etalon)
		if "torque_rated" in etalonCopy:
			etalonCopy["torque_rated"] = round(etalonCopy["torque_rated"], 1)

		if "motor_body_length" in etalonCopy:
			etalonCopy["motor_body_length"] = round(etalonCopy["motor_body_length"])

		etalonSubDictDiff = {}
		parsedSubDictDiff = {}

		for k in sorted(set(parsed) | set(etalonCopy)):
			a = etalonCopy.get(k, None)
			b = parsed.get(k, None)

			if a is not None and b is not None and a != b:
				etalonSubDictDiff[k] = a
				parsedSubDictDiff[k] = b

		if "high_torque" in parsedSubDictDiff:
			#del etalonSubDictDiff["high_torque"]
			#del parsedSubDictDiff["high_torque"]
			self.__class__.lengthIncons.append((m, etalonSubDictDiff["high_torque"], parsedSubDictDiff["high_torque"]))

		relativeCurrentPerPhaseDeltaThreshold = 0.091
		if "current_per_phase" in parsedSubDictDiff:
			if abs(etalonSubDictDiff["current_per_phase"] - parsedSubDictDiff["current_per_phase"]) < etalonSubDictDiff["current_per_phase"] * relativeCurrentPerPhaseDeltaThreshold:
				del etalonSubDictDiff["current_per_phase"]
				del parsedSubDictDiff["current_per_phase"]

		relativeLengthDeltaThreshold = 0.12
		if "motor_body_length" in parsedSubDictDiff:
			if abs(etalonSubDictDiff["motor_body_length"] - parsedSubDictDiff["motor_body_length"]) < etalonSubDictDiff["motor_body_length"] * relativeLengthDeltaThreshold:
				del etalonSubDictDiff["motor_body_length"]
				del parsedSubDictDiff["motor_body_length"]

		self.assertEqual(etalonSubDictDiff, parsedSubDictDiff)


if __name__ == "__main__":
	unittest.main()
