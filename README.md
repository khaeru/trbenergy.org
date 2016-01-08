# Website of TRB ADC70

This website uses the [Pelican](http://getpelican.com) static website generator. See the [Pelican documentation](http://docs.getpelican.com/en/stable) for more information.

A Pelican plugin, in `plugins/trb.py`, automatically generates two types of content:
- Lists of committee members.
- Lists of sessions and presentations from TRB Annual Meetings.

…from data stored either in a Google Drive spreadsheet, _or_ as text files in <acronym title="tab-separated values">TSV</a> format.

## Using

The plugin is controlled by the *TRB* setting in `private.py`. To protect private information, this file is not included with the code; users *must* create it, by copying `private.py.example`.

*TRB* is a Python `dict` with the following keys:
- **data_source**: either 'google_drive' or 'csv'. If 'google_drive', the [`gspread`](https://github.com/burnash/gspread) package must be installed to access Google Drive, and *data_auth* and *google_drive_key* must be set. If 'csv', *data_path* must be set.
- **data_auth**: a (username, password) tuple used to authenticate to Google Drive.
- **google_drive_key**: a 44-character string specifying the key or identifier of the Google Drive spreadsheet containing the data.
- **data_path**: path relative to the root directory containing data in the files `members.tsv`, `presentations.tsv` and `sessions.tsv`.
- **pdf_urls**: either 'local' or 'cloud'.

Create a symlink named `themes` to a directory containing the [pelican-themes](https://github.com/getpelican/pelican-themes) repository.

## License
Copyright 2015, Paul Natsuo Kishimoto <<mail@paul.kishimoto.name>>

Licensed under the [GNU General Public License, version 3](http://www.gnu.org/licenses/gpl-3.0.en.html).
