import numpy as np
from keras.models import *
from keras.layers import Input, merge, Conv2D, MaxPooling2D, UpSampling2D, Dropout, Cropping2D
from keras.optimizers import *
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from keras import backend as keras
from data import dataProcess

class myUnet(object):

	def __init__(self, n_pts = 2048, img_cols = 512):

		self.n_pts = n_pts

	def load_data(self, x_data, y_data ):
		x_train = np.load(x_data)
		y_train = np.load(y_data)
		return x_train, y_train

	def get_unet(self):

		inputs = Input((self.n_pts, 3,2))

		'''
		unet with crop(because padding = valid)

		conv1 = Conv2D(64, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(inputs)
		print "conv1 shape:",conv1.shape
		conv1 = Conv2D(64, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv1)
		print "conv1 shape:",conv1.shape
		crop1 = Cropping2D(cropping=((90,90),(90,90)))(conv1)
		print "crop1 shape:",crop1.shape
		pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
		print "pool1 shape:",pool1.shape

		conv2 = Conv2D(128, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(pool1)
		print "conv2 shape:",conv2.shape
		conv2 = Conv2D(128, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv2)
		print "conv2 shape:",conv2.shape
		crop2 = Cropping2D(cropping=((41,41),(41,41)))(conv2)
		print "crop2 shape:",crop2.shape
		pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
		print "pool2 shape:",pool2.shape

		conv3 = Conv2D(256, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(pool2)
		print "conv3 shape:",conv3.shape
		conv3 = Conv2D(256, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv3)
		print "conv3 shape:",conv3.shape
		crop3 = Cropping2D(cropping=((16,17),(16,17)))(conv3)
		print "crop3 shape:",crop3.shape
		pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
		print "pool3 shape:",pool3.shape

		conv4 = Conv2D(512, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(pool3)
		conv4 = Conv2D(512, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv4)
		drop4 = Dropout(0.5)(conv4)
		crop4 = Cropping2D(cropping=((4,4),(4,4)))(drop4)
		pool4 = MaxPooling2D(pool_size=(2, 2))(drop4)

		conv5 = Conv2D(1024, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(pool4)
		conv5 = Conv2D(1024, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv5)
		drop5 = Dropout(0.5)(conv5)

		up6 = Conv2D(512, 2, activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(UpSampling2D(size = (2,2))(drop5))
		merge6 = merge([crop4,up6], mode = 'concat', concat_axis = 3)
		conv6 = Conv2D(512, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(merge6)
		conv6 = Conv2D(512, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv6)

		up7 = Conv2D(256, 2, activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(UpSampling2D(size = (2,2))(conv6))
		merge7 = merge([crop3,up7], mode = 'concat', concat_axis = 3)
		conv7 = Conv2D(256, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(merge7)
		conv7 = Conv2D(256, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv7)

		up8 = Conv2D(128, 2, activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(UpSampling2D(size = (2,2))(conv7))
		merge8 = merge([crop2,up8], mode = 'concat', concat_axis = 3)
		conv8 = Conv2D(128, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(merge8)
		conv8 = Conv2D(128, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv8)

		up9 = Conv2D(64, 2, activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(UpSampling2D(size = (2,2))(conv8))
		merge9 = merge([crop1,up9], mode = 'concat', concat_axis = 3)
		conv9 = Conv2D(64, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(merge9)
		conv9 = Conv2D(64, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv9)
		conv9 = Conv2D(2, 3, activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv9)
		'''

		conv1 = Conv2D(64, (3,3), activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(inputs)
		print "conv1 shape:",conv1.shape
		conv1 = Conv2D(64, (3,1), activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv1)
		print "conv1 shape:",conv1.shape
		pool1 = AveragePooling2D(pool_size=(2, 1))(conv1)
		print "pool1 shape:",pool1.shape

		conv2 = Conv2D(128, (3,1), activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(pool1)
		print "conv2 shape:",conv2.shape
		conv2 = Conv2D(128, (3,1), activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv2)
		print "conv2 shape:",conv2.shape
		pool2 = MaxPooling2D(pool_size=(2,1))(conv2)
		print "pool2 shape:",pool2.shape

		conv3 = Conv2D(256, (3,1), activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(pool2)
		print "conv3 shape:",conv3.shape
		conv3 = Conv2D(256, (3,1), activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv3)
		print "conv3 shape:",conv3.shape
		pool3 = MaxPooling2D(pool_size=(2,1))(conv3)
		print "pool3 shape:",pool3.shape

		conv4 = Conv2D(512, (3,1), activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(pool3)
		conv4 = Conv2D(512, (3,1), activation = 'relu', padding = 'valid', kernel_initializer = 'glorot_normal')(conv4)
		drop4 = Dropout(0.5)(conv4)
		pool4 = MaxPooling2D(pool_size=(2,1))(drop4)

		conv5 = Conv2D(1024, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(pool4)
		conv5 = Conv2D(1024, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(conv5)
		drop5 = Dropout(0.5)(conv5)
		pool5 = MaxPooling2D(pool_size=(2,1))(drop5)


		conv6 = Conv2D(2048, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(pool5)
		conv6 = Conv2D(2048, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(conv6)
		drop6 = Dropout(0.5)(conv6)


		up7 = Conv2D(1024, (2,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(UpSampling2D(size = (2,2))(drop6))
		merge7 = merge([drop5,up7], mode = 'concat', concat_axis = 3)
		conv7 = Conv2D(1024, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(merge7)
		conv7 = Conv2D(1024, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(conv7)

		up8 = Conv2D(512, (2,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(UpSampling2D(size = (2,2))(conv7))
		merge8 = merge([drop4,up8], mode = 'concat', concat_axis = 3)
		conv8 = Conv2D(512, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(merge8)
		conv8 = Conv2D(512, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(conv8)

		up9 = Conv2D(256, (2,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(UpSampling2D(size = (2,2))(conv8))
		merge9 = merge([conv3,up9], mode = 'concat', concat_axis = 3)
		conv9 = Conv2D(256, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(merge9)
		conv9 = Conv2D(256, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(conv9)

		up10 = Conv2D(128, (2,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(UpSampling2D(size = (2,2))(conv9))
		merge10 = merge([conv2,up10], mode = 'concat', concat_axis = 3)
		conv10 = Conv2D(128, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(merge10)
		conv10 = Conv2D(128, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(conv10)

		up11 = Conv2D(64, (2,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(UpSampling2D(size = (2,2))(conv10))
		merge11 = merge([conv1,up11], mode = 'concat', concat_axis = 3)
		conv11 = Conv2D(64, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(merge11)
		conv11 = Conv2D(32,(3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(conv11)
		conv11 = Conv2D(16, (3,1), activation = 'relu', padding = 'same', kernel_initializer = 'glorot_normal')(conv11)
		conv11 = Conv2D(6, (3,1), activation = 'softmax_', padding = 'same', kernel_initializer = 'glorot_normal')(conv11)

		model = Model(input = inputs, output = conv11)

		model.compile(optimizer = Adam(lr = 1e-4), loss = 'binary_crossentropy', metrics = ['accuracy'])

		return model


	def train(self):

		print("loading data")
		imgs_train, imgs_mask_train, imgs_test = self.load_data()
		print("loading data done")
		model = self.get_unet()
		print("got unet")

		model_checkpoint = ModelCheckpoint('unet.hdf5', monitor='loss',verbose=1, save_best_only=True)
		print('Fitting model...')
		model.fit(imgs_train, imgs_mask_train, batch_size=1, nb_epoch=10, verbose=1, shuffle=True, callbacks=[model_checkpoint])

		print('predict test data')
		imgs_mask_test = model.predict(imgs_test, batch_size=1, verbose=1)
		np.save('imgs_mask_test.npy', imgs_mask_test)


if __name__ == '__main__':
	myunet = myUnet()
	myunet.train()
