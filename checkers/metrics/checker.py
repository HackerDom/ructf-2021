import string
import random
import re

from gornilo import Checker, CheckRequest, PutRequest, GetRequest, Verdict
from api import Api

devices = ["Huawei", "JBL", "Samsung", "Sony", "Xiaomi"]
types = ["time", "volume"]

checker = Checker()


def get_random_str(length=10, only_chars=False):
    if only_chars:
        return "".join(random.choices(string.ascii_letters, k=length))
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


@checker.define_check
async def check_service(request: CheckRequest) -> Verdict:
    api = Api(f"{request.hostname}:5051")
    device = random.choice(devices)
    metric_type = random.choice(types)
    metainfo = get_random_str()
    info = get_random_str(length=20)
    value = random.randint(10, 100) if metric_type == "volume" else random.randint(1, 3600)
    metric = {"device": device, "type": metric_type, "value": value, "info": info, "metainfo": metainfo}
    err, token = api.send_metric(metric)
    if err is not None:
        return verdict_from_api(err)
    err, res = api.get_metric(token)
    if err is not None:
        return verdict_from_api(err)
    if len(res) == 0 or res[0].get("device") != device or res[0].get("type") != metric_type or res[0].get("value") != value or res[0].get("metainfo") != metainfo:
        return Verdict.MUMBLE("invalid metric")
    
    err, metrics = api.get_metrics()
    if err is not None:
        return verdict_from_api(err)
    if {"device": device, "type": metric_type, "value": value, "info": info} not in metrics:
        return Verdict.MUMBLE("invalid list of metrics")
    
    return Verdict.OK()


@checker.define_put(vuln_rate=1, vuln_num=1)
async def put(request: PutRequest) -> Verdict:
    api = Api(f"{request.hostname}:5051")
    device = random.choice(devices)
    metric_type = random.choice(types)
    metainfo = request.flag
    info = get_random_str(length=20)
    value = random.randint(10, 100) if metric_type == "volume" else random.randint(1, 3600)
    metric = {"device": device, "type": metric_type, "value": value, "info": info, "metainfo": metainfo}
    err, token = api.send_metric(metric)
    if err is not None:
        return verdict_from_api(err)
    return Verdict.OK(token)


@checker.define_get(vuln_num=1)
async def get(request: GetRequest) -> Verdict:
    api = Api(f"{request.hostname}:5051")
    token = request.flag_id.strip()
    # print(token)
    err, metric = api.get_metric(token)
    if err is not None:
        return verdict_from_api(err)
    # print(metric)
    if len(metric) == 0:
        return Verdict.MUMBLE("invalid metric")
    # print(metric[0]["metainfo"], request.flag)
    if metric[0].get("metainfo") != request.flag:
        return Verdict.MUMBLE("invalid flag")
    
    return Verdict.OK()
    


def verdict_from_api(err: str) -> Verdict:
    if err == "connection failure":
        return Verdict.DOWN(err)
    else:
        return Verdict.MUMBLE(err)


if __name__ == "__main__":
    checker.run()
