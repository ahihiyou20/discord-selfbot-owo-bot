from requests import get, post

class CAPI:
	def __init__(self, userID: str, server: int):
		self.ID = userID
		self.url = None
		if server == 1: self.url = "https://autofarmsupport.tk"
		elif server == 2: self.url = "https://afbot.dev"

	def solve(self, Json: dict) -> bool:
		Json['id'] = self.ID
		result = post(self.url, json=Json, timeout=300)
		if result.ok:
			return result.json()
		elif result.status_code == 401:
			return False

	def report(self, Json) -> None:
		Json['id'] = self.ID
		post(self.url + "/report", json=Json, timeout=120)
