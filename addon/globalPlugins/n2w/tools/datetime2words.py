# date and time conversion.
# By: Mateo C.
import addonHandler
addonHandler.initTranslation()

# Translators: The twelve months of the year for date conversion.
months = [
	[1, _("January")],
	[2, _("February")],
	[3, _("March")],
	[4, _("Appril")],
	[5, _("May")],
	[6, _("June")],
	[7, _("July")],
	[8, _("August")],
	[9, _("September")],
	[10, _("October")],
	[11, _("November")],
	[12, _("December")]
]

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
			elif language == "uk":
				return f"{day} {months[mont-1][1]} {year} рік"
		elif format == 2:
			if not language == "uc":
				return f"{months[mont-1][1]} {day}, {year}"
			else:
				return f"{months[mont-1][1]} {day}, {year} рік"
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
		hour_str = str(hours) + " " + _("hours")
	if minutes == 0:
		min_str = ''
	elif minutes == 1:
		# Translators: Conversion message if is an one minute.
		min_str = _("one minute")
	else:
		# Translators: Conversion message if is several minutes.
		min_str = str(minutes) + " " + _("minutes")
	if seconds == 0:
		sec_str = ''
	elif seconds == 1:
		# Translators: Conversion message if is an one second.
		sec_str = _("one second")
	else:
		# Translators: Conversion message if is several seconds.
		sec_str = str(seconds) + " " + _("seconds")
	if min_str == '' and sec_str == '':
		return hour_str + " " + _("oclock")
	elif hour.count(':') == 1:
		return hour_str + " " + _("and") + " " + min_str
	else:
		return hour_str + ", " + min_str + " " + _("and") + " " + sec_str