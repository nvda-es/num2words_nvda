# [Number to words](https://github.com/savoirfairelinux/num2words) for NVDA

Author: Mateo Cedillo

## Introduction:

I was inspired to make this little add-on, because some people use speech synthesizers like `ETI-Eloquence` which has some flaws when it comes to number processing, even if they are separated and confuses the user saying both numbers separated by spaces as if it were a decimal point. 

This add-on improves the reading of numbers to words for these cases, it supports larger numbers and, in addition, the library supports many languages.

## Usage:

This addon has two ways of using numbers to words:

* Real time mode: as long as NVDA is talking and there's a text containing numbers anywhere in it, the conversion will display its result and be transmitted by speech. This applies to any speech synthesizer you use.
* Manual mode: you can write numbers or text, and/or numbers at the same time, interacting through a dialog box to do so. The dialog has:
	* An input box to write your entry.
	* A convert button. By pressing this button, you will be shown a message box with the final result.
	* A cancel button: Exits the conversion dialog.

### Input gestures:

* Toggle numbers to words (or real time mode): (Unassigned gesture for now to avoid interference with other add-ons).
* Open conversion dialog (manual mode): alt+shift+NVDA+n.
* More features soon!

#### Important notes:

* As the library supports many languages, keep in mind that the conversion is done in the language of your speech synthesizer. This will even apply when you change the language of your synthesizer.
* Currently, speaking a converted number with the cursor isn't implemented and as a consequence will spell out the converted number.

## Compile this add-on:

Note: this add-on depends on a submodule, so:

1. cd to this repo: `cd num2words_nvda`
2. Type `git submodule init` and `git submodule update` in the console to clone the num2words library repository that is set as a module.
3. If there are no errors, `scons` command should work correctly.

## Contact:

If you want to help improve this addon, you can send an email to `angelitomateocedillo@gmail.com` or make your contributions on the GitHub repo.

---

# Changelog:

## 0.1

* Initial release. You may find some minor bugs. If so, please let me know.