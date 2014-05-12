import google0
import google1
import google2
import google3
import google4
import google5
import google6
import google7
import google8
import google9
import googleA

g0 = google0.dict1
print(len(g0))
g1 = google1.dict1
print(len(g1))
g2 = google2.dict1
print(len(g2))
g3 = google3.dict1
print(len(g3))
g4 = google4.dict1
print(len(g4))
g5 = google5.dict1
print(len(g5))
g6 = google6.dict1
print(len(g6))
g7 = google7.dict1
print(len(g7))
g8 = google8.dict1
print(len(g8))
g9 = google9.dict1
print(len(g9))
gA = googleA.dict1
print(len(gA))
big_dict = {}
print gA['he,will']
dictList = [g0, g1, g2, g3, g4, g5, g6, g7, g8, g9, gA]
#big_dict = reduce(lambda x, y: x.update(y), dictList)
for d in dictList:
    big_dict.update(d)
print len(big_dict)
