import requests, urllib.parse;

class UP_API:
	ENDPOINT = "https://api.up.com.au/api/v1/"
	def __init__(self, token):
		self.token = token

	def ping(self):
		""" Access the ping utility to ensure the validity of the Bearer token """
		headers = { "Authorization": f"Bearer {self.token}" }
		api_path = "util/ping"
		full_path = urllib.parse.urljoin(UP_API.ENDPOINT, api_path)

		response = requests.get(urllib.parse.urljoin(UP_API.ENDPOINT, api_path), headers=headers)

		return response.status_code == 200


	def accounts(self):
		headers = { "Authorization": f"Bearer {self.token}" }
		api_path = "accounts"
		
		response = requests.get(urllib.parse.urljoin(UP_API.ENDPOINT, api_path), headers=headers)
		
		if response.status_code == 200:
			return [Account(i, self) for i in response.json()["data"]]

	
	def account(self, account_id):
		headers = { "Authorization": f"Bearer {self.token}" }
		api_path = f"accounts/{account_id}"

		response = requests.get(urllib.parse.urljoin(UP_API.ENDPOINT, api_path), headers=headers)

		if response.status_code == 200:
			return response.json()

	def transactions(self):
		headers = { "Authorization": f"Bearer {self.token}" }
		api_path = "transactions"
		
		response = requests.get(urllib.parse.urljoin(UP_API.ENDPOINT, api_path), headers=headers)

		if response.status_code == 200:
			return TransactionSet(response.json()["data"], self)
		else:
			return response.status_code
	
	def transactions_by_account(self, account_id):
		headers = { "Authorization": f"Bearer {self.token}" }
		api_path = f"accounts/{account_id}/transactions"

		response = requests.get(urllib.parse.urljoin(UP_API.ENDPOINT, api_path), headers=headers)

		if response.status_code == 200:
			return response.json()

class Account:
	def __init__(self, account_dict, self_api):
		self.self_api = self_api

		self.id = account_dict["id"]
		self.display_name = account_dict["attributes"]["displayName"]
		self.account_type = account_dict["attributes"]["accountType"]
		self.ownership_type = account_dict["attributes"]["ownershipType"]
		self.balance = account_dict["attributes"]["balance"]["value"]
		self.currency = account_dict["attributes"]["balance"]["currencyCode"]

	def get_transactions(self):
		return self.self_api.transactions_by_account(self.id)

class Transaction:
	def __init__(self, transaction_dict, self_api):
		self.self_api = self_api
		
		self.id = transaction_dict["id"]
		self.status = transaction_dict["attributes"]["status"]
		self.raw_text = transaction_dict["attributes"]["rawText"]
		self.description = transaction_dict["attributes"]["description"]
		self.message = transaction_dict["attributes"]["message"]
		self.is_categorizable = transaction_dict["attributes"]["isCategorizable"]
		
		self.value = transaction_dict["attributes"]["amount"]["value"] 
		self.currency = transaction_dict["attributes"]["amount"]["currencyCode"]

		self.created_at = transaction_dict["attributes"]["createdAt"]
		self.settled_at = transaction_dict["attributes"]["settledAt"]
		
		if transaction_dict["relationships"]["category"]["data"]:
			self.category = transaction_dict["relationships"]["category"]["data"]["id"]
		else:
			self.category = None

class TransactionSet:
	def __init__(self, data_dict, self_api):
		self.transactions = [Transaction(i, self_api) for i in data_dict]
		self.self_api = self_api

	def get_by_category(self, category):
		t = TransactionSet([], self.self_api)
		t.transactions = [i for i in self.transactions if i.category == category]

		return t

	def get_by_description(self, description):
		t = TransactionSet([], self.self_api)
		t.transactions = [i for i in self.transactions if i.description == description]
		
		return t

	def __getitem__(self, item):
		return self.transactions[item]

	def __iter__(self):
		return self.transactions
