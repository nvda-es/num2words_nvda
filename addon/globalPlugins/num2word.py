# num2words for NVDA
# Author: Mateo Cedillo
# imports:
import globalPluginHandler
import globalCommands
from scriptHandler import script
import inputCore
import speech
from speech.speech import getCurrentLanguage, processText
from speech.commands import LangChangeCommand, CharacterModeCommand
from speech.types import SpeechSequence
from speech.priorities import Spri
from speech import manager
from logHandler import log
import config
import addonHandler
import tones
import ui
from typing import Optional
import globalVars
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'num2words'))
import num2words
import re
import gui, wx
# default params:
speak_orig = None # speak object if num2words is disabled.
realtime = False
language = "en"
# Since I always run and test this code from scratchpad, it's important to enable translation if only if this is run as a standalone addon. Otherwise, there is an error message.
if not config.conf['development']['enableScratchpadDir']:
	addonHandler.initTranslation()

# months definition, useful for date conversion
# Translators: the twelve months of the year for date conversion.
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

def convert_date(date, format):
	"""
We have two formats:
1: dd/mm/aaaa
2: mm/dd/aaaa
	"""
	parts = date.split('/')
	if len(parts) == 3:
		day = parts[0]
		mont = int(parts[1])
		year = parts[2]
		if format == 1:
			return f"{day} {months[mont-1][1]} {year}"
		elif format == 2:
			return f"{months[mont-1][1]} {day}, {year}"
	elif len(parts) == 2:
		day = parts[0]
		mont = int(parts[1])
		if format == 1:
			return f"{day} {months[mont-1][1]}"
		elif format == 2:
			return f"{months[mont-1][1]} {day}"
	raise Exception("invalid date format")

def convert_num_to_words(utterance, language, to='cardinal', ordinal=False, **kwargs):
	match = re.findall(r'[\d./]+', utterance)
	if len(match) > 0:
		if len(re.findall(r'\d{28,}', utterance)) > 0:
			tones.beep(1200, 100)
			utterance =_(
				# Translators: Error message when the number is too big.
				_("The number is too big! twenty seven numbers maximum")
			)
		else:
			utterance = ' '.join([num2words.num2words(m, ordinal=ordinal, lang=language, to=to) if m.replace('.', '').replace('/', '').isdigit() else m for m in re.split(r'([\d./]+)', utterance)])
	utterance = utterance.strip()
	if not utterance[0].isupper():
		utterance = utterance.capitalize()
	return utterance

# error message when language isn't supported:
def _lang_not_supported_MSG():
	wx.MessageBox(
		# Translators: Error message if the language is not supported by num2words.
		_("The language set in the speech synthesis is not supported by the num2words library. If you want to suggest or add this language, you can do it through the library repository: https://github.com/savoirfairelinux/num2words"),
		# Translators: Title of the error message.
		_("Error")
	)

#taken from num2words/num2words/__init__.py
def check_language(lang):
	if lang not in num2words.CONVERTER_CLASSES:
		# ... and then try only the first 2 letters
		lang = lang[:2]
	if lang not in num2words.CONVERTER_CLASSES:
		return False
	else:
		return lang

# function modified from NVDA source. (speech/speech.py)
def speak_mod(speechSequence: SpeechSequence,
		priority: Spri = None
):
	global realtime
	if not realtime:
		return speak_orig(speechSequence=speechSequence, priority=priority)
	import speechViewer
	if speechViewer.isActive:
		speechViewer.appendSpeechSequence(speechSequence)
	autoLanguageSwitching=config.conf['speech']['autoLanguageSwitching']
	autoDialectSwitching=config.conf['speech']['autoDialectSwitching']
	curLanguage=defaultLanguage=getCurrentLanguage()
	prevLanguage=None
	defaultLanguageRoot=defaultLanguage.split('_')[0]
	converted_speechSequence=[]
	for item in speechSequence:
		if isinstance(item,LangChangeCommand):
			if not autoLanguageSwitching: continue
			curLanguage=item.lang
			if not curLanguage or (not autoDialectSwitching and curLanguage.split('_')[0]==defaultLanguageRoot):
				curLanguage=defaultLanguage
		elif isinstance(item,str):
			if autoLanguageSwitching and curLanguage!=prevLanguage:
				converted_speechSequence.append(LangChangeCommand(curLanguage))
				prevLanguage=curLanguage
			# Aplying number to words to synthesizer language:
			new_item = convert_num_to_words(utterance=item, language=curLanguage)
			# for testing:
			#new_item = convert_num_to_words(utterance=item, language="en")
			converted_speechSequence.append(new_item)
		else:
			converted_speechSequence.append(item)
	inputCore.logTimeSinceInput()
	log.io("Speaking %r" % converted_speechSequence)
	curLanguage=defaultLanguage
	for index in range(len(converted_speechSequence)):
		item=speechSequence[index]
		if autoLanguageSwitching and isinstance(item,LangChangeCommand):
			curLanguage=item.lang
	speak_orig(speechSequence = converted_speechSequence, priority = priority)

