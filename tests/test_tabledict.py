#import os
#import sys
#topdir = os.path.join(os.path.dirname(__file__), "..")
#sys.path.append(topdir)
from app import table
import cPickle
from nose.tools import assert_equal


def test_table():
    t = table.TableDict(10)
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


