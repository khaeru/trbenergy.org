title: {{year}} Presentations

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
