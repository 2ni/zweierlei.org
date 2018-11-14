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
- https://blog.angular-university.io/angular-jwt/
- https://blog.mwaysolutions.com/2014/06/05/10-best-practices-for-better-restful-api/
- https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb

### Redis
- https://medium.com/@stockholmux/from-sql-to-redis-chapter-1-145c82e4baa0

Common commands for redis-cli
```
FLUSHALL      - all
FLUSHDB       - current db
SMEMBERS      - return all members of a set
HMSET         - insert hash
HGETALL	      - get all key/values from a hash
SADD          - add to unordered set
ZADD	      - add to sorted set
ZRANGEBYSCORE - get range of sorted set
```

see redis.txt
z:users:<id> (hash)
z:allUsers   (unordered set)

z:stories:<id> (hash)
z:allStories   (unordered set)
z:storiesCreatedIndex (ordered set)


### Usefull python stuff
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
