#!/usr/bin/env python
# coding: utf-8

# U^2 Net - https://github.com/NathanUA/U-2-Net/blob/master/model/u2net.py
# 
# Based off of implementation https://github.com/NathanUA/U-2-Net/blob/master/model/u2net.py

# In[ ]:


import tensorflow as tf


# In[ ]:


from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    BatchNormalization,
    Conv2D,
    Conv2DTranspose,
    MaxPooling2D,
    Dropout,
    SpatialDropout2D,
    UpSampling2D,
    Input,
    concatenate,
    multiply,
    add,
    Activation,
    GlobalAveragePooling2D,
    Dense,
    Multiply,
    Input,
)
from tensorflow.keras import backend as K


# In[ ]:


def rebnconv_block(inputs, filters = 3, dirate = 1, afunc = 'relu', kernel_initializer="he_normal", padding="same"):
    conv = Conv2D(
        filters,
        3,
        kernel_initializer=kernel_initializer,
        padding=padding,
        dilation_rate=(dirate, dirate),
    )(inputs)
    bn = BatchNormalization()(conv)
    activation = Activation(afunc)(bn)
    return activation


# In[ ]:


def rsu4f(inputs, in_ch=3, mid_ch=12, out_ch=3):
    rebnconvin = rebnconv_block(inputs, out_ch)
    
    rebnconv1 = rebnconv_block(rebnconvin, mid_ch, dirate=1)
    rebnconv2 = rebnconv_block(rebnconv1, mid_ch, dirate=2)
    rebnconv3 = rebnconv_block(rebnconv2, mid_ch, dirate=4)
    
    rebnconv4 = rebnconv_block(rebnconv3, mid_ch, dirate=8)
    
    rebnconv3d = rebnconv_block(concatenate([rebnconv4, rebnconv3]), mid_ch, dirate=4)
    rebnconv2d = rebnconv_block(concatenate([rebnconv3d, rebnconv2]), mid_ch, dirate=2)
    rebnconv1d = rebnconv_block(concatenate([rebnconv2d, rebnconv1]), out_ch, dirate=1)
    
    return rebnconv1d


# In[ ]:


def rsu4(inputs, in_ch=3, mid_ch=12, out_ch=3):
    rebnconvin = rebnconv_block(inputs, out_ch)
    
    rebnconv1 = rebnconv_block(rebnconvin, mid_ch, dirate=1)
    pool1 = MaxPooling2D((2, 2))(rebnconv1)
    rebnconv2 = rebnconv_block(pool1, mid_ch, dirate=1)
    pool2 = MaxPooling2D((2, 2))(rebnconv2)
    rebnconv3 = rebnconv_block(pool2, mid_ch, dirate=1)
    
    rebnconv4 = rebnconv_block(rebnconv3, mid_ch, dirate=2)
    
    rebnconv3d = rebnconv_block(concatenate([rebnconv4, rebnconv3]), mid_ch, dirate=1)
    rebnconv3dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv3d)
    rebnconv2d = rebnconv_block(concatenate([rebnconv3dup, rebnconv2]), mid_ch, dirate=1)
    rebnconv2dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv2d)
    rebnconv1d = rebnconv_block(concatenate([rebnconv2dup, rebnconv1]), out_ch, dirate=1)
    
    return rebnconv1d


# In[ ]:


