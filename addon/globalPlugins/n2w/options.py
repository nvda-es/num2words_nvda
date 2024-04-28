# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023-2024 Mateo Cedillo <angelitomateocedillo@gmail.com>
# This file is covered by the GNU General Public License.
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# Num2words options UI
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