class ConversionDialog(wx.Dialog):
	def __init__(self, parent):
		super(ConversionDialog, self).__init__(
			parent=parent,
			# Translators: Name of the conversion dialog.
			title=_("Convert number to words")
		)
		# declare:
		self.use_ordinal_only=False
		self.mode=0
		self.write_label = wx.StaticText(
			self,
			# Translators: Label for the input box for the conversion.
			label=_("Write something here, example: 3 free throws")
		)

		self.input_text = wx.TextCtrl(self)
		self.convert = wx.Button(
			self,
			# Translators: Label for the conversion button.
			label=_("Convert")
		)
		self.cancel = wx.Button(
			self,
			# Translators: Label for the button to cancel the conversion.
			label=_("Cancel")
		)
		self.ordinal = wx.CheckBox(
			self,
			# Translators: label for the checkbox to convert to ordinals.
			label=_("Ordinal mode")
		)
		self.conversion_label = wx.StaticText(
			self,
			# Translators: label for the combo box to choose the conversion mode.
			label=_("Choose conversion mode:")
		)
		self.conversion_mode = wx.Choice(
			self,
			# Translators: Options to choose the conversion mode that numbers to words supports. There are five modes:
			choices=[
				_("None"),
				_("cardinal"),
				_("Ordinal"),
				_("Ordinal number"),
				_("date"),
				_("Year"),
				_("Currency")
			]
		)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.write_label, 0, wx.ALL, 5)
		sizer.Add(self.input_text, 0, wx.EXPAND|wx.ALL, 5)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(self.conversion_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		hbox.Add(self.conversion_mode, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		sizer.Add(hbox, 0, wx.EXPAND|wx.ALL, 5)
		sizer.Add(self.ordinal, 0, wx.ALL, 5)
		sizer.Add(self.convert, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		sizer.Add(self.cancel, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		self.SetSizer(sizer)
		self.Bind(wx.EVT_CHECKBOX, self.onOrdinal, self.ordinal)
		self.Bind(wx.EVT_CHOICE, self.onConversion_mode, self.conversion_mode)
		self.Bind(wx.EVT_BUTTON, self.onConvert, self.convert)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel)
		self.Bind(wx.EVT_CHAR_HOOK, self.accel_keys)
		# set default parametters:
		self.conversion_mode.SetSelection(0)
		self.input_text.SetFocus()
		# set acceleator keys:
		self.SetEscapeId(self.cancel.GetId())

	def onOrdinal(self, event):
		self.use_ordinal_only = event.IsChecked()
		self.conversion_mode.Enable(not event.IsChecked())

	def onConversion_mode(self, event):
		self.mode = self.conversion_mode.GetSelection()

	def onConvert(self, event):
		to_convert = self.input_text.GetValue()
		if not to_convert :
			wx.MessageBox(
				# Translators: Error message when there is nothing to convert.
				_("there's nothing to convert"),
				# Translators: Title of the error message.
				_("Error")
			)
		else:
			language = getCurrentLanguage() # based on the synthesizer language
			# supported modes:
			if self.mode == 0 or self.mode == 1:
				conversion_type = "cardinal"
			elif self.mode == 2:
				conversion_type = "ordinal"
			elif self.mode == 3:
				conversion_type = "ordinal_num"
			elif self.mode == 4:
				conversion_type = "date" # custom mode
			elif self.mode == 5:
				conversion_type = "year"
			elif self.mode == 6:
				conversion_type = "currency"
			# convert:
			if not conversion_type == "date":
				words = convert_num_to_words(
					utterance=to_convert,
					ordinal=self.use_ordinal_only,
					language=language,
					to=conversion_type
				)
			else:
				words = convert_date(to_convert, 1)
				words = convert_num_to_words(
					utterance=words,
					ordinal=self.use_ordinal_only,
					language=language,
					to="year"
				)
			wx.MessageBox(
				words,
				# Translators: title of the conversion results dialog.
				_("Conversion results")
			)

	def OnCancel(self, event):
		self.Destroy()

	def accel_keys(self, event):
		keycode = event.GetKeyCode()
		if keycode == wx.WXK_ESCAPE:
			self.OnCancel(event)
		else:
			event.Skip()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Translators: Add-on category name.
	scriptCategory = _("Number to words")
	def __init__(self):
		super().__init__()
		# detect if language is supported:
		if check_language(getCurrentLanguage()) == False:
			wx.CallLater(500, _lang_not_supported_MSG)
			return
		else:
			global speak_orig
			# original object when is disabled:
			speak_orig = speech._manager.speak
			# replace the original speak object to the modified speak_mod func:
			speech._manager.speak = speak_mod

	# GUI for conversion:
	def onConvert(self, evt):
		gui.mainFrame._popupSettingsDialog(ConversionDialog)

	# scripts:
	@script(
		# Translators: Description of the conversion of numbers to words in real time mode for input help.
		description=_("Switch reading from numbers to words."),
		category=globalCommands.SCRCAT_SPEECH,
		gesture=None
	)
	def script_switch_num2word(self, gesture):
		global realtime
		if not realtime:
			# Translators: message announced when realtime mode is enabled.
			ui.message(_("Num2words enabled."))
			realtime = True
		else:
			# Translators: message announced when realtime mode is disabled.
			ui.message(_("Num2words disabled."))
			realtime = False

	@script(
		# Translators: Description of the manual conversion dialog for input help.
		description=_("Opens a dialog to convert number to words manually"),
		gesture="kb:alt+shift+NVDA+N"
	)
	def script_convertor(self, gesture):
		wx.CallAfter(self.onConvert, None)