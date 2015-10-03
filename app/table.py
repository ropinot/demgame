import cPickle


class TableDict(object):
    """A table stored as a dict of dicts"""
    def __init__(self, num_periods):
        self.data = {}
        self.data['num_periods'] = num_periods
        self.data['demand'] =  {t: 0 for t in xrange(1, num_periods+1)}
        self.data['stock'] =  {t: 0 for t in xrange(1, num_periods+1)}
        self.data['forecast'] =  {t: 0 for t in xrange(1, num_periods+2)}
        self.data['order'] =  {t: 0 for t in xrange(1, num_periods+1)}
        self.data['received'] = {t: 0 for t in xrange(1, num_periods+1)}
        self.data['sales'] = {t: 0 for t in xrange(1, num_periods+1)}
        self.data['lost_sales'] = {t: 0 for t in xrange(1, num_periods+1)}
        self.data['error'] = {t: 0. for t in xrange(1, num_periods+1)}
        self.data['spot'] = {t: 0 for t in xrange(1, num_periods+1)}
        self.data['allowed'] = ['demand', 'stock', 'forecast', 'order', 'received', 'sales', 'lost_sales', 'error', 'spot']
        self.data['current'] = 1

    def __getitem__(self, key):
        return getattr(self, key)

    def set_current(self, period):
        self.data['current'] = period

    def set_cell(self, row, period, value):
        if row not in self.data['allowed']:
            raise Exception('Row {} not recognized'.format(row))

        if 0 < period <= self.data['num_periods']:
            self.data[row][period] = value

        return

    def get_cell(self, row, period):
        if row not in self.data['allowed']:
            raise Exception('Row {} not recognized'.format(row))

        if 0 < period <= self.data['num_periods']:
            return self.data[row][period]
        else:
            return 0

    def get_interval(self, row, from_period, to_period):
        """ Return a specified interval of data as a list (from_period and to_period included) """
        if row not in self.data['allowed']:
            raise Exception('Row {} not recognized'.format(row))

        if from_period < to_period <= self.data['num_periods']:
            if from_period <= 0:
                from_period = 1
            return [self.data[row][period] for period in xrange(from_period, to_period+1)]
        else:
            raise Exception('Error in setting from_period ({}) and/or to_period ({})'.format(from_period, to_period))


    def print_table(self):
        print self.data['forecast']
        print self.data['stock']
        print self.data['received']
        print self.data['order']
        print self.data['demand']
        print self.data['sales']
        print self.data['lost_sales']
        print self.data['spot']


    def get_HTML(self):
        html = '<table id="board" class="table table-striped table-condensed"><tr><th width=100px>&nbsp;</th>'
        for t in xrange(1, self.data['num_periods']+1):
            html += '<th width={}px>{}</th>'.format(45, t)
        html +='</tr>'

        html += self.convert_row('received')
        html += self.convert_row('stock')
        html += self.convert_row('spot')
        html += self.convert_row('forecast')
        html += self.convert_row('demand')
        html += self.convert_row('order')
        html += self.convert_row('sales')
        html += self.convert_row('lost_sales')
        html += self.convert_row('error')

        html += '</table>'
        return html


    def convert_row(self, row):
        if row not in self.data['allowed']:
            raise Exception('Row {} not recognized ({})'.format(row, str(self.data['allowed'])))
        _html = ''
        _html +='<tr><td>{}</td>'.format(row.upper())
        for t in xrange(1, self.data['num_periods']+1):
            htmlclass='""'
            if t == self.data['current']:
                htmlclass='current'
            elif t < self.data['current']:
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


