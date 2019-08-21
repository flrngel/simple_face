# Simple face recognition

## How to run
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

## How to see results

1. Put first frame of cctv as `0.jpg`(refers to <camera_id>.jpg) into `./cctv_images`
2. Wait for 5 seconds
3. Put next frame of cctv as `0.jpg` into `./cctv_images`
4. Check the directory `./faces/`
5. Check the redis with command below
```bash
docker exec -it <redis container id> redis-cli keys*
docker exec -it <redis container id> redis-cli zrange 0 -1 <face_id>:history
```
