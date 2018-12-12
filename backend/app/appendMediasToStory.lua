--[[

appends medias to story if story exists and uid allowed

Mandatory: <id> id <uid> uid <medias> <json list>

redis-cli --eval appendMediasToStory.lua   , uid 5834578e-351c-451a-94c6-500aa755f804 id a96970f1-fbaa-439c-892a-cec49ea6376d medias <json string>

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
for i, key in pairs({"uid", "id", "medias"}) do
    if not argv[key] then
        return key .. " missing"
    end
end

-- TODO keys computed for now (should be given by KEYS argument when calling script
local KEYstory = "z:stories:" .. argv["id"]
local KEYstoryByUser = "z:storiesByUser:" .. argv["uid"]
local KEYmediasByStory = "mediasByStory:" .. argv["id"]
local KEYstoriesPosition = "z:stories:position"
local KEYcreated = "z:stories:index:created"

-- check if story exists
if redis.call("EXISTS", KEYstory) == 0 then
    return "missing story"
end

-- check if user exists
if redis.call("EXISTS", KEYuser) == 0 then
    return "uid not found"
end

-- check if user allowed
if redis.call("SISMEMBER", KEYstoryByUser, argv["id"]) == 0 then
    return "not allowed"
end

-- append medias if not exist
local newmedias = {}
local newmedias_count = 0
local c = redis.call("LRANGE", KEYmediasByStory, 0, -1)
local currentmedias = {}
for _,id in pairs(c) do currentmedias[id] = 1 end

local pos = {}
local timestamp = nil
local data =  cjson.decode(argv["medias"])
print("inserting into " .. KEYmediasByStory)
for i,d in pairs(data) do
    if d["id"] ~= nil and currentmedias[d["id"]] ~= 1 then
        print(d["id"])
        table.insert(newmedias, d["id"])
        newmedias_count = newmedias_count+1
        -- get 1st lat/lon/timestamp from uploads
        if d["lat"] and d["lon"] and pos["lat"] == nil then
            pos["lat"] = d["lat"]
            pos["lon"] = d["lon"]
            timestamp = d["timestamp"]
        end

    end
end

if newmedias_count > 0 then
    redis.call("RPUSH", KEYmediasByStory, unpack(newmedias))
    -- update lat/lon/timestamp of story if no geo info
    if pos["lat"] and redis.call("ZSCORE", KEYstoriesPosition, argv["id"]) == false then
        redis.call("GEOADD", KEYstoriesPosition, pos["lon"], pos["lat"], argv["id"])
        redis.call("ZADD", KEYcreated, argv["created"], argv["id"])
        print("updated pos of story to " .. pos["lat"] .. "," .. pos["lon"])
    end
end
return "OK"
