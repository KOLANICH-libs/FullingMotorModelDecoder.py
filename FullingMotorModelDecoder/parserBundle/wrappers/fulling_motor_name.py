import typing
from UniGrammarRuntime.IWrapper import IWrapper, IParseResult


class main(IParseResult):
	__slots__ = ("size", "typed")

	def __init__(self):
		self.size = None
		self.typed = None


class gearbox_specifier(IParseResult):
	__slots__ = ("ratio",)

	def __init__(self):
		self.ratio = None


class three_phase_t(IParseResult):
	__slots__ = ("type_marker", "motor_body_length", "suffix")

	def __init__(self):
		self.type_marker = None
		self.motor_body_length = None
		self.suffix = None


class three_phase_suffix_t(IParseResult):
	__slots__ = ("current_per_phase_over_ten", "leads", "shafts_count")

	def __init__(self):
		self.current_per_phase_over_ten = None
		self.leads = None
		self.shafts_count = None


class stepper_suffix_t(IParseResult):
	__slots__ = ("suffix_body",)

	def __init__(self):
		self.suffix_body = None


class suffix_with_current(IParseResult):
	__slots__ = ("current", "tail")

	def __init__(self):
		self.current = None
		self.tail = None


class shafts_count_and_step_rate_any_order_1_t(IParseResult):
	__slots__ = ("shafts_count", "step_rate")

	def __init__(self):
		self.shafts_count = None
		self.step_rate = None


class shafts_count_and_step_rate_any_order_2_t(IParseResult):
	__slots__ = ("step_rate", "shafts_count")

	def __init__(self):
		self.step_rate = None
		self.shafts_count = None


class stepper_suffix_tail(IParseResult):
	__slots__ = ("variant", "shafts_count_and_step_rate_any_order", "encoder", "unknown_F", "key_way", "screwed_shaft", "gearbox", "hollow")

	def __init__(self):
		self.variant = None
		self.shafts_count_and_step_rate_any_order = None
		self.encoder = None
		self.unknown_F = None
		self.key_way = None
		self.screwed_shaft = None
		self.gearbox = None
		self.hollow = None


class stepper_t(IParseResult):
	__slots__ = ("type_marker", "stepper_modifiers", "motor_body_length", "suffix")

	def __init__(self):
		self.type_marker = None
		self.stepper_modifiers = None
		self.motor_body_length = None
		self.suffix = None


class stepper_marker(IParseResult):
	__slots__ = ("series",)

	def __init__(self):
		self.series = None


class permanent_t(IParseResult):
	__slots__ = ("type_marker", "motor_body_length", "suffix")

	def __init__(self):
		self.type_marker = None
		self.motor_body_length = None
		self.suffix = None


class brushless_marker(IParseResult):
	__slots__ = ("is_price_performance", "is_round", "is_flat", "is_square", "is_unknown_C")

	def __init__(self):
		self.is_price_performance = None
		self.is_round = None
		self.is_flat = None
		self.is_square = None
		self.is_unknown_C = None


class execution_configuration_t(IParseResult):
	__slots__ = ("number", "unit")

	def __init__(self):
		self.number = None
		self.unit = None


class brushless_modifier_poles_torque(IParseResult):
	__slots__ = ("poles_or_other", "variant")

	def __init__(self):
		self.poles_or_other = None
		self.variant = None


class brushless_modifier_length_electronics_electrics(IParseResult):
	__slots__ = ("motor_body_length", "tail")

	def __init__(self):
		self.motor_body_length = None
		self.tail = None


class brushless_t(IParseResult):
	__slots__ = ("type_marker", "modifier")

	def __init__(self):
		self.type_marker = None
		self.modifier = None


class brushless_electronic_tail(IParseResult):
	__slots__ = ("has_electronics", "cfg")

	def __init__(self):
		self.has_electronics = None
		self.cfg = None


