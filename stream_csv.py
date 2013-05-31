import csv
from inspect import isgenerator
from django.http import HttpResponse


# The CSV writer only expects the file object to have a write() function.
# So we can just return the output straight back and send it to the browser.
# This might not always be the case.
class FakeFile(object):
    def write(self, string):
        return string


class StreamCSVException(Exception):
    pass


class StreamCSV():
    writer = csv.writer(FakeFile())

    def __init__(self):
        self.filename = 'output.csv'
        self.heading = []
        self.data_generator = False

    def output(self):
        if isgenerator(self.data_generator):
            yield self.writer.writerow(self.heading)
            for a in self.data_generator:
                yield self.writer.writerow(a)
        else:
            raise StreamCSVException('No data_generator provided. \
                Must pass a generator function (ie. yield not return)')

    def http_response(self):
        response = HttpResponse(self.output(), mimetype='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename=%s' % self.filename
        return response
