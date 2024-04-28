# num2words for NVDA
# Author: Mateo Cedillo
# imports:
import globalPluginHandler
import globalCommands
from scriptHandler import script
import speech
from speech.priorities import Spri
from speech.speech import getCurrentLanguage
from speech.types import SpeechSequence
import config
import addonHandler
import ui
import globalVars
import gui
import wx
from gui import settingsDialogs
from .conversion_UI import ConversionDialog
from . import nvda_implementation
from .options import num2words_Settings

# default params and definitions:
speak_orig = None # speak object if num2words is disabled.
realtime = False # this determines whether or not to use the add-on's realtime mode while NVDA is speaking. This can be configured using the gesture set or the num2words settings panel.
language = "en"
# Speech OnDemand:
try:
	# NVDA >= 2024.1
	speech.speech.SpeechMode.onDemand
	speakOnDemand = {'speakOnDemand': True}
except AttributeError:
	# NVDA <= 2023.3
	speakOnDemand = {}

addonHandler.initTranslation()

# Set default Add-On settings:
confspec = {
	"enableOnStartup": "boolean(default=False)"
}
config.conf.spec["num2words"] = confspec

def switch_speak(speechSequence: SpeechSequence, priority: Spri = None):
	if realtime:
		return nvda_implementation.speak_mod(speechSequence=speechSequence, priority=priority)
	else:
		return speak_orig(speechSequence=speechSequence, priority=priority)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Translators: Add-on category name.
	scriptCategory = _("Number to words")
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		global realtime
		# Add num2words category to the NVDA settings panel.
		settingsDialogs.NVDASettingsDialog.categoryClasses.append(num2words_Settings)
		# detect if language is supported:
		if nvda_implementation.check_language(getCurrentLanguage()) == False:
			wx.CallLater(500, _lang_not_supported_MSG)
			return
		else:
			global speak_orig
			# original object when is disabled:
			speak_orig = nvda_implementation.speak_orig
			# replace the original speak object to the modified speak_mod func:
			speech._manager.speak = switch_speak
		# If the config to enable num2words on startup is enabled...
		if config.conf["num2words"]["enableOnStartup"]:
			realtime = True

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		global realtime
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(num2words_Settings)
		if realtime:
			realtime = False

	# GUI for conversion:
	def onConvert(self, evt):
		gui.mainFrame._popupSettingsDialog(ConversionDialog)

	# scripts:
	@script(
		# Translators: Description of the conversion of numbers to words in real time mode for input help.
		description=_("Switch reading from numbers to words."),
		category=globalCommands.SCRCAT_SPEECH,
		gesture=None,
		**speakOnDemand
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