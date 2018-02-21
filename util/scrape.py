"""Script for extracting information from the old, ORNL website."""

# coding: utf-8

# Cell:

import re

from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import display_html

pd.set_option('display.max_colwidth', -1)


# ## 2010, 2009(ish), 2008, 2007, 2006

# Cell:

YEAR = 2006
DEBUG = True

fn = './trb_sitepages/%d_webpage.html' % YEAR
soup = BeautifulSoup(open(fn), 'html.parser')


# Cell:

condense = lambda s: re.sub('\s{2,}', ' ', s)
session_re = re.compile('%d\s+(Poster )?Session (\d+)' % YEAR)
filename_re = re.compile('(?:../)?trb_documents/(?:\d{4}[ _]presentations/)?(.*)')

s_columns = ['Year',
             'Type',
             'Number',
             'Title']
sessions = []
p_columns = ['Year',
             'Session',
             'Number',
             'Slides',
             'Authors',
             'Title',
             'Filenames']
presentations = []

elem = [
    # 'td',  # 2010
    'div', 'td', 'span',  # 2008, 2007
    ]
td_classes = [
    # 'style17', 'style44', 'style55',  # 2010
    'style3', 'style17', 'style21', 'style44',  # 2008, 2007, 2006
    ]

for cell in soup.find_all(elem, class_=td_classes):
    text = ' '.join(map(condense, cell.stripped_strings))
    if text == '':
        continue
    link =  cell.find('a')
    if link:
        splits = text.split(' - ', maxsplit=1)
        p_title = ' - '.join(splits[:-1])
        p_authors = splits[-1]
        match = filename_re.match(link['href'])
        if match:
            p_slides = 'Y'
            p_filename = match.groups()[0].replace('%20', ' ')
        else:
            assert False, link['href']
            p_filename = ''
        #print(p_title, p_author, p_filename, '', sep='\n')
        presentations.append({
            'Year': YEAR,
            'Session': session,
            'Number': '{:02}-XXX'.format(YEAR % 2000),
            'Slides': p_slides,
            'Authors': p_authors,
            'Title': p_title,
            'Filenames': p_filename,
            })
    else:
        #print('\n', text)
        try:
            s_number, s_title = text.split(' - ', maxsplit=1)
        except ValueError:
            s_number = text
        session = session_re.match(s_number)
        if session:
            s_type = 'Session'
            session = session.groups()[1]
            #print(s_title)
        # elif s_number == '2010 Committee Meeting':  # 2010
        # elif s_number.startswith('"Handouts"'):  # 2007
        elif s_number in ['Other Presentations', 'Special Report']:  # 2006
            session = 'ADC70'
            s_type = 'Meeting'
            s_title = 'Transportation Energy Committee'
        elif s_number == 'Subcommittee Meeting':
            session = 'CCJS'
            s_type = 'Meeting'
            s_title = 'Climate Change Joint Subcommittee of ADC70, ADC80, ADD40'
        else:
            print('MISSED:', s_number)
            continue
        sessions.append({'Year': YEAR,
                         'Type': s_type,
                         'Number': session,
                         'Title': s_title})

sessions = pd.DataFrame(sessions, columns=s_columns).drop_duplicates()
presentations = pd.DataFrame(presentations,
                             columns=p_columns).drop_duplicates()
csv_kwargs = dict(index=False, sep='\t')

if DEBUG:
    display_html(sessions.to_html(index=False), raw=True)
    display_html(presentations.to_html(index=False), raw=True)
else:
    sessions.to_csv('sessions_%d.tsv' % YEAR, **csv_kwargs)
    presentations.to_csv('presentations_%d.tsv' % YEAR, **csv_kwargs)