def rsu5(inputs, in_ch=3, mid_ch=12, out_ch=3):
    rebnconvin = rebnconv_block(inputs, out_ch)
    
    rebnconv1 = rebnconv_block(rebnconvin, mid_ch, dirate=1)
    pool1 = MaxPooling2D((2, 2))(rebnconv1)
    rebnconv2 = rebnconv_block(pool1, mid_ch, dirate=1)
    pool2 = MaxPooling2D((2, 2))(rebnconv2)
    rebnconv3 = rebnconv_block(pool2, mid_ch, dirate=1)
    pool3 = MaxPooling2D((2, 2))(rebnconv3)
    rebnconv4 = rebnconv_block(pool3, mid_ch, dirate=1)
    
    rebnconv5 = rebnconv_block(rebnconv4, mid_ch, dirate=2)
    
    rebnconv4d = rebnconv_block(concatenate([rebnconv5, rebnconv4]), mid_ch, dirate=1)
    rebnconv4dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv4d)
    rebnconv3d = rebnconv_block(concatenate([rebnconv4dup, rebnconv3]), mid_ch, dirate=1)
    rebnconv3dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv3d)
    rebnconv2d = rebnconv_block(concatenate([rebnconv3dup, rebnconv2]), mid_ch, dirate=1)
    rebnconv2dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv2d)
    rebnconv1d = rebnconv_block(concatenate([rebnconv2dup, rebnconv1]), out_ch, dirate=1)
    
    return rebnconv1d


# In[ ]:


def rsu6(inputs, in_ch=3, mid_ch=12, out_ch=3):
    rebnconvin = rebnconv_block(inputs, out_ch)
    
    rebnconv1 = rebnconv_block(rebnconvin, mid_ch, dirate=1)
    pool1 = MaxPooling2D((2, 2))(rebnconv1)
    rebnconv2 = rebnconv_block(pool1, mid_ch, dirate=1)
    pool2 = MaxPooling2D((2, 2))(rebnconv2)
    rebnconv3 = rebnconv_block(pool2, mid_ch, dirate=1)
    pool3 = MaxPooling2D((2, 2))(rebnconv3)
    rebnconv4 = rebnconv_block(pool3, mid_ch, dirate=1)
    pool4 = MaxPooling2D((2, 2))(rebnconv4)
    rebnconv5 = rebnconv_block(pool4, mid_ch, dirate=1)
    
    rebnconv6 = rebnconv_block(rebnconv5, mid_ch, dirate=2)
    
    rebnconv5d = rebnconv_block(concatenate([rebnconv6, rebnconv5]), mid_ch, dirate=1)
    rebnconv5dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv5d)
    rebnconv4d = rebnconv_block(concatenate([rebnconv5dup, rebnconv4]), mid_ch, dirate=1)
    rebnconv4dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv4d)
    rebnconv3d = rebnconv_block(concatenate([rebnconv4dup, rebnconv3]), mid_ch, dirate=1)
    rebnconv3dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv3d)
    rebnconv2d = rebnconv_block(concatenate([rebnconv3dup, rebnconv2]), mid_ch, dirate=1)
    rebnconv2dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv2d)
    rebnconv1d = rebnconv_block(concatenate([rebnconv2dup, rebnconv1]), out_ch, dirate=1)
    
    return rebnconv1d


# In[ ]:


def rsu7(inputs, in_ch=3, mid_ch=12, out_ch=3):
    rebnconvin = rebnconv_block(inputs, out_ch)
    
    rebnconv1 = rebnconv_block(rebnconvin, mid_ch, dirate=1)
    pool1 = MaxPooling2D((2, 2))(rebnconv1)
    rebnconv2 = rebnconv_block(pool1, mid_ch, dirate=1)
    pool2 = MaxPooling2D((2, 2))(rebnconv2)
    rebnconv3 = rebnconv_block(pool2, mid_ch, dirate=1)
    pool3 = MaxPooling2D((2, 2))(rebnconv3)
    rebnconv4 = rebnconv_block(pool3, mid_ch, dirate=1)
    pool4 = MaxPooling2D((2, 2))(rebnconv4)
    rebnconv5 = rebnconv_block(pool4, mid_ch, dirate=1)
    pool5 = MaxPooling2D((2, 2))(rebnconv5)
    rebnconv6 = rebnconv_block(pool5, mid_ch, dirate=1)
    
    rebnconv7 = rebnconv_block(rebnconv6, mid_ch, dirate=2)
    
    rebnconv6d = rebnconv_block(concatenate([rebnconv7, rebnconv6]), mid_ch, dirate=1)
    rebnconv6dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv6d)
    rebnconv5d = rebnconv_block(concatenate([rebnconv6dup, rebnconv5]), mid_ch, dirate=1)
    rebnconv5dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv5d)
    rebnconv4d = rebnconv_block(concatenate([rebnconv5dup, rebnconv4]), mid_ch, dirate=1)
    rebnconv4dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv4d)
    rebnconv3d = rebnconv_block(concatenate([rebnconv4dup, rebnconv3]), mid_ch, dirate=1)
    rebnconv3dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv3d)
    rebnconv2d = rebnconv_block(concatenate([rebnconv3dup, rebnconv2]), mid_ch, dirate=1)
    rebnconv2dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv2d)
    rebnconv1d = rebnconv_block(concatenate([rebnconv2dup, rebnconv1]), out_ch, dirate=1)
    
    return rebnconv1d


