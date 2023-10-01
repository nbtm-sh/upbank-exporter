from up.api import UP_API
from prometheus_client import Gauge, start_http_server
import time

class Exporter:
	def __init__(self, api : UP_API, port = 8192):
		self.api = api
		self.INT = 60
		self.port = port

	def run(self):
		spend_gauge = Gauge("up_debit_account_balance", "Balance of the debit account")

		start_http_server(self.port)
		
		while True:
			spend_gauge.set(float(self.api.accounts().value))
			
			time.sleep(self.INT)
					
