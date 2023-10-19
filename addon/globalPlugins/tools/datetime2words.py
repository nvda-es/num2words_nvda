# date and time conversion.
# By: Mateo C.
import addonHandler
addonHandler.initTranslation()

def convert_date(date, format, language="en"):
	"""
	We have two formats:
	1: dd/mm/yyyy
	2: mm/dd/yyyy
	"""
	parts = date.split('/')
	if len(parts) == 3:
		day = parts[0]
		mont = int(parts[1])
		year = parts[2]
		if format == 1:
			if language == "en":
				return f"{day} {months[mont-1][1]} {year}"
			elif language == "es":
				return f"{day} de {months[mont-1][1]} de {year}"
		elif format == 2:
			return f"{months[mont-1][1]} {day}, {year}"
	elif len(parts) == 2:
		day = parts[0]
		mont = int(parts[1])
		if format == 1:
			if language == "en":
				return f"{day} {months[mont-1][1]}"
			elif language == "es":
				return f"{day} de {months[mont-1][1]}"
		elif format == 2:
			return f"{months[mont-1][1]} {day}"
	# Translators: Message when the date is not valid.
	raise Exception(_("invalid date format"))

def convert_hour(hour):
	hours = int(hour.split(':')[0])
	minutes = int(hour.split(':')[1])
	seconds = 00
	if hour.count(':') == 2:
		seconds = int(hour.split(':')[2])
	# checks:
	if hours > 23 or minutes > 59 or seconds > 59:
		# Translators: Message when it is an invalid hour. I mean, out of range to 23:59:59
		raise Exception(_("Invalid hour!"))
	if hours == 1:
		# Translators: Conversion message if is an one hour.
		hour_str = _("one hour")
	else:
		# Translators: Conversion message if is several hours.
		hour_str = f'{hours} {_("hours")}'
	if minutes == 0:
		min_str = ''
	elif minutes == 1:
		# Translators: Conversion message if is an one minute.
		min_str = _("one minute")
	else:
		# Translators: Conversion message if is several minutes.
		min_str = f'{minutes} {_("minutes")}'
	if seconds == 0:
		sec_str = ''
	elif seconds == 1:
		# Translators: Conversion message if is an one second.
		sec_str = _("one second")
	else:
		# Translators: Conversion message if is several seconds.
		sec_str = f'{seconds} {_("seconds")}'
	if min_str == '' and sec_str == '':
		return f'{hour_str} {_("oclock")}'
	elif hour.count(':') == 1:
		return f'{hour_str} {_("and")} {min_str}'
	else:
		return f'{hour_str}, {min_str} {_("and")} {sec_str}'