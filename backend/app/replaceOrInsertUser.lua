--[[

Replace if email belongs to user (and email free)
Inserts if email free
Mandatory: uid <uid> email <email>

redis-cli --eval replaceOrInsertUser.lua   , uid 5834578e-351c-451a-94c6-500aa755f80 email test@zweierlei.org ...

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
for i, key in pairs({"uid", "email"}) do
    if not argv[key] or argv[key] == "None" then
        err_elms = err_elms .. key .. ","
        err_count = err_count+1
    end
end

if err_count > 0 then
    return "required element:" .. err_elms:sub(1, -2)
end


local uid = argv["uid"]
argv["uid"] = nil

-- TODO keys computed for now (should be given by KEYS argument when calling script
local KEYallEmails = "z:allEmails"
local KEYusers = "z:users:" .. uid
local KEYusersByEmail = "z:usersByEmail:"

local emailRegistered = redis.call("SISMEMBER", KEYallEmails, argv["email"])
local currentEmail = redis.call("HMGET", KEYusers, "email")[1] -- oldemail

if currentEmail ~= argv["email"] and emailRegistered == 1 then
    return "exists:email"
else
    -- for simplicity always remove (and potentially re-add below)
    if currentEmail then
        redis.call("DEL", KEYusersByEmail .. currentEmail)
        redis.call("SREM", KEYallEmails, currentEmail)
    end

    redis.call("SET", KEYusersByEmail .. argv["email"], uid)
    redis.call("SADD", KEYallEmails, argv["email"])
    -- we replace *all* user data with given data! (not given keys are deleted)
    redis.call("DEL", KEYusers)
    local argvPacked = {}
    for k,v in pairs(argv) do table.insert(argvPacked, k) table.insert(argvPacked, v) end
    return redis.call("HMSET", KEYusers, unpack(argvPacked))

end
