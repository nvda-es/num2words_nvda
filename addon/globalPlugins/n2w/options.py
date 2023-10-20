# Num2words options UI
# By: Mateo C
# imports:
from gui import guiHelper
# To support future NVDA versions with API updates.
from gui.settingsDialogs import SettingsPanel
import wx
import config
import addonHandler

addonHandler.initTranslation()

class num2words_Settings(SettingsPanel):
	title = _("number to words")
	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.enableOnStartup = sHelper.addItem(wx.CheckBox(self, label=_("Enable the numbers to words conversion in real time on startup")))
		self.enableOnStartup.SetValue(config.conf["num2words"]["enableOnStartup"])

	def onSave(self):
		config.conf["num2words"]["enableOnStartup"] = self.enableOnStartup.GetValue()