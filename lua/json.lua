local json = {}

function json.serialize(inp)
	local out=""
	--do nothing now
	return out	
end

function json.deserialize(...)
	local out
	local str = ""
	--concate all inputs
	local args={...}
	for _,s in pairs(args) do str=str..tostring(s) end
	--find '{'
	local state = "start"
	local frst = string.find(str, '{')
	local last = string.find(str, '}[^}]*$')-- [^}] = something that not contain }, *$ - end of line
	if frst==nil or last==nil then
		print("Can't find { or }")
	else
		print("Found { at "..tostring(frst))
		print("Found } at "..tostring(last))
	end
	return out
end

function json.help()
	print("serialize(<any object>) - store object as JSON string")
	print("deserialize(string[, ...]) - get object from JSON string")
end

return json