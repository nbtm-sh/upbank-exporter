import exporter, os
from upbankapi import Client

if __name__ == '__main__':
	api = Client(os.getenv("UP_TOKEN"))
	exp = exporter.Exporter(api)

	exp.run()	
