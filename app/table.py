import cPickle


class TableDict(object):
    """A table stored as a dict of dicts"""
    def __init__(self, num_periods):
        #super(Table, self).__init__()
        self.num_periods = num_periods
        self.data = {}
        self.data['demand'] =  {t: 0 for t in xrange(1, num_periods+1)}
        self.data['stock'] =  {t: 0 for t in xrange(1, num_periods+1)}
        self.data['forecast'] =  {t: 0 for t in xrange(1, num_periods+2)}
        self.data['order'] =  {t: 0 for t in xrange(1, num_periods+1)}
        self.data['received'] =  {t: 0 for t in xrange(1, num_periods+1)}
        self.allowed = ['demand', 'stock', 'forecast', 'order', 'received']
        self.current_period = 0


    def set_cell(self, row, period, value):
        if row not in self.allowed:
            raise Exception('Row identifier not recognized')

        if 0 < period <= self.num_periods:
            self.data[row][period] = value

        return

    def get_cell(self, row, period):
        if row not in self.allowed:
            raise Exception('Row identifier not recognized')

        if 0 < period <= self.num_periods:
            return self.data[row][period]


    def print_table(self):
        print self.data['demand']
        print self.data['stock']
        print self.data['forecast']
        print self.data['order']
        print self.data['received']


    def get_HTML(self):
        html = '<table border=1 width=200%><tr><th width=8%>&nbsp;</th>'
        for t in xrange(1, self.num_periods+1):
            html += '<th width={}%>{}</th>'.format(92./self.num_periods, t)
        html +='</tr>'

        html += self.convert_row('stock')
        html += self.convert_row('received')
        html += self.convert_row('forecast')
        html += self.convert_row('demand')
        html += self.convert_row('order')

        html += '</table>'
        return html


    def convert_row(self, row):
        if row not in self.allowed:
            raise Exception('Row identifier not recognized')
        _html = ''
        _html +='<tr><td>{}</td>'.format(row.upper())
        for t in xrange(1, self.num_periods+1):
            htmlclass=''
            if t == self.current_period:
                htmlclass='current'
            elif t < self.current_period:
                htmlclass='past'
            _html += '<td align=right class={}>{}</td>'.format(htmlclass, self.get_cell(row, t))
        _html +='</tr>\n\r'
        return _html



def main():
    t = TableDict(10)
    t.print_table()

    with open('ftable.pick', 'w') as handle:
        cPickle.dump(t.data, handle)

    try:
        t.set_cell('pippo', 1, 10)
    except Exception as e:
        print e

    try:
        t.set_cell('order', 5, 1000)
    except Exception as e:
        print e

    t.print_table()
    print t.get_cell('order', 5)

    print t.get_HTML()


if __name__ == '__main__':
    main()

