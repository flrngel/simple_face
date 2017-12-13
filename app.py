import redis
import face_recognition
from skimage import io
import glob
import time
import json
import os
import numpy as np

r = redis.StrictRedis.from_url(url='redis://redis')

camera_nums = 1
visit_margin = 60 * 60 * 2

def get_timestamp():
  return int(time.time())

now_time = get_timestamp()

#filenames = sorted(glob.glob('./cctv_images/*.jpg'))

face_db = r.lrange('facedb', 0, -1)
for i in range(len(face_db)):
  face_db[i] = np.asarray(json.loads(face_db[i]))

for cam_i in range(camera_nums):
  #r.delete(f'bbox:{cam_i}')

  image = face_recognition.load_image_file(f'./cctv_images/{cam_i}.jpg')
  face_locations = face_recognition.face_locations(image)

  face_locations_final = []

  for face_location in face_locations:
    si, ej, sj, ei = face_location
    encodings = face_recognition.api.face_encodings(image[si:sj, ei:ej])
    if len(encodings) == 0:
      continue
    now_face = encodings[0]
    r.zadd(f'{cam_i}:bbox_history', now_time, ','.join([str(si), str(sj), str(ei), str(ej)]))
    if len(face_db) > 0:
      compare_face = face_recognition.api.compare_faces(face_db, now_face, tolerance=0.3)
      if True in compare_face:
        i = compare_face.index(True)
        history = r.zrevrange(f'{i}:history', 0, 1)

        if len(history) == 1:
          last_visited = int(history[0])
          if now_time - last_visited <= visit_margin:
            r.zadd(f'{i}:history', now_time, now_time)
            r.zadd(f'customer_history', now_time, i)
      else:
        i = len(face_db)
        r.lpush('facedb', json.dumps(now_face.tolist()))
        face_db.append(now_face[0])
        r.zadd(f'{i}:history', now_time, now_time)
        r.zadd(f'customer_history', now_time, i)
        io.imsave(f'faces/{i}.jpg', image[si:sj, ei:ej])
    else:
      # TODO: remove duplicated code
      i = len(face_db)
      r.lpush('facedb', json.dumps(now_face.tolist()))
      face_db.append(now_face)
      r.zadd(f'{i}:history', now_time, now_time)
      io.imsave(f'faces/{i}.jpg', image[si:sj, ei:ej])

    face_locations_final.append({i: face_location})

  r.set(f'bbox:{cam_i}', json.dumps(face_locations_final))

  # TODO: unlink after process
  #os.unlink()
