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
# Since I always run and test code from scratchpad, it's important to enable translation if only if this is run as a standalone addon. Otherwise, there is an error message.
if not config.conf['development']['enableScratchpadDir']:
	addonHandler.initTranslation()

def convert_num_to_words(utterance, language):
	digits = re.findall(r'\d', utterance)
	if len(digits ) > 29:
		tones.beep(1200, 100)
		utterance =_(
			# Translators: Error message when the number is too big.
			_("The number is too big! twenty seven numbers maximum")
	)
	else:
		utterance = ' '.join([num2words.num2words(i ,lang=language) if i.isdigit() else i for i in utterance.split()])
		if not utterance[0].isupper():
			utterance = utterance.capitalize()
	return utterance

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
			new_item = convert_num_to_words(item, curLanguage)
			# for testing:
			#new_item = convert_num_to_words(item, "en")
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
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(
			wx.StaticText(
				self,
				# Translators: Label for the input box for the conversion.
				label=_("Write something here, example: 3 free throws")
			),
			0,
			wx.ALL,
			5
		)
		sizer.Add(self.input_text, 0, wx.EXPAND|wx.ALL, 5)
		sizer.Add(self.convert, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		sizer.Add(self.cancel, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		self.SetSizer(sizer)
		self.Bind(wx.EVT_BUTTON, self.onConvert, self.convert)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel)

		self.input_text.SetFocus()

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
			words = convert_num_to_words(to_convert, language)
			wx.MessageBox(
				words,
				# Translators: title of the conversion results dialog.
				_("Conversion results")
			)

	def OnCancel(self, event):
		self.Destroy()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Translators: Add-on category name.
	scriptCategory = _("Number to words")
	def __init__(self):
		super().__init__()
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