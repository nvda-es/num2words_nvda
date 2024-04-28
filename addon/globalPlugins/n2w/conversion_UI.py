# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023-2024 Mateo Cedillo <angelitomateocedillo@gmail.com>
# This file is covered by the GNU General Public License.
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# WX UI for manual conversion mode:

import wx
from speech.speech import getCurrentLanguage
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'num2words'))
import num2words
from .nvda_implementation import check_language
from .tools.datetime2words import convert_date, convert_hour
import addonHandler
addonHandler.initTranslation()


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
		self.currency = "EUR"
		self.thisLanguageHasCurrencies = False
		self.language = check_language(getCurrentLanguage()) # based on the synthesizer language
		self.currencies = list(num2words.CONVERTER_CLASSES[self.language].CURRENCY_FORMS.keys())
		if not self.currencies:
			self.currencies = [
				# Translators: message to inform the user that there is no type of currency to convert with this language.
				_("There are no currencies to convert for this language. Using default.")
			]
		else:
			self.thisLanguageHasCurrencies = True
		self.write_label = wx.StaticText(
			self,
			# Translators: Label for the input box for the conversion.
			label="&"+_("Write something here, example: 3 free throws")
		)

		self.input_text = wx.TextCtrl(self)
		self.convert = wx.Button(
			self,
			# Translators: Label for the conversion button.
			label="&"+_("Convert")
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
			label=_("Choose conversion &mode:")
		)
		self.conversion_mode = wx.Choice(
			self,
			# Translators: Options to choose the conversion mode that numbers to words supports. There are seven modes:
			choices=[
				_("None"),
				_("cardinal"),
				_("Ordinal"),
				_("Ordinal number"),
				_("Date"),
				_("Hour"),
				_("Year"),
				_("Currency")
			]
		)
		self.currencies_label = wx.StaticText(
			self,
			# Translators: label for the currency selection combo box.
			label=_("Select the currency to convert:")
		)
		self.select_currencies = wx.Choice(
			self,
			choices=self.currencies
		)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.write_label, 0, wx.ALL, 5)
		sizer.Add(self.input_text, 0, wx.EXPAND|wx.ALL, 5)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(self.conversion_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		hbox.Add(self.conversion_mode, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		hbox.Add(self.currencies_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		hbox.Add(self.select_currencies, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
		sizer.Add(hbox, 0, wx.EXPAND|wx.ALL, 5)
		sizer.Add(self.ordinal, 0, wx.ALL, 5)
		sizer.Add(self.convert, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		sizer.Add(self.cancel, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		self.SetSizer(sizer)
		self.Bind(wx.EVT_CHECKBOX, self.onOrdinal, self.ordinal)
		self.Bind(wx.EVT_CHOICE, self.onConversion_mode, self.conversion_mode)
		self.Bind(wx.EVT_CHOICE, self.onSelect_currencies, self.select_currencies)
		self.Bind(wx.EVT_BUTTON, self.onConvert, self.convert)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel)
		self.Bind(wx.EVT_CHAR_HOOK, self.accel_keys)
		# set default parametters:
		self.conversion_mode.SetSelection(0)
		if self.thisLanguageHasCurrencies:
			self.select_currencies.SetSelection(0)
		self.input_text.SetFocus()
		# by default, disabling currency controls:
		self.currencies_label.Disable()
		self.select_currencies.Disable()
		# set accelerator keys:
		self.SetEscapeId(self.cancel.GetId())

	def onOrdinal(self, event):
		self.use_ordinal_only = event.IsChecked()
		self.conversion_mode.Enable(not event.IsChecked())

	def onConversion_mode(self, event):
		self.mode = self.conversion_mode.GetSelection()
		if self.mode == 7:
			self.currencies_label.Enable()
			self.select_currencies.Enable()
		else:
			self.currencies_label.Disable()
			self.select_currencies.Disable()

	def onSelect_currencies(self, event):
		self.currency = self.select_currencies.GetStringSelection()

	def onConvert(self, event):
		words = None
		to_convert = self.input_text.GetValue()
		if not to_convert :
			wx.MessageBox(
				# Translators: Error message when there is nothing to convert.
				_("there's nothing to convert"),
				# Translators: Title of the error message.
				_("Error"),
				wx.ICON_ERROR
			)
		else:
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
				conversion_type = "hour" # custom mode
			elif self.mode == 6:
				conversion_type = "year"
			elif self.mode == 7:
				conversion_type = "currency"
			# convert:
			if conversion_type == "date":
				try:
					words = convert_date(to_convert, 1, self.language)
					words = convert_num_to_words(
						utterance=words,
						ordinal=self.use_ordinal_only,
						language=self.language,
						to="year"
					)
				except Exception as e:
					wx.MessageBox(
						# Translators: error message when it is an invalid date.
						_(str(e)),
						# Translators: Title of the error message.
						_("Conversion error"),
						wx.ICON_ERROR
					)
			elif conversion_type == "hour":
				if ":" in to_convert:
					try:
						words = convert_hour(to_convert)
						words = convert_num_to_words(
							utterance=words,
							ordinal=self.use_ordinal_only,
							language=self.language,
							to="cardinal"
						)
					except Exception as e:
						wx.MessageBox(
							# Translators: error message when the hour is invalid.
							_(str(e)),
							# Translators: Title of the error message.
							_("Conversion error"),
							wx.ICON_ERROR
						)
				else:
					wx.MessageBox(
						# Translators: Error message when a valid time is not given.
						_("This is not a valid hour format"),
						# Translators: Title of the error message.
						_("Conversion error"),
						wx.ICON_ERROR
					)
			else:
				words = convert_num_to_words(
					utterance=to_convert,
					ordinal=self.use_ordinal_only,
					language=self.language,
					to=conversion_type,
					currency=self.currency
				)
			if words is not None:
				wx.MessageBox(
					words,
					# Translators: title of the conversion results dialog.
					_("Conversion results")
				)
		return words

	def OnCancel(self, event):
		self.Destroy()

	def accel_keys(self, event):
		keycode = event.GetKeyCode()
		if keycode == wx.WXK_ESCAPE:
			self.OnCancel(event)
		else:
			event.Skip()
