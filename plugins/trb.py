from pathlib import Path
import os
import logging

import pandas as pd
from pelican import signals
from pelican.generators import CachingGenerator


PAGE_TITLES = {
    'members': '{year} Transportation Energy Committee',
    'presentations': '{year} Presentations',
    }


log = logging.getLogger(__name__)


class TRBGenerator(CachingGenerator):
    def __init__(self, *args, **kwargs):
        # Add the path to the templates used by this generator
        kwargs["settings"].setdefault("THEME_TEMPLATES_OVERRIDES", [])
        kwargs["settings"]["THEME_TEMPLATES_OVERRIDES"].append(
            str(Path(__file__).parent / "trb")
        )

        # Use the parent class to initialize
        super().__init__(*args, **kwargs)

        # Retrieve plugin-specific settings
        settings = self.settings["TRB"]

        # Load data
        data = {}
        tables = ['members', 'sessions', 'presentations']
        if settings['data_source'] == 'google_drive':
            # Connect to the spreadsheet containing the presentations data
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                settings['data_auth'],
                scopes=['https://spreadsheets.google.com/feeds'])
            conn = gspread.authorize(credentials)
            workbook = conn.open_by_key(settings['google_drive_key'])
            for t in tables:
                tmp = workbook.worksheet(t.title()).get_all_values()
                data[t] = pd.DataFrame(tmp[1:], columns=tmp[0])
        elif settings['data_source'] == 'tsv':
            # Read from individual TSV files
            for t in tables:
                fn = '%s/%s.tsv' % (settings['data_path'], t)
                data[t] = pd.read_csv(fn, sep='\t')

        # Merge to a table containing all sessions
        data['all'] = pd.merge(data['presentations'], data['sessions'],
                               left_on=['Year', 'Session'],
                               right_on=['Year', 'Number'],
                               suffixes=['', '_s'])

        self.data = data

    def generate_output(self, writer):
        def _pseudo_page(type, **kwargs):
            localcontext = self.context.copy()
            localcontext.update(kwargs)
            return {
                'title': PAGE_TITLES[type].format(**kwargs),
                'content': self.get_template(type).render(localcontext),
                }

        template = self.get_template('page')

        log.info('TRB plugin: committee ')
        for year, members in self.data['members'].groupby('Year'):
            fn = os.path.join('members', str(year), 'index.html')
            page = _pseudo_page('members', year=year, members=members)
            writer.write_file(fn, template, self.context, page=page,
                              relative_urls=self.settings['RELATIVE_URLS'])

        log.info('TRB plugin: presentations ')
        for year, p in self.data['all'].groupby('Year'):
            fn = os.path.join('presentations', str(year),  'index.html')
            page = _pseudo_page('presentations', year=year, presentations=p)
            writer.write_file(fn, template, self.context, page=page,
                              relative_urls=self.settings['RELATIVE_URLS'])


def callback(pelican):
    return TRBGenerator


def register():
    signals.get_generators.connect(callback)
