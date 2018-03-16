import json

dic = {"good" : 115
,"movies" : 126
,"films" : 147
,"this" : 149
,"classic" : 161
,"buzz" : 167
,"it" : 182
,"toys" : 191
,"woody" : 191
,"time" : 196
,"characters" : 203
,"great" : 240
,"animated" : 243
,"animation" : 276
,"the" : 300
,"pixar" : 342
,"film" : 504
,"movie" : 519
,"toy" : 534
,"story" : 612}

result = []
for x in dic:
    result.append(json.dumps({"text":x,"weight":dic[x]}))
print result
