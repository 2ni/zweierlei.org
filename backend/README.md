### Installation
```
brew install pyenv-virtualenv (see https://github.com/pyenv/pyenv-virtualenv)

pyenv install 3.7.1
pyenv virtualenv zweierlei
pyenv local zweierlei
(pyenv activate zweierlei)
pip install -Ur requirements.txt
```

### Resources / Todos
- use private / public keys for jwt
- global allowedFields for ie user

- https://blog.angular-university.io/angular-jwt/
- https://blog.mwaysolutions.com/2014/06/05/10-best-practices-for-better-restful-api/
- https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb

### Redis
- https://medium.com/@stockholmux/from-sql-to-redis-chapter-1-145c82e4baa0

Common commands for redis-cli
```
FLUSHALL          - all
FLUSHDB           - current db
SMEMBERS          - return all members of a set
HMSET             - insert hash
HGETALL	          - get all key/values from a hash
SADD              - add to unordered set
ZADD	          - add to sorted set
ZRANGEBYSCORE     - get range of sorted set
ZRANGE key 0 -1   - get all members of sorted set
ZSCORE key member - get value / check if exists
RPUSH key value   - insert to sorted list
LRANGE key 0 -1   - get all members of sorted list
```

see redis.txt
z:users:<id>           (hash)
z:allUsers             (unordered set)
z:usersByEmail:<email> (string)
z:stories:<id>         (hash)
z:allStories           (unordered set)
z:storiesCreatedIndex  (ordered set)

### Useful terminal stuff
```
convert -size 1x1 xc:white test.jpg                                  # create jpg
exiftool -GPSLatitude="68.154715" -GPSLongitude="14.211241" -GPSLatitudeRef="North" -GPSLongitudeRef="East" test.jpg
exiftool -GPSDateTime="2018-20-10 07:15:30Z" -GPSDateStamp="2018:10:20" -GPSTimeStamp="07:15:30" test.jpg
```

### Useful python stuff
```
> # create uuid
> import uuid
> uuid.uuid4()
>
> # get timestamp from date string
> from datetime import datetime as dt
> from datetime import timezone
> s = "24.12.2017 18:30:00
> dt.strptime(s, "%d.%m.%Y %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()
> ts = 1573470671
> dt.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
