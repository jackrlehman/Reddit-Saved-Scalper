# Reddit Saved Scalper
Last updated: 10/18/2022. Current version broken as of 2/18/2023.

## About
Reddit Saved Scalper downloads all static media (excluding text) from your reddit saved tab. As Reddit's saved tab is limited to 1k posts, and deletes saved items past 1.2k, this utility allows for you to maintain your saved tab without worrying about saved media being forever lost.

## Usage
Executable Included. Download: https://github.com/jackrlehman/Reddit-Saved-Scalper/releases


## Development
Requires Python 3+

### Packages
selenium 4.5.0, webdriver-manager 3.8.3, urllib3 1.26.12
<pre>
"pip3 install selenium" 
"pip3 install webdriver-manager"
"pip3 install urllib3"
</pre>

### Exe Creation
https://stackoverflow.com/questions/5458048/how-can-i-make-a-python-script-standalone-executable-to-run-without-any-dependen for usage.

<pre>
python -m PyInstaller [args] (ex: python -m PyInstaller script.py)
</pre>

Versioning format:
<pre>
v(MONTH).(DAY).(YEAR).(LETTER)
v10.18.2022.A
</pre>
