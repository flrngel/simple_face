# Simple face recognition

```bash
# prepare redis
$ docker run -d -p 6379:6379 --name redis redis
# build (only first)
$ docker build -t face .
# execute
$ docker run -it --rm -v `pwd`:/app --link redis:redis face python app.py
```
