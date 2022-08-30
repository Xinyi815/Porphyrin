# first neural network with keras tutorial
import tensorflow as tf
from numpy import loadtxt
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# load the dataset
dataset = loadtxt('total_data_free.txt', delimiter=',')

# split into input (X) and output (y) variables
X = dataset[:, 0:27]
#print(f'X = {X}')
y = dataset[:, 29]

# define the keras model
model = Sequential()
model.add(Dense(30, input_shape=(27,),activation='relu'))
model.add(Dense(25, ))
model.add(Dense(20, ))
model.add(Dense(15, ))
model.add(Dense(10, ))
model.add(Dense(5,))
model.add(Dense(1,))


# compile the keras model
print('Compiling model...')
metrics=['mse', 'mae', 'mape', 'cosine_proximity']

model.compile(
    loss='mae',
    optimizer='adam', 
    metrics=metrics,
    )

# fit the keras model on the dataset
print('Training model...')
historial = model.fit(X, y, epochs=1000, batch_size=18, verbose=True)
print("Model trained!")


# Metrics plots
fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(historial.history['mae'])
axs[0, 0].set_title('MAE')

axs[0, 1].plot(historial.history['cosine_proximity'])
axs[0, 1].set_title('Cosine Proximity')
plt.tight_layout()
#plt.savefig("metrics_free.png")

# evaluate the keras model
evaluation = model.evaluate(X, y)
print('======= Metrics ========')
print('Loss: %.3f' % (evaluation[0]))
print('MSE: %.3f' % (evaluation[1]))
print('MAE: %.3f' % (evaluation[2]))
print('MAPE: %.3f' % (evaluation[3]))
print(f'Accuracy: {100 - evaluation[3]}')
print('Cosine proximity: %.3f' % (evaluation[4]))
print('========================')


# make predictions with the model
predictions = model.predict(X)
# summarize the first 9 cases
for i in range(10):
    print('%s => %.4f (expected %.4f)' % (X[i].tolist(), predictions[i], y[i]))

# save model and architecture to single file
model.save("model_free_noEAIP.h5")
print("Saved model to disk")

n = list(range(len(X)))
i = [2,3,4,5,6,7,8,9,10]
plt.subplot(212)
plt.title('raw HL and prediction (free)')
plt.plot(i, y[:9], color='blue', marker='o', label='raw data')
plt.plot(i, predictions[:9], color='red', marker='o', label='prediction ')
plt.xlabel('No of porphyrin units')
plt.ylabel('HL gap/eV')
plt.legend()
plt.tight_layout()
plt.savefig("free_noEAIP.png")

# new 5 instances where we do not know the answer: H_C8_20, H_C8_30, H_C8_40, H_C8_50 and H_C8_100
Xnew = np.array([[7268.08,2610,572,40,80,80,40,80,0,0,0,0,0,0,0,40,40,0,80,0,0,0,0,0,0,8,20],[10589.08,3810,832,60,120,120,60,120,0,0,0,0,0,0,0,60,60,0,120,0,0,0,0,0,0,8,30],[13910.08,5010,1092,80,160,160,80,160,0,0,0,0,0,0,0,80,80,0,160,0,0,0,0,0,0,8,40],[17231.08,6210,1352,100,200,200,100,200,0,0,0,0,0,0,0,100,100,0,200,0,0,0,0,0,0,8,50],[33836.08,12210,2652,200,400,400,200,400,0,0,0,0,0,0,0,200,200,0,400,0,0,0,0,0,0,8,100]])
# make a prediction
ynew = model.predict(Xnew)
# show the inputs and predicted outputs
print("X=%s, Predicted=%s" % (Xnew.tolist(), ynew))