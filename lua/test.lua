local js = require "json"

local obj = {}
obj['x']=5
obj['y']=10
obj['name']='Dummy'

local str = '{"x":5,"y":10,"name":"Dummy"}'

local str_out = js.serialize(obj)
if str_out~=str then
	print("MISMATCH serialize")
	print("EXPECT:  ",str)
	print("RECEIVED:",str_out)
end

local obj_out = js.deserialize(str)
print("obj:")
if obj_out~=obj then
	print("MISMATCH deserialize")
end