class mainParser(IWrapper):
	__slots__ = ()

	def process_main(self, parsed) -> main:
		rec = main()
		rec.size = self.backend.getSubTreeText(parsed.size)  # type: str
		rec.typed = self.process_type_specific(parsed.typed)  # type: typing.Union[stepper_t, permanent_t, brushless_t, three_phase_t]
		return rec

	def process_gearbox_specifier(self, parsed) -> gearbox_specifier:
		rec = gearbox_specifier()
		rec.ratio = self.backend.getSubTreeText(parsed.ratio)  # type: str
		return rec

	def process_type_specific(self, parsed) -> typing.Union[stepper_t, permanent_t, brushless_t, three_phase_t]:
		stepper = getattr(parsed, "stepper", None)
		if stepper is not None:
			return self.process_stepper_t(stepper)
		permanent = getattr(parsed, "permanent", None)
		if permanent is not None:
			return self.process_permanent_t(permanent)
		brushless = getattr(parsed, "brushless", None)
		if brushless is not None:
			return self.process_brushless_t(brushless)
		three_phase = getattr(parsed, "three_phase", None)
		if three_phase is not None:
			return self.process_three_phase_t(three_phase)
		raise TypeError(dir(parsed))

	def process_three_phase_t(self, parsed) -> three_phase_t:
		rec = three_phase_t()
		rec.type_marker = self.backend.getSubTreeText(parsed.type_marker)  # type: str
		rec.motor_body_length = self.backend.getSubTreeText(parsed.motor_body_length)  # type: str
		rec.suffix = self.process_three_phase_suffix_opt_our(getattr(parsed, "suffix", None))  # type: typing.Optional[three_phase_suffix_t]
		return rec

	def process_three_phase_suffix_opt_our(self, parsed) -> typing.Optional[three_phase_suffix_t]:
		return self.backend.enterOptional(parsed, self.process_three_phase_suffix_t)

	def process_three_phase_suffix_t(self, parsed) -> three_phase_suffix_t:
		rec = three_phase_suffix_t()
		rec.current_per_phase_over_ten = self.backend.getSubTreeText(parsed.current_per_phase_over_ten)  # type: str
		rec.leads = self.backend.getSubTreeText(parsed.leads)  # type: str
		rec.shafts_count = self.process_shafts_count_marker_opt_our(getattr(parsed, "shafts_count", None))  # type: typing.Optional[str]
		return rec

	def process_stepper_suffix_t(self, parsed) -> stepper_suffix_t:
		rec = stepper_suffix_t()
		rec.suffix_body = self.process_suffix_with_or_without_tail(parsed.suffix_body)  # type: typing.Union[suffix_with_current, stepper_suffix_tail]
		return rec

	def process_suffix_with_or_without_tail(self, parsed) -> typing.Union[suffix_with_current, stepper_suffix_tail]:
		with_current = getattr(parsed, "with_current", None)
		if with_current is not None:
			return self.process_suffix_with_current(with_current)
		without_current = getattr(parsed, "without_current", None)
		if without_current is not None:
			return self.process_stepper_suffix_tail(without_current)
		raise TypeError(dir(parsed))

	def process_suffix_with_current(self, parsed) -> suffix_with_current:
		rec = suffix_with_current()
		rec.current = self.backend.getSubTreeText(parsed.current)  # type: str
		rec.tail = self.process_stepper_suffix_tail(parsed.tail)  # type: stepper_suffix_tail
		return rec

	def process_double_step_rate_marker(self, parsed) -> typing.Optional[str]:
		return self.backend.enterOptional(parsed, self.backend.terminalNodeToStr)

	def process_encoder_presence_marker(self, parsed) -> typing.Optional[str]:
		return self.backend.enterOptional(parsed, self.backend.terminalNodeToStr)

	def process_unknown_marker_F(self, parsed) -> typing.Optional[str]:
		return self.backend.enterOptional(parsed, self.backend.terminalNodeToStr)

	def process_keyway_marker(self, parsed) -> typing.Optional[str]:
		return self.backend.enterOptional(parsed, self.backend.terminalNodeToStr)

	def process_screwed_shaft_marker(self, parsed) -> typing.Optional[str]:
		return self.backend.enterOptional(parsed, self.backend.terminalNodeToStr)

	def process_gearbox_specifier_opt_our(self, parsed) -> typing.Optional[gearbox_specifier]:
		return self.backend.enterOptional(parsed, self.process_gearbox_specifier)

	def process_hollow_specifier_opt_our(self, parsed) -> typing.Optional[str]:
		return self.backend.enterOptional(parsed, self.backend.getSubTreeText)

	def process_shafts_count_marker_opt_our(self, parsed) -> typing.Optional[str]:
		return self.backend.enterOptional(parsed, self.backend.getSubTreeText)

	def process_shafts_count_and_step_rate_any_order_1_t(self, parsed) -> shafts_count_and_step_rate_any_order_1_t:
		rec = shafts_count_and_step_rate_any_order_1_t()
		rec.shafts_count = self.process_shafts_count_marker_opt_our(getattr(parsed, "shafts_count", None))  # type: typing.Optional[str]
		rec.step_rate = self.process_double_step_rate_marker(getattr(parsed, "step_rate", None))  # type: typing.Optional[str]
		return rec

	def process_shafts_count_and_step_rate_any_order_2_t(self, parsed) -> shafts_count_and_step_rate_any_order_2_t:
		rec = shafts_count_and_step_rate_any_order_2_t()
		rec.step_rate = self.process_double_step_rate_marker(getattr(parsed, "step_rate", None))  # type: typing.Optional[str]
		rec.shafts_count = self.process_shafts_count_marker_opt_our(getattr(parsed, "shafts_count", None))  # type: typing.Optional[str]
		return rec

	def process_shafts_count_and_step_rate_any_order_t(self, parsed) -> typing.Union[shafts_count_and_step_rate_any_order_1_t, shafts_count_and_step_rate_any_order_2_t]:
		shafts_count_and_step_rate_any_order_1 = getattr(parsed, "shafts_count_and_step_rate_any_order_1", None)
		if shafts_count_and_step_rate_any_order_1 is not None:
			return self.process_shafts_count_and_step_rate_any_order_1_t(shafts_count_and_step_rate_any_order_1)
		shafts_count_and_step_rate_any_order_2 = getattr(parsed, "shafts_count_and_step_rate_any_order_2", None)
		if shafts_count_and_step_rate_any_order_2 is not None:
			return self.process_shafts_count_and_step_rate_any_order_2_t(shafts_count_and_step_rate_any_order_2)
		raise TypeError(dir(parsed))

	def process_stepper_suffix_tail(self, parsed) -> stepper_suffix_tail:
		rec = stepper_suffix_tail()
		rec.variant = self.backend.getSubTreeText(parsed.variant)  # type: str
		rec.shafts_count_and_step_rate_any_order = self.process_shafts_count_and_step_rate_any_order_t(parsed.shafts_count_and_step_rate_any_order)  # type: typing.Union[shafts_count_and_step_rate_any_order_1_t, shafts_count_and_step_rate_any_order_2_t]
		rec.encoder = self.process_encoder_presence_marker(getattr(parsed, "encoder", None))  # type: typing.Optional[str]
		rec.unknown_F = self.process_unknown_marker_F(getattr(parsed, "unknown_F", None))  # type: typing.Optional[str]
		rec.key_way = self.process_keyway_marker(getattr(parsed, "key_way", None))  # type: typing.Optional[str]
		rec.screwed_shaft = self.process_screwed_shaft_marker(getattr(parsed, "screwed_shaft", None))  # type: typing.Optional[str]
		rec.gearbox = self.process_gearbox_specifier_opt_our(getattr(parsed, "gearbox", None))  # type: typing.Optional[gearbox_specifier]
		rec.hollow = self.process_hollow_specifier_opt_our(getattr(parsed, "hollow", None))  # type: typing.Optional[str]
		return rec

	def process_stepper_modifiers_opt_our(self, parsed) -> typing.Optional[str]:
		return self.backend.enterOptional(parsed, self.backend.getSubTreeText)

	def process_stepper_t(self, parsed) -> stepper_t:
		rec = stepper_t()
		rec.type_marker = self.process_stepper_marker(parsed.type_marker)  # type: stepper_marker
		rec.stepper_modifiers = self.process_stepper_modifiers_opt_our(getattr(parsed, "stepper_modifiers", None))  # type: typing.Optional[str]
		rec.motor_body_length = self.backend.getSubTreeText(parsed.motor_body_length)  # type: str
		rec.suffix = self.process_stepper_suffix_t(parsed.suffix)  # type: stepper_suffix_t
		return rec

	def process_stepper_series_opt_our(self, parsed) -> typing.Optional[str]:
		return self.backend.enterOptional(parsed, self.backend.getSubTreeText)

	def process_stepper_marker(self, parsed) -> stepper_marker:
		rec = stepper_marker()
		rec.series = self.process_stepper_series_opt_our(getattr(parsed, "series", None))  # type: typing.Optional[str]
		return rec

	def process_permanent_t(self, parsed) -> permanent_t:
		rec = permanent_t()
		rec.type_marker = self.backend.getSubTreeText(parsed.type_marker)  # type: str
		rec.motor_body_length = self.backend.getSubTreeText(parsed.motor_body_length)  # type: str
		rec.suffix = self.process_stepper_suffix_t(parsed.suffix)  # type: stepper_suffix_t
		return rec

	def process_brushless_marker(self, parsed) -> brushless_marker:
		rec = brushless_marker()
		rec.is_price_performance = self.backend.getSubTreeText(parsed.is_price_performance)  # type: str
		rec.is_round = self.backend.getSubTreeText(parsed.is_round)  # type: str
		rec.is_flat = self.backend.getSubTreeText(parsed.is_flat)  # type: str
		rec.is_square = self.backend.getSubTreeText(parsed.is_square)  # type: str
		rec.is_unknown_C = self.backend.getSubTreeText(parsed.is_unknown_C)  # type: str
		return rec

	def process_execution_configuration_t(self, parsed) -> execution_configuration_t:
		rec = execution_configuration_t()
		rec.number = self.backend.getSubTreeText(parsed.number)  # type: str
		rec.unit = self.backend.getSubTreeText(parsed.unit)  # type: str
		return rec

	def process_brushless_modifier_variants(self, parsed) -> typing.Union[brushless_modifier_poles_torque, brushless_modifier_length_electronics_electrics]:
		poles_torque = getattr(parsed, "poles_torque", None)
		if poles_torque is not None:
			return self.process_brushless_modifier_poles_torque(poles_torque)
		length_electronics_electrics = getattr(parsed, "length_electronics_electrics", None)
		if length_electronics_electrics is not None:
			return self.process_brushless_modifier_length_electronics_electrics(length_electronics_electrics)
		raise TypeError(dir(parsed))

	def process_brushless_modifier_poles_torque(self, parsed) -> brushless_modifier_poles_torque:
		rec = brushless_modifier_poles_torque()
		rec.poles_or_other = self.backend.getSubTreeText(parsed.poles_or_other)  # type: str
		rec.variant = self.backend.getSubTreeText(parsed.variant)  # type: str
		return rec

	def process_brushless_modifier_length_electronics_electrics(self, parsed) -> brushless_modifier_length_electronics_electrics:
		rec = brushless_modifier_length_electronics_electrics()
		rec.motor_body_length = self.backend.getSubTreeText(parsed.motor_body_length)  # type: str
		rec.tail = self.process_brushless_tail_opt_our(getattr(parsed, "tail", None))  # type: typing.Optional[typing.Union[brushless_electronic_tail, execution_configuration_t]]
		return rec

	def process_brushless_tail_opt_our(self, parsed) -> typing.Optional[typing.Union[brushless_electronic_tail, execution_configuration_t]]:
		return self.backend.enterOptional(parsed, self.process_brushless_tail)

	def process_brushless_t(self, parsed) -> brushless_t:
		rec = brushless_t()
		rec.type_marker = self.process_brushless_marker(parsed.type_marker)  # type: brushless_marker
		rec.modifier = self.process_brushless_modifier_variants(parsed.modifier)  # type: typing.Union[brushless_modifier_poles_torque, brushless_modifier_length_electronics_electrics]
		return rec

	def process_brushless_tail(self, parsed) -> typing.Union[brushless_electronic_tail, execution_configuration_t]:
		electronic = getattr(parsed, "electronic", None)
		if electronic is not None:
			return self.process_brushless_electronic_tail(electronic)
		no_electronic = getattr(parsed, "no_electronic", None)
		if no_electronic is not None:
			return self.process_execution_configuration_t(no_electronic)
		raise TypeError(dir(parsed))

	def process_execution_configuration_opt_our(self, parsed) -> typing.Optional[execution_configuration_t]:
		return self.backend.enterOptional(parsed, self.process_execution_configuration_t)

	def process_brushless_electronic_tail(self, parsed) -> brushless_electronic_tail:
		rec = brushless_electronic_tail()
		rec.has_electronics = self.backend.getSubTreeText(parsed.has_electronics)  # type: str
		rec.cfg = self.process_execution_configuration_opt_our(getattr(parsed, "cfg", None))  # type: typing.Optional[execution_configuration_t]
		return rec

	__MAIN_PRODUCTION__ = process_main


__MAIN_PARSER__ = mainParser
