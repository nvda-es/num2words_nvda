# Num2Words Monkey patches for the NVDA implementation:
from typing import Optional
import tones
import re
import os
import config
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'num2words'))
import num2words
import wx
import inputCore
import speech
from speech.speech import getCurrentLanguage, processText
from speech.commands import LangChangeCommand, CharacterModeCommand
from speech.types import SpeechSequence
from speech.priorities import Spri
from speech import manager
from logHandler import log
import addonHandler
addonHandler.initTranslation()

speak_orig = speech._manager.speak

def convert_num_to_words(
	utterance: str,
	language: str,
	to: Optional[str] = 'cardinal',
	ordinal: Optional[bool] = False,
	currency: Optional[str] = "EUR",
	**kwargs
):
	match = re.findall(r'[\d./]+', utterance)
	if len(match) > 0:
		if len(re.findall(r'\d{28,}', utterance)) > 0:
			tones.beep(1200, 100)
			utterance =_(
				# Translators: Error message when the number is too big.
				_("The number is too big! twenty seven numbers maximum")
			)
		else:
			# apply some text replacements to avoid decimal errors:
			utterance = utterance.replace("..", ".") # > 2 dots is considered a decimal error.
			if not to == "currency":
				utterance = ' '.join([num2words.num2words(m, ordinal=ordinal, lang=language, to=to) if m.replace('.', '').replace('/', '').isdigit() else m for m in re.split(r'([\d./]+)', utterance)])
			else:
				utterance = ' '.join([num2words.num2words(m, ordinal=ordinal, lang=language, to=to, currency=currency) if m.replace('.', '').replace('/', '').isdigit() else m for m in re.split(r'([\d./]+)', utterance)])

	if utterance and not utterance[0].isupper():
		utterance = utterance.capitalize()
	return utterance

# error message when language isn't supported:
def _lang_not_supported_MSG():
	wx.MessageBox(
		# Translators: Error message if the language is not supported by num2words.
		_("The language set in the speech synthesis is not supported by the num2words library. If you want to suggest or add this language, you can do it through the library repository: https://github.com/savoirfairelinux/num2words"),
		# Translators: Title of the error message.
		_("Error"),
		wx.ICON_ERROR
	)

#taken from num2words/num2words/__init__.py
def check_language(lang: str):
	if lang not in num2words.CONVERTER_CLASSES:
		# ... and then try only the first 2 letters
		lang = lang[:2]
	if lang not in num2words.CONVERTER_CLASSES:
		return False
	else:
		return lang

# function modified from NVDA source. (speech/speech.py)
def speak_mod(speechSequence: SpeechSequence,
		priority: Spri = None,
):
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