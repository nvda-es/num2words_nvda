# [Number to words](https://github.com/savoirfairelinux/num2words) for NVDA

Author: Mateo Cedillo

## Introduction:

I was inspired to make this little add-on, because some people use speech synthesizers like `ETI-Eloquence` which has some flaws when it comes to number processing, even if they are separated and confuses the user saying both numbers separated by spaces as if it were a decimal point. 

This add-on improves the reading of numbers to words for these cases, it supports larger numbers and, in addition, the library supports many languages.

## comparison of results between original and converted speech input

This comparison table demonstrates the differences between number processing on a synthesizer and num2words processing.

The following comparison has been evaluated using the [IBMTTS driver](https://github.com/davidacm/NVDA-IBMTTS-Driver) for NVDA.


### Using long numbers:

| Language | Original input | Output | Converted input |
|---|---|---|---|
| Spanish | 921359131290481307233416326 | nueve dos ún tres cinco nueve ún tres ún dos nueve cero cuatro ocho ún tres cero siete dos tres tres cuatro ún seis tres dos seis | novecientos veintiuno cuatrillones trescientos cincuenta y nueve mil ciento treinta y uno trillones doscientos noventa mil cuatrocientos ochenta y uno billones trescientos siete mil doscientos treinta y tres millones cuatrocientos dieciséis mil trescientos veintiséis |
| English | 921359131290481307233416326 | nine two one three five nine one three one two nine zero four eight one three zero seven two three three four one six three two six | nine hundred and twenty-one septillion, three hundred and fifty-nine sextillion, one hundred and thirty-one quintillion, two hundred and ninety quadrillion, four hundred and eighty-one trillion, three hundred and seven billion, two hundred and thirty-three million, four hundred and sixteen thousand, three hundred and twenty-six |

### Using spaces as separators (only in Spanish):

* Original input: 12 499
* Output: doce mil cuatrocientos noventa y nueve
* Converted input: doce cuatrocientos noventa y nueve

## Usage:

This addon has three ways of using numbers to words:

* Real time mode: as long as NVDA is talking and there's a text containing numbers anywhere in it, the conversion will display its result and be transmitted by speech. This applies to any speech synthesizer you use.
	* You can use this feature temporarily by adding an input gesture (see below). As this is a temporary feature, it will be disabled when you exit NVDA.
	* You can also configure this feature to start when NVDA starts. To do this, just press NVDA+N, go to `preferences>settings...` and select the number to words category. There you will find the corresponding checkbox.
* Manual mode: you can write numbers or text, and/or numbers at the same time, interacting through a dialog box to do so. The dialog has:
	* A checkbox to convert to ordinal.
	* If the ordinal box is not checked, a combo box will appear to choose the conversion mode. There are six conversion modes and they are as follows:
		* Ordinal, for example: 1 = first.
		* Ordinal number, for example: 1 = first (aplies the same method that ordinal option).
		* Date, for example (dd/mm/aaaa format): 23/07/2023 = Twenty-three  july  twenty twenty-three.
		* Hour, for example: 12:30:15 = It's twelve hours, thirty minutes and fifteen seconds.
		* Year, for example: 1980 =  nineteen eighty (has no effect in many languages).
		* Currency, for example: 2.15 = two euro, fifteen cents.
			* Once you select this option, a new combo box will appear to choose the currency. Each language has different currencies apart from the eur, and the list can vary.
	* An input box to write your entry.
	* A convert button. By pressing this button, you will be shown a message box with the final result.
	* A cancel button: Exits the conversion dialog.
* Selection mode: If there's selected text containing numbers or numbers between words, the result will be converted and spoken aloud.

Note: you can also copy the last result that was converted (see below)

### Input gestures:

* Toggle numbers to words (or real time mode): (Unassigned gesture for now to avoid interference with other add-ons).
* Convert numbers to words based on the selected text (selection mode): unassigned gesture.
* Open conversion dialog (manual mode): alt+shift+NVDA+n.
* Copy the last spoken result: unassigned gesture.
* More features soon!

#### Important notes:

* As the library supports many languages, keep in mind that the conversion is done in the language of your speech synthesizer. This will even apply when you change the language of your synthesizer.
* When starting NVDA, the synthesizer language is checked. If this is not supported, you will be notified.
* The num2words library can convert up to 27 consecutive numbers. If the text is longer than 27 numbers, it will let you know with a beep and a speech message.
* Currently, speaking a converted number with the cursor isn't implemented and as a consequence will spell out the converted number.

## Compile this add-on:

Note: this add-on depends on a submodule, so:

1. cd to this repo: `cd num2words_nvda`
2. Type `git submodule init` and `git submodule update` in the console to clone the num2words library repository that is set as a module.
3. If there are no errors, `scons` command should work correctly.

## Add-on(s) I was inspired by

During the development of this add-on, I have been inspired by the following which I thank each of the authors of these add-ons:

* [Clock and Calendar for NVDA](https://addons.nvda-project.org/addons/clock.en.html) because it gave me a base idea of how I could implement the date and time conversion.

## Contact:

If you want to help improve this addon, you can send an email to `angelitomateocedillo@gmail.com` or make your contributions on the GitHub repo.

---

# Changelog:

## 0.5.1

* In this patch I've fixed an error with manual conversion mode due to the code organization consequences.

## 0.5

* Added: The support for NVDA 2024.1 has been reintroduced, adding On-Demand mode support for switch num2words in realtime.
* Added: new scripts
	* Convert numbers to words based on the selected text.
	* Copy the last converted result, thanks `mk360`.
* Fixed: errors with invalid decimals. Now, for example, when num2words in realtime mode is enabled, NVDA will not go silent or display an error in the log in these cases.
* Updated: num2words library.
	* This update as new languages: Spanish Costa Rica, Welsh and Chechen
	* Code improvements, python 3.12 compativility.
* A code refactoring was made to the entire add-on. This way, it can be more readable and organized for contributers.

## 0.4.1

* In this patch I've made a regression for last tested NVDA version. Although I want to be honest and the thrut is that I've tested this add-on with 2024.1 alpha and 2024.1 hasn't been released yet, to avoid problems to publish it in the add-on store, I'll happily back to 2023.3 as the last tested version.
* Also, the variables in some functions in the code has been clarified to improve readability.

## 0.4

* Now, when selecting the conversion mode by currency, a combo box has been added to choose a currency to be converted, through the list of currencies supported by the selected language and determined by the synthesizer.
* Added an option in the NVDA settings panel to enable reading numbers to words in real time mode on startup.
* Added Ukrainian language, thanks to `Георгій` and `Володимир Пиріг`.
* Updated num2words to 0.5.13
	* Adds support for Belarusian and Slovak.
	* Updates and code refactorings for Rusian and Ukrainian.
* The add-on doesn't check anymore if scratchpad option in the `settings panel > advanced` is enabled.
* Fixed: `string index out of range` error when browsing websites. Thanks, `Volodymyr`.
* Fixed: Realtime conversion and NVDA speech separators. The add-on should now separate the converted words correctly.
* Fixed: compatibility with NVDA 2024.1.
* Fixed: improper translation handling in hour conversion. Language maintainers will need to update new entries for it to work correctly.
* Ordered the code for better readability.

## 0.3

* Added Turkish language, thanks to `Umut KORKMAZ`.
* Added date and time conversions in the manual conversion GUI.

## 0.2

* Now the result from numbers to words is capitalized.
* Updated num2words library to commit `da48a319179f19b900d5b01ed394b304e94d31cf`.
* Added conversion modes supported by the num2words library in the manual conversion GUI.
* Minor fixes in the manual conversion GUI.
* Added synthesizer language check when starting NVDA. So, in case the language isn't supported, a part of this add-on will be disabled.

## 0.1

* Initial release. You may find some minor bugs. If so, please let me know.