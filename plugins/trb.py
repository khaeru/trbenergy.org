#!/usr/bin/env python3
import os

import pandas as pd
from logging import warn
from pelican import signals
from pelican.generators import CachingGenerator


PAGE_TITLES = {
    'members': '%d Transportation Energy Committee',
    'presentations': '%d Presentations',
    }


class TRBGenerator(CachingGenerator):
    def __init__(self, *args, **kwargs):
        super(TRBGenerator, self).__init__(*args, **kwargs)

        settings = kwargs['settings']['TRB']

        # Load data
        data = {}
        tables = ['members', 'sessions', 'presentations']
        if settings['data_source'] == 'google_drive':
            # Connect to the spreadsheet containing the presentations data
            import gspread
            conn = gspread.login(*settings['data_auth'])
            workbook = conn.open_by_key(settings['google_drive_key'])
            for t in tables:
                tmp = workbook.worksheet(t).get_all_values()
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
                'title': PAGE_TITLES[type] % kwargs['year'],
                'content': self.get_template(type).render(localcontext),
                }

        template = self.get_template('page')

        for year, members in self.data['members'].groupby('Year'):
            fn = os.path.join('pages', 'members-%d.html' % year)
            page = _pseudo_page('members', year=year, members=members)
            writer.write_file(fn, template, self.context, page=page,
                              relative_urls=self.settings['RELATIVE_URLS'])
            print('TRB plugin: wrote %s' % fn)

        for year, p in self.data['all'].groupby('Year'):
            fn = os.path.join('pages', 'presentations-%d.html' % year)
            page = _pseudo_page('presentations', year=year, presentations=p)
            writer.write_file(fn, template, self.context, page=page,
                              relative_urls=self.settings['RELATIVE_URLS'])
            print('TRB plugin: wrote %s' % fn)


def callback(pelican):
    return TRBGenerator


def add_template_path(pelican):
    pelican.settings['EXTRA_TEMPLATES_PATHS'].append(
        os.path.join(os.path.dirname(__file__), 'trb')
        )


def register():
    signals.initialized.connect(add_template_path)
    signals.get_generators.connect(callback)
