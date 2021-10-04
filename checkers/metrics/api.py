import re
import user_agent_randomizer
from requests import Session
from errs import INVALID_FORMAT, CONNECTION_FAILURE


class Api:
    def __init__(self, address):
        self.host = address
        self.url = f"http://{self.host}"
        self.session = Session()

    def send_metric(self, metric):
        try:
            resp = self.session.put(f"{self.url}/metrics/save_metric", json=metric, headers={"User-Agent": user_agent_randomizer.get()})
        except Exception as e:
            print(e)
            return CONNECTION_FAILURE, None
        try:
            token = resp.json().get("token")
            if token is None:
                return INVALID_FORMAT, None
        except Exception as e:
            print(e)
            return INVALID_FORMAT, None

        return None, token


    def get_metric(self, token):
        data = {"token": token}
        try:
            resp = self.session.post(f"{self.url}/metrics/metric", json=data, headers={"User-Agent": user_agent_randomizer.get()})
        except Exception as e:
            print(e)
            return CONNECTION_FAILURE, None
        try:
            metric = resp.json()
            if not isinstance(metric, list):
                return INVALID_FORMAT, None
        except Exception as e:
            print(e)
            return INVALID_FORMAT, None
        return None, metric

    def get_metrics(self):
        try:
            resp = self.session.get(f"{self.url}/metrics", headers={"User-Agent": user_agent_randomizer.get()})
        except Exception as e:
            return CONNECTION_FAILURE, None
        try:
            metrics = resp.json().get("metrics")
            if metrics is None:
                return INVALID_FORMAT, None
        except Exception as e:
            print(e)
            return INVALID_FORMAT, None
        return None, metrics

if __name__ == "__main__":
    api = Api("localhost:8080")
    print(api.get_metrics())
