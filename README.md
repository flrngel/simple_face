# Simple face recognition

```bash
# prepare redis
$ docker run -d -p 6379:6379 --name redis redis
# build (only first)
$ docker build -t face .
# execute once
$ docker run -it --rm -v `pwd`:/app --link redis:redis face python app.py
# execute background
$ docker run -d --rm -v `pwd`:/app --link redis:redis face ./background.sh
```
