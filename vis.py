template = """
<body>
  <style>
  table {{ border-collapse: collapse; }}
  td {{ width: 20px; height: 20px; }}
  </style>
  {table}
"""


class TD:
    def __init__(self, color):
        self.color = color

    def render(self):
        return "<td style='background-color: %s'>&nbsp;</td>" % (self.color,)


class TR(list):
    def render(self):
        return '<tr>%s</tr>' % (''.join(td.render() for td in self),)


class Table:
    def __init__(self, width, height, default_color="#CCC"):
        self.rows = []
        for _ in range(height):
            row = [TD(default_color) for _ in range(width)]
            self.rows.append(TR(row))

    def render(self):
        tbl = '<table>%s</table>' % (''.join(tr.render() for tr in self.rows),)
        return template.format(table=tbl)