# In[ ]:


def u2net_block(inputs, in_ch = 3, out_ch = 1, kernel_initializer = 'he_normal', padding = 'same'):
    stage1 = rsu7(inputs, in_ch, 32, 64)
    pool12 = MaxPooling2D((2, 2))(stage1)
    stage2 = rsu6(pool12, 64, 32, 128)
    pool23 = MaxPooling2D((2, 2))(stage2)
    stage3 = rsu5(pool23, 128, 64, 256)
    pool34 = MaxPooling2D((2, 2))(stage3)
    stage4 = rsu4(pool34, 256, 128, 512)
    pool45 = MaxPooling2D((2, 2))(stage4)
    stage5 = rsu4f(pool45, 512, 256, 512)
    pool56 = MaxPooling2D((2, 2))(stage5)
    
    stage6 = rsu4f(pool56, 512, 256, 512)
    stage6up = UpSampling2D((2, 2), interpolation='bilinear')(stage6)
    
    stage5d = rsu4f(concatenate([stage6up, stage5]), 1024, 256, 512)
    stage5dup = UpSampling2D((2, 2), interpolation='bilinear')(stage5d)
    stage4d = rsu4(concatenate([stage5dup, stage4]), 1024, 128, 256)
    stage4dup = UpSampling2D((2, 2), interpolation='bilinear')(stage4d)
    stage3d = rsu5(concatenate([stage4dup, stage3]), 512, 64, 128)
    stage3dup = UpSampling2D((2, 2), interpolation='bilinear')(stage3d)
    stage2d = rsu6(concatenate([stage3dup, stage2]), 256, 32, 64)
    stage2dup = UpSampling2D((2, 2), interpolation='bilinear')(stage2d)
    stage1d = rsu6(concatenate([stage2dup, stage1]), 128, 16, 64)
    
    side1 = Conv2D(out_ch, 3, kernel_initializer=kernel_initializer, padding=padding)(stage1d)
    side2 = Conv2D(out_ch, 3, kernel_initializer=kernel_initializer, padding=padding)(stage2d)
    side3 = Conv2D(out_ch, 3, kernel_initializer=kernel_initializer, padding=padding)(stage3d)
    side4 = Conv2D(out_ch, 3, kernel_initializer=kernel_initializer, padding=padding)(stage4d)
    side5 = Conv2D(out_ch, 3, kernel_initializer=kernel_initializer, padding=padding)(stage5d)
    side6 = Conv2D(out_ch, 3, kernel_initializer=kernel_initializer, padding=padding)(stage6)
    
    d1 = side1
    d2 = UpSampling2D((2, 2), interpolation='bilinear')(side2)
    d3 = UpSampling2D((4, 4), interpolation='bilinear')(side3)
    d4 = UpSampling2D((8, 8), interpolation='bilinear')(side4)
    d5 = UpSampling2D((16, 16), interpolation='bilinear')(side5)
    d6 = UpSampling2D((32, 32), interpolation='bilinear')(side6)
    
    d0 = Conv2D(
        out_ch, 3,
        kernel_initializer=kernel_initializer,
        padding=padding
    )(concatenate([d1, d2, d3, d4, d5, d6]))
    
    def sig(x):
        return Activation('sigmoid')(x)
    
    return sig(d0), sig(d1), sig(d2), sig(d3), sig(d4), sig(d5), sig(d6)


