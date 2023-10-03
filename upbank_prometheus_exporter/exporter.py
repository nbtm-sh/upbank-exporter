import time
from prometheus_client import start_http_server, Gauge, Counter

class Exporter:
	def __init__(self, api, port = 8192):
		self.api = api
		self.INT = 60
		self.port = port
		self._trans_ids = []

	def run(self):
		account_val = Gauge("up_account_balance", "Balance of the account", ["account", "account_type", "ownership"])
		category_transactions = Counter("up_transactions", "All transactions", ["account", "category", "raw_text", "description"])

		start_http_server(self.port)
		
		while True:
			for i in self.api.accounts():
				account_val.labels(account=i.name, account_type=i.type, ownership=i.ownership_type).set(i.balance)
				for trans in i.transactions():
					# Something something trans girls when they see the name of any logistics company
					if trans.id in self._trans_ids:
						continue
					self._trans_ids.append(trans.id)
					# In future, this can be replaced with a webhook to avoid huge amounts of RAM usage if you like spending your money
					category = trans.category
					if category is None:
						category = ""
					else:
						category = trans.category.id
					category_transactions.labels(account=i.id, category=category, raw_text=trans.raw_text, description=trans.description).inc(max(0, trans.amount*-1))

			
			time.sleep(self.INT)
					
