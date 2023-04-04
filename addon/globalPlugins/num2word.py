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
import tones
import ui
from typing import Optional
import globalVars
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'num2words'))
import num2words
import gui, wx
# default params:
speak_orig = None # speak object if num2words is disabled.
num2word_enhabled = False
language = "en"

def convert_num_to_words(utterance, language):
	utterance = ' '.join([num2words.num2words(i ,lang=language) if i.isdigit() else i for i in utterance.split()])
	return utterance

# function modified from NVDA source. (speech/speech.py)
def speak_mod(speechSequence: SpeechSequence,
		priority: Spri = None
):
	global num2word_enhabled
	if not num2word_enhabled:
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
			# debugging num2words:
			print(f"Before: {item}")
			# Aplying number to words to synthesizer language:
			new_item = convert_num_to_words(item, curLanguage)
			# for testing:
			#new_item = convert_num_to_words(item, "en")
			print(f"After: {new_item}")
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
		super(ConversionDialog, self).__init__(parent=parent, title="Convert number to words")
		self.number_textbox = wx.TextCtrl(self)
		self.convert_button = wx.Button(self, label="Convert")
		self.cancel_button = wx.Button(self, label="Cancel")
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(wx.StaticText(self, label="Write something here, example: 3 free throws"), 0, wx.ALL, 5)
		sizer.Add(self.number_textbox, 0, wx.EXPAND|wx.ALL, 5)
		sizer.Add(self.convert_button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		sizer.Add(self.cancel_button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		self.SetSizer(sizer)
		self.Bind(wx.EVT_BUTTON, self.onConvert, self.convert_button)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel_button)

		self.number_textbox.SetFocus()

	def onConvert(self, event):
		number = self.number_textbox.GetValue()
		language = getCurrentLanguage() # based on the synthesizer language
		words = convert_num_to_words(number, language)
		wx.MessageBox(words, "Result")

	def OnCancel(self, event):
		self.Destroy()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = "Number to words"
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
		description="Switch reading from numbers to words.",
		category=globalCommands.SCRCAT_SPEECH,
		gesture=None
	)
	def script_switch_num2word(self, gesture):
		global num2word_enhabled
		if not num2word_enhabled:
			ui.message("Num2words enabled.")
			num2word_enhabled = True
		else:
			ui.message("Num2words disabled.")
			num2word_enhabled = False

	@script(
		description="Opens a dialog to convert number to words manually",
		gesture="kb:alt+shift+NVDA+N"
	)
	def script_convertor(self, gesture):
		wx.CallAfter(self.onConvert, None)