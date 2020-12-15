from pathlib import Path
from warnings import warn
import typing

from UniGrammarRuntime.ParserBundle import ParserBundle

_thisDir = Path(__file__).parent

bundleDir = _thisDir / "parserBundle"
bundle = ParserBundle(bundleDir)
grammar = bundle.grammars["fulling_motor_name"]
wrapper = grammar.getWrapper("antlr4")


def decodeShaftsCount(letter: str) -> int:
	return ord(letter.upper()) - ord("A") + 1

from icecream import ic

def _decodeParsed(p) -> dict:
	res = {}
	res["size"] = int(p.size)
	tpd = p.typed
	series = tpd.__class__.__name__[:-2]
	res["type"] = series
	#
	m = tpd.type_marker

	def processSuffix(stepsLower: typing.Optional[int] = None):
		sfx = tpd.suffix
		if sfx:
			sb = sfx.suffix_body
			try:
				# current_rated	current_peak_max 	current_per_phase	current_unloaded
				res["current_per_phase"] = int(sb.current) / 10 ** (len(sb.current) - 1)
			except AttributeError:
				st = sb
			else:
				st = sb.tail

			res["variant"] = int(st.variant)
			res["encoder"] = bool(st.encoder)
			res["key_way"] = bool(st.key_way)
			res["screwed_shaft"] = bool(st.screwed_shaft)
			res["unknown_F"] = bool(st.unknown_F)
			res["hollow"] = bool(st.hollow)

			scsr = st.shafts_count_and_step_rate_any_order
			if scsr.shafts_count:
				res["shafts_count"] = decodeShaftsCount(scsr.shafts_count)
				if stepsLower is not None:
					res["steps_per_revolution"] = stepsLower * 2 if scsr.step_rate else stepsLower

			if st.gearbox:
				res["gearbox"] = float(st.gearbox.ratio)
			else:
				res["gearbox"] = None

	#res[series] = True
	if series == "brushless":
		for k in m.__slots__:
			if getattr(m, k):
				res[k[3:]] = True

		modifier = tpd.modifier

		try:
			res["motor_body_length"] = int(modifier.motor_body_length)
		except AttributeError:
			res["poles_or_other"] = modifier.poles_or_other  # usually determines count of poles, A models have more poles (usually 10) than non-lettered models (usually 8), B models have more poles (usually 6) than non-lettered models, but some B models have no A analogues and have 8 poles and C models usually have no analogues and also have 8 poles. 
			res["variant"] = int(modifier.variant)
		else:
			if modifier.tail:  # ToDo: from the parsed ones I see no tail
				try:
					res['electronics'] = bool(modifier.tail.has_electronics)
				except AttributeError:
					cfg = modifier.tail
				else:
					cfg = modifier.tail.cfg
			else:
				cfg = None

			if cfg:
				unit2Name = {
					"V": 'voltage',
					"A": "current"
				}
				
				quantityKeyName = unit2Name[cfg.unit] + "_rated"
				res[quantityKeyName] = int(cfg.number)

	elif series == "stepper":
		res["motor_body_length"] = int(tpd.motor_body_length)
		markers = {
			None: "standard",
			"T": "standard",
			'H': "hybrid"
		}
		res["series"] = markers[m.series]

		if tpd.stepper_modifiers:
			modifiers = {
				'H': {"high_torque": True},
				'C': {"hyper_torque": True},
			}
			res.update(modifiers[tpd.stepper_modifiers])

		processSuffix(200)
		
	elif series == "permanent":
		res["motor_body_length"] = int(tpd.motor_body_length)
		processSuffix(None) # usually stepsLower=20, but not always
	elif series == "three_phase":
		res["motor_body_length"] = int(tpd.motor_body_length)
		sfx = tpd.suffix
		if sfx:
			res["current_per_phase"] = int(sfx.current_per_phase_over_ten) / 10
			if sfx.leads:
				res["input_count"] = int(sfx.leads)
			if sfx.shafts_count:
				res["shafts_count"] = decodeShaftsCount(sfx.shafts_count)

	else:
		raise ValueError(series)


	steps = res.get("steps_per_revolution", None)
	if steps:
		res['angle_step'] = 360 / steps

	for shapeType in ("round", "square"):
		if res.get(shapeType, None):
			del res[shapeType]
			res["shape"] = shapeType

	return res

def decodeModel(s: str) -> dict:
	p = wrapper(s)
	#print(p)
	return _decodeParsed(p)
