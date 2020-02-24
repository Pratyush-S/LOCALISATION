#importing libraries
import tensorflow as tf
import pandas as pd
import numpy as np
from keras.models import model_from_json
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD,Adam
import os.path
import json
import matplotlib.pyplot as plt

seed = 124
np.random.seed(seed)


dataset1 = pd.read_excel(r'D:\PS!\LOCALISATION\raw_data\channel_info_data_2nov.xlsx')   
print("a")     
dataset2 = pd.read_excel(r'D:\PS!\LOCALISATION\raw_data\channel_info_data_4nov.xlsx')        
print("b")
dataset3 = pd.read_excel(r'D:\PS!\LOCALISATION\raw_data\channel_info_data_5nov.xlsx')        
print("c")
dataset4 = pd.read_excel(r'D:\PS!\LOCALISATION\raw_data\channel_info_data_6nov.xlsx')        
print("d")
dataset5 = pd.read_excel(r'D:\PS!\LOCALISATION\raw_data\channel_info_data_7nov.xlsx')        
print("e")



frames=[dataset1, dataset2, dataset3]
dataset = pd.concat(frames)
dataset =dataset.reset_index(drop=True)




dataset=dataset1


avg_val=(dataset[col[0]]+dataset[col[1]]+dataset[col[2]]+dataset[col[3]]+dataset[col[4]]+dataset[col[5]]+dataset[col[6]]+dataset[col[7]]+dataset[col[8]]+dataset[col[9]])/6


diffz1=pd.Series((avg_val-dataset['CO2_Zone_1']))
diffz2=pd.DataFrame((avg_val-dataset['CO2_Zone_2']))
diffz3=pd.DataFrame((avg_val-dataset['CO2_Zone_3']))
diffz4=pd.DataFrame((avg_val-dataset['CO2_Zone_4']))
diffz5=pd.DataFrame((avg_val-dataset['CO2_Zone_5']))
diffz6=pd.DataFrame((avg_val-dataset['CO2_Zone_6']))
    
   
  
  
    #creating dataframe for deviation from mean
    frames2=[diffz1,diffz2,diffz3,diffz4,diffz5,diffz6]
    dataset_2=pd.concat(frames2, axis=1)
    dataset_2.columns=['dif1','dif2','dif3','dif4','dif5','dif6']
    dataset=pd.concat([dataset,dataset_2],axis=1)
#    dataset['humid_f']=dataset['humid_f']*10

    #  Shuffle Data
    #The frac keyword argument specifies the fraction of rows to return in the random sample
    #so frac=1 means return all rows (in random order)
    #https://stackoverflow.com/questions/29576430/shuffle-dataframe-rows
    
    dataset = dataset.reset_index(drop=True)
    col=dataset.columns.values
    dataset=dataset.drop(col[0],axis=1)
  
    


col=dataset.columns

X_complete=dataset[['a1', 'a1c','a2', 'a2c', 'a3', 'a3c', 'a4', 'a4c', 'a5', 'a5c']]
y_complete=dataset[[ 'seat']]


col=list(X_complete.columns.values)

for i in col:#[:-1]:
    avg=X_complete[str(i)].mean()
    sd=X_complete[str(i)].std()
    X_complete[str(i)]=X_complete[str(i)].apply(lambda X:(X-avg)/(sd))
    print(avg)
    print(sd)
    print(i)



X_complete=X_complete.values
y_complete=pd.get_dummies(y_complete['seat']).values



# Creating a Train and a Test Dataset
X_train, X_test, y_train, y_test = train_test_split(X_complete, y_complete, test_size=0.2, random_state=seed)



# Define Neural Network model layers
model = Sequential()
model.add(Dense(10, input_dim=10, activation='relu'))
#model.add(Dense(10, input_dim=11, activation='softmax'))
model.add(Dense(120, activation='relu'))
model.add(Dense(20, activation='relu'))

model.add(Dense(12, activation='softmax'))
# Compile model
model.compile(Adam(lr=0.0001),'categorical_crossentropy',metrics=['accuracy'])




if os.path.isfile('@new_model_severityl.h5'):

    # Model reconstruction from JSON file
    json_file = open('new_model_severity.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    
    # Load weights into the new model
    model.load_weights('new_model_severity.h5')
    print("Model weights loaded from saved model data.")

    model.compile(Adam(lr=0.01),'categorical_crossentropy',metrics=['accuracy'])
else:
    print("Model weights data not found. Model will be fit on training set now.")

    # Fit model on training data - try to replicate the normal input
    history=model.fit(X_train,y_train,epochs=200,batch_size=200,verbose=1,validation_data=(X_test,y_test))
    
 
         # Save parameters to JSON file
    model_json = model.to_json()
    with open("diffusion_severity_detect.json", "w") as json_file:
        json_file.write(model_json)

    # Save model weights to file
    model.save_weights('diffusion_severity_detect.h5')


model.summary()
                

# Model predictions for test set
y_pred = model.predict(X_complete)
y_test_class = np.argmax(y_complete,axis=1)
y_pred_class = np.argmax(y_pred,axis=1)

print(y_test_class,y_pred_class)
#print(y_pred_class)


# Evaluate model on test data
score = model.evaluate(X_complete,y_complete, batch_size=128,verbose=1)
 
# Compute stats on the test set and Output all results
from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_test_class,y_pred_class))
print(confusion_matrix(y_test_class,y_pred_class))


plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.legend(['train', 'test'], loc='upper left')