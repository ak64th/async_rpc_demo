Run the server:

```bash
pip install -r requirements.txt
python -m async_rpc_demo_rq.bootstrap
# python -m async_rpc_demo_aps.bootstrap
```

Add new job

```http
POST / HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 78
Content-Type: application/json
Host: 127.0.0.1:8000
User-Agent: HTTPie/0.9.8

{
    "analysis": {
        "image_url": "https://via.placeholder.com/150",
        "task_type": 1
    }
}
```
```http
HTTP/1.1 200 OK
Connection: close
Content-Type: application/json
Date: Fri, 03 Jan 2020 06:36:57 GMT
Server: waitress
Transfer-Encoding: chunked

{
    "data": {
        "job_id": "32031b6b10e24f9dba8bb4ec4032526a"
    },
    "error": 0,
    "message": "Succeed"
}
```

Query job result:

```http
POST / HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 57
Content-Type: application/json
Host: 127.0.0.1:8000
User-Agent: HTTPie/0.9.8

{
    "query": {
        "job_id": "32031b6b10e24f9dba8bb4ec4032526a"
    }
}
```
```http
HTTP/1.1 200 OK
Connection: close
Content-Type: application/json
Date: Fri, 03 Jan 2020 06:38:22 GMT
Server: waitress
Transfer-Encoding: chunked

{
    "data": {
        "job_id": "32031b6b10e24f9dba8bb4ec4032526a",
        "result": null,
        "status": "queued"
    },
    "error": 0,
    "message": "Succeed"
}
```
