#!/usr/bin/env python3
import os

import gspread
from jinja2 import Environment, Template
import pandas as pd

TARGET = 'content/pages/{}.md'

e = Environment(trim_blocks=True, lstrip_blocks=True)


def worksheet_to_df(name):
    data = sh.worksheet(name).get_all_values()
    return pd.DataFrame(data[1:], columns=data[0])

def t(text):
    return e.from_string(text)

# Connect to the spreadsheet containing the presentations data
gc = gspread.login(os.environ['GOOGLE_EMAIL'], os.environ['GOOGLE_PW'])
sh = gc.open_by_key(os.environ['DATA_WB_KEY'])

# Committee members
template = t("""title: 2012 Transportation Energy Committee

<table class="table">
  <tr>
    <th>Name</th>
    <th>Affiliation</th>
    <th>Status</th>
  </tr>
{% for n, member in members.iterrows() %}
  <tr>
    <td>{{member.Title}} {{member.Name}}</td>
    <td>{{member.Organization}}</td>
    <td>{{member.Status}}</td>
  </tr>
{% endfor %}
</table>
""")

with open(TARGET.format('members'), 'w') as f:
    html = template.render(members=worksheet_to_df('Members 2012'))
    f.write(html)

# Presentation

sessions = worksheet_to_df('Sessions')
presentations = worksheet_to_df('Presentations')

allp = pd.merge(presentations, sessions,
                left_on=['Year', 'Session'], right_on=['Year', 'Number'],
                suffixes=['', '_s'])

template = t(
"""title: {{year}} Presentations
{% set dash = joiner(' — ') %}
{% for ns, s in presentations.groupby('Session') %}
  {{ dash() }}<a href="#{{ns}}">{{ns}}</a>
{% endfor %}

{% for ns, s in presentations.groupby('Session') %}
{% for np, p in s.iterrows() %}
{% if loop.first %}
<a name="{{ns}}"></a>
## {{p.Type}} {{p.Number_s}}: {{p.Title_s}}
<table class="table">
{% endif %}
  <tr>
    <td style="white-space:nowrap">
    {% if p.Slides == 'Y' %}
    [{{p.Number}}]({filename}/pdf/{{p.Number}}.pdf)
    {% else %}
    {{p.Number}}
    {% endif %}
    </td>
    <td>
      {{p.Title}}<br/>
      <strong>{{p.Authors}}</strong>
    </td>
  </tr>
{% endfor %}
</table>
<span style="float:right"><a href="#top">⇱ back to top</a></span>
{% endfor %}
""")

for year, group in allp.groupby('Year'):
    with open(TARGET.format(year), 'w') as f:
        f.write(template.render(year=year, presentations=group))
