
data=[170,85,6,1,4,360,0]

data=[170,85,3,4,1,3]


data1=[hex(i) for i in data]

c=hex(0)

i=2

for i in range(2,len(data)):
    
    c=int(c, 16)^int(data1[i], 16)
    c=hex(c)
    print(c)
    print(i)
    print(data1[i])
    
    i=i+1