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
local err_elms = ""
local err_count = 0
for i, key in pairs({"uid", "id", "medias"}) do
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
local KEYmediasByStory = "z:mediasByStory:" .. argv["id"]
local KEYstoriesPosition = "z:stories:position"
local KEYcreated = "z:stories:index:created"
local KEYuser = "z:users:" .. argv["uid"]

-- check if story exists
if redis.call("EXISTS", KEYstory) == 0 then
    return "missing story"
end

-- check if user exists
if redis.call("EXISTS", KEYuser) == 0 then
    return "uid not found"
end

-- check if user allowed
if redis.call("ZSCORE", KEYstoryByUser, argv["id"]) == false then
    return "not allowed "
end

-- append medias if not exist
local newmedias = {}
local newmedias_count = 0
local c = redis.call("LRANGE", KEYmediasByStory, 0, -1)
local currentmedias = {}
for _,id in pairs(c) do currentmedias[id] = 1 end

local pos = {}
local created = nil
local data =  cjson.decode(argv["medias"])
-- print("inserting into " .. KEYmediasByStory)
for i,d in pairs(data) do
    if d["id"] ~= nil and currentmedias[d["id"]] ~= 1 then
        -- print(d["relative_url"])
        -- insert <3 digits from id>/<id>.<type> eg 8/7/f/87f0865f-7547-4402-bf84-582ff5655097.jpeg
        table.insert(newmedias, d["relative_url"])
        newmedias_count = newmedias_count+1
        -- get 1st lat/lon/created from uploads
        if d["lat"] and d["lon"] and pos["lat"] == nil then
            pos["lat"] = d["lat"]
            pos["lon"] = d["lon"]
            created = d["created"]
        end

    end
end

if newmedias_count > 0 then
    redis.call("RPUSH", KEYmediasByStory, unpack(newmedias))
    -- update lat/lon/created of story if no geo info
    if pos["lat"] and redis.call("ZSCORE", KEYstoriesPosition, argv["id"]) == false then
        redis.call("GEOADD", KEYstoriesPosition, pos["lon"], pos["lat"], argv["id"])
        redis.call("ZADD", KEYcreated, created, argv["id"])
        -- print("updated pos of story to " .. pos["lat"] .. "," .. pos["lon"])
    end
end
return "OK"
