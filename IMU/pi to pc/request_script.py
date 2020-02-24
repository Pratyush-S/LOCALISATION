# importing the requests library 
import requests 
  
# api-endpoint 
addrs = "http://192.168.1.191"
  
# location given here 
port = "8050"
  
# defining a params dict for the parameters to be sent to the API 
url=addrs+':'+port  
# sending get request and saving the response as response object 

r = requests.get(url)   

data = r.json() 
    print(data)
    b=data.keys()
  


r=requests.get('http://192.168.1.191:8050')

acc=[]
gry=[]
mag=[]

for i in b:
        print(i[0])
        if i[0]=='A': 
            acc.append(data[i])
        elif i[0]=='G':
            gry.append(data[i])
        else:
            mag.append(data[i])
        
            