# In[ ]:


def u2netp_block(inputs, in_ch = 3, out_ch = 1, kernel_initializer = 'he_normal', padding = 'same'):
    stage1 = rsu7(inputs, in_ch, 16, 64)
    pool12 = MaxPooling2D((2, 2))(stage1)
    stage2 = rsu6(pool12, 64, 16, 64)
    pool23 = MaxPooling2D((2, 2))(stage2)
    stage3 = rsu5(pool23, 64, 16, 64)
    pool34 = MaxPooling2D((2, 2))(stage3)
    stage4 = rsu4(pool34, 64, 16, 64)
    pool45 = MaxPooling2D((2, 2))(stage4)
    stage5 = rsu4f(pool45, 64, 16, 64)
    pool56 = MaxPooling2D((2, 2))(stage5)
    
    stage6 = rsu4f(pool56, 64, 16, 64)
    stage6up = UpSampling2D((2, 2), interpolation='bilinear')(stage6)
    
    stage5d = rsu4f(concatenate([stage6up, stage5]), 128, 16, 64)
    stage5dup = UpSampling2D((2, 2), interpolation='bilinear')(stage5d)
    stage4d = rsu4(concatenate([stage5dup, stage4]), 128, 16, 64)
    stage4dup = UpSampling2D((2, 2), interpolation='bilinear')(stage4d)
    stage3d = rsu5(concatenate([stage4dup, stage3]), 128, 16, 64)
    stage3dup = UpSampling2D((2, 2), interpolation='bilinear')(stage3d)
    stage2d = rsu6(concatenate([stage3dup, stage2]), 128, 16, 64)
    stage2dup = UpSampling2D((2, 2), interpolation='bilinear')(stage2d)
    stage1d = rsu6(concatenate([stage2dup, stage1]), 128, 16, 64)
    
    side1 = Conv2D(out_ch, 3, kernel_initializer=kernel_initializer, padding=padding)(stage1d)
    side2 = Conv2D(out_ch, 3, kernel_initializer=kernel_initializer, padding=padding)(stage2d)
    side3 = Conv2D(out_ch, 3, kernel_initializer=kernel_initializer, padding=padding)(stage3d)
    side4 = Conv2D(out_ch, 3, kernel_initializer=kernel_initializer, padding=padding)(stage4d)
    side5 = Conv2D(out_ch, 3, kernel_initializer=kernel_initializer, padding=padding)(stage5d)
    side6 = Conv2D(out_ch, 3, kernel_initializer=kernel_initializer, padding=padding)(stage6)
    
    d1 = side1
    d2 = UpSampling2D((2, 2), interpolation='bilinear')(side2)
    d3 = UpSampling2D((4, 4), interpolation='bilinear')(side3)
    d4 = UpSampling2D((8, 8), interpolation='bilinear')(side4)
    d5 = UpSampling2D((16, 16), interpolation='bilinear')(side5)
    d6 = UpSampling2D((32, 32), interpolation='bilinear')(side6)
    
    d0 = Conv2D(
        out_ch, 3,
        kernel_initializer=kernel_initializer,
        padding=padding
    )(concatenate([d1, d2, d3, d4, d5, d6]))
    
    def sig(x):
        return Activation('sigmoid')(x)
    
    return sig(d0), sig(d1), sig(d2), sig(d3), sig(d4), sig(d5), sig(d6)


# In[ ]:

if __name__ == "__main__":
    inputs = Input((256, 256, 1))
    sides = u2net_block(inputs)
    
    model = Model(inputs=[inputs], outputs=sides)
    
    print(model.summary())



# In[ ]:





# In[ ]:




