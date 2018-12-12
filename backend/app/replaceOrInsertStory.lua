--[[

Replace or insert new story
Mandatory: uid <uid> id <id> title <title> description <description>

redis-cli --eval replaceOrInsertStory.lua   , uid 5834578e-351c-451a-94c6-500aa755f80 id 111 title <title> description <description>

]]--

local argv = {}
local nextkey
for i, v in pairs(ARGV) do
    if i % 2  == 1 then
        nextkey = v
    else
        argv[nextkey] = v
    end
end

-- check mandatory fields
local err_elms = ""
local err_count = 0
for i, key in pairs({"uid", "id", "title", "description"}) do
    if not argv[key] or argv[key] == "None" then
        err_elms = err_elms .. key .. ","
        err_count = err_count+1
    end
end

if err_count > 0 then
    return "required element:" .. err_elms:sub(1, -2)
end

-- TODO keys computed for now (should be given by KEYS argument when calling script
local KEYstory = "z:stories:" .. argv["id"]
local KEYstoryByUser = "z:storiesByUser:" .. argv["uid"]
local KEYcreated = "z:stories:index:created"
local KEYuser = "z:users:" .. argv["uid"]

-- check if user exists
if redis.call("EXISTS", KEYuser) == 0 then
    return "not found: uid"
end

-- check if user allowed
if redis.call("EXISTS", KEYstory) == 1 and redis.call("ZSCORE", KEYstoryByUser, argv["id"]) == false then
    return "not allowed"
end

-- add meta data
local argvPacked = {}
for k,v in pairs({"title", "description"}) do table.insert(argvPacked, v) table.insert(argvPacked, argv[v]) end
redis.call("HMSET", KEYstory, unpack(argvPacked))

-- save created if it not exists
if argv["created"] and redis.call("ZSCORE", KEYcreated, argv["id"]) == nil then
    redis.call("ZADD", KEYcreated, argv["created"], argv["id"])
end

-- save to user story list if not yet done
if redis.call("ZSCORE", KEYstoryByUser, argv["id"]) == false then
    local count = redis.call("ZREVRANGEBYSCORE", KEYstoryByUser, "inf", "-inf", "WITHSCORES", "LIMIT", 0, 1)[2]
    if count then
        count = count + 1
    else
        count = 0
    end
    redis.call("ZADD", KEYstoryByUser, count, argv["id"])
end

return "OK"
