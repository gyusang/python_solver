A = []
a = [1,2,3,4,5]
b = [1,3,5,7,9]
for i in range(5):
	c = []
	c.append((0,(7+2*i)%10))
	c.append((a[i],b[i]))
	c.append((a[(i+1)%5],(b[(i+1)%5]+2)%10))
	A.append(c)
	c = []
	c.append((0,(8+2*i)%10))
	c.append((a[(i+1)%5],(b[(i+1)%5]+1)%10))
	A.append(c)

B = []
a = [2,3,4,5,1]
b = [2,4,6,8,0]
for i in range(5):
	c = []
	c.append((a[i],(b[i]+4)%10))
	c.append((a[i-1],b[i-1]))
	B.append(c)

C = []
a = [9,10,6,7,8]
aa = [7,9,1,3,5]
b = [4,3,2,1,5]
bb = [3,1,9,7,5]
for i in range(5):
	c = []
	c.append((a[(i+1)%5],(aa[(i+1)%5]+6)%10))
	c.append((a[i],aa[i]))
	c.append((b[i],bb[i]))
	C.append(c)
	c = []
	c.append((a[(i+1)%5],(aa[(i+1)%5]+7)%10))
	c.append((b[i],(bb[i]+9)%10))
	C.append(c)
	c = []
	c.append((a[(i+1)%5],(aa[(i+1)%5]+8)%10))
	c.append((b[i],(bb[i]+8)%10))
	c.append((b[(i+1)%5],(bb[(i+1)%5]+2)%10))
	C.append(c)
	c = []
	c.append((a[(i+1)%5],(aa[(i+1)%5]+9)%10))
	c.append((b[(i+1)%5],(bb[(i+1)%5]+1)%10))
	C.append(c)

D = []
a = [10,6,7,8,9]
b = [0,2,4,6,8]
for i in range(5):
	c = []
	c.append((a[i],(b[i]+4)%10))
	c.append((a[i-1],b[i-1]))
	D.append(c)

E = []
a = [9,10,6,7,8]
b = [9,1,3,5,7]
for i in range(5):
	c = []
	c.append((11,(7+2*i)%10))
	c.append((a[i],b[i]))
	c.append((a[(i+1)%5],(b[(i+1)%5]+2)%10))
	E.append(c)
	c = []
	c.append((11,(8+2*i)%10))
	c.append((a[(i+1)%5],(b[(i+1)%5]+1)%10))
	E.append(c)

change = [A,B,C,D,E]
import json
with open("blockinfo.txt","w") as file:
	json.dump(change,file)
