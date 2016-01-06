title: {year} Transportation Energy Committee

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
