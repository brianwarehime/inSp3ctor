import requests as req
import json

from bs4 import BeautifulSoup
from queue import Empty, Queue
from threading import Thread

max_consumers = 10
results = dict(Bucket={}, Object={})
files = []
verbose = True


def check_object_status(xml_response, site):
    y = BeautifulSoup(xml_response, "html.parser")
    object_keys = y.findAll('key')
    for key in object_keys:
        bucket_checker(site.rstrip() + "/" + key.get_text(), "Object")


def parse_response(xml_response):
    y = BeautifulSoup(xml_response, "html.parser")
    return y.error.endpoint.string


def check_response(status_code: int, word, content, s3_type):
    redirect = ''
    global results
    if status_code == 200:
        results[s3_type].setdefault('public', []).append(word.rstrip())
        if content:
            check_object_status(content, word)
    elif status_code == 403:
        results[s3_type].setdefault('private', []).append(word.rstrip())
    elif status_code == 301:
        if content:
            redirect = parse_response(content)
            bucket_checker(f"http://{redirect}", 'Bucket')
    else:
        results[s3_type].setdefault('no_exist', []).append(word.rstrip())


def bucket_checker(word, s3_type):
    if s3_type == "Object":
        try:
            checker = req.head(word.rstrip(), timeout=10)  # for larges files
        except req.exceptions.Timeout:
            check_response(200, word, None, s3_type)
        check_response(checker.status_code, word, None, s3_type)
    if s3_type == "Bucket":
        checker = req.get(word.rstrip())
        check_response(checker.status_code, word, checker.content, s3_type)


def produce(queue: Queue):
    with open('bucket_names.txt', 'r') as fb:
        with open('file_names.txt', 'r') as ff:
            buckets = fb.readlines()
            files = ff.readlines()
            for l in buckets:
                l = l.strip()
                queue.put(("Bucket", f"http://s3.amazonaws.com/{l}"))
                queue.put(("Bucket", f"http://{l}.s3.amazonaws.com"))
                [queue.put(
                    ("Object", f"http://s3.amazonaws.com/{l}/{f}")) for f in files]
                [queue.put(
                    ("Object", f"http://{l}.s3.amazonaws.com/{f}")) for f in files]


def consume(queue: Queue):
    while not queue.empty():
        try:
            s3_type, url = queue.get(timeout=0.1)
            queue.task_done()
            if verbose:
                print(url)
            bucket_checker(url, s3_type)
        except Empty:
            pass
    return


def remove_repeated(_results: dict):
    for k in _results['Bucket'].keys():
        _results['Bucket'][k] = list(set(_results['Bucket'][k]))
    for k in _results['Object'].keys():
        _results['Object'][k] = list(set(_results['Object'][k]))
    return _results


def main():
    q = Queue()
    produce(q)

    consumers = []
    for i in range(max_consumers):
        consumer = Thread(target=consume, args=(q,))
        consumer.start()
        consumers.append(consumer)

    for consumer in consumers:
        consumer.join()


if __name__ == '__main__':
    main()
    print(json.dumps(remove_repeated(results)))
