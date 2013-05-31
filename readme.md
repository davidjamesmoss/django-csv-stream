# Django-CSV-Stream

Simple wrapper around the standard Python CSV module for streaming very large CSV files to the browser row-by-row without intermediate files or StringIO.

### Usage (in a Django view)
	from stream_csv import StreamCSV

	def my_view(request):
		# Generator to yield one row at a time
		def data():
			for r in results:
				output = [r.name, r.address, r.phone]
				yield output

		my_csv = StreamCSV()
		my_csv.filename = 'Bookings.csv'  # Defaults to 'output.csv'
		my_csv.heading = ['Name', 'Adddress', 'Telephone']  # Optional
		my_csv.data_generator = data()
		return my_csv.http_response()
		
Raises a StreamCSVException if you don’t pass in a generator.