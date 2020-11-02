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


def rebnconv_block(
    inputs,
    filters = 3,
    dirate = 1,
    afunc = 'swish',
    dropout = 0.0,
    kernel_initializer="he_normal",
    padding="same"
):
    conv = Conv2D(
        filters,
        3,
        kernel_initializer=kernel_initializer,
        padding=padding,
        dilation_rate=(dirate, dirate),
    )(inputs)
    bn = BatchNormalization()(conv)
    if dropout > 0.0:
        bn = SpatialDropout2D(dropout)(bn)
    activation = Activation(afunc)(bn)
    return activation


# In[ ]:


def rsu4f(inputs, in_ch=3, mid_ch=12, out_ch=3, enc_dropout=0.0, dec_dropout=0.0):
    rebnconvin = rebnconv_block(inputs, out_ch, dropout=enc_dropout)
    
    rebnconv1 = rebnconv_block(rebnconvin, mid_ch, dirate=1, dropout=enc_dropout)
    rebnconv2 = rebnconv_block(rebnconv1, mid_ch, dirate=2, dropout=enc_dropout)
    rebnconv3 = rebnconv_block(rebnconv2, mid_ch, dirate=4, dropout=enc_dropout)
    
    rebnconv4 = rebnconv_block(rebnconv3, mid_ch, dirate=8, dropout=dec_dropout)
    
    rebnconv3d = rebnconv_block(concatenate([rebnconv4, rebnconv3]), mid_ch, dirate=4, dropout=dec_dropout)
    rebnconv2d = rebnconv_block(concatenate([rebnconv3d, rebnconv2]), mid_ch, dirate=2, dropout=dec_dropout)
    rebnconv1d = rebnconv_block(concatenate([rebnconv2d, rebnconv1]), out_ch, dirate=1, dropout=dec_dropout)
    
    return rebnconv1d


# In[ ]:


def rsu4(inputs, in_ch=3, mid_ch=12, out_ch=3, enc_dropout=0.0, dec_dropout=0.0):
    rebnconvin = rebnconv_block(inputs, out_ch, dropout=enc_dropout)
    
    rebnconv1 = rebnconv_block(rebnconvin, mid_ch, dirate=1, dropout=enc_dropout)
    pool1 = MaxPooling2D((2, 2))(rebnconv1)
    rebnconv2 = rebnconv_block(pool1, mid_ch, dirate=1, dropout=enc_dropout)
    pool2 = MaxPooling2D((2, 2))(rebnconv2)
    rebnconv3 = rebnconv_block(pool2, mid_ch, dirate=1, dropout=enc_dropout)
    
    rebnconv4 = rebnconv_block(rebnconv3, mid_ch, dirate=2, dropout=dec_dropout)
    
    rebnconv3d = rebnconv_block(concatenate([rebnconv4, rebnconv3]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv3dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv3d)
    rebnconv2d = rebnconv_block(concatenate([rebnconv3dup, rebnconv2]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv2dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv2d)
    rebnconv1d = rebnconv_block(concatenate([rebnconv2dup, rebnconv1]), out_ch, dirate=1, dropout=dec_dropout)
    
    return rebnconv1d


# In[ ]:


def rsu5(inputs, in_ch=3, mid_ch=12, out_ch=3, enc_dropout=0.0, dec_dropout=0.0):
    rebnconvin = rebnconv_block(inputs, out_ch, dropout=enc_dropout)
    
    rebnconv1 = rebnconv_block(rebnconvin, mid_ch, dirate=1, dropout=enc_dropout)
    pool1 = MaxPooling2D((2, 2))(rebnconv1)
    rebnconv2 = rebnconv_block(pool1, mid_ch, dirate=1, dropout=enc_dropout)
    pool2 = MaxPooling2D((2, 2))(rebnconv2)
    rebnconv3 = rebnconv_block(pool2, mid_ch, dirate=1, dropout=enc_dropout)
    pool3 = MaxPooling2D((2, 2))(rebnconv3)
    rebnconv4 = rebnconv_block(pool3, mid_ch, dirate=1, dropout=enc_dropout)
    
    rebnconv5 = rebnconv_block(rebnconv4, mid_ch, dirate=2, dropout=dec_dropout)
    
    rebnconv4d = rebnconv_block(concatenate([rebnconv5, rebnconv4]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv4dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv4d)
    rebnconv3d = rebnconv_block(concatenate([rebnconv4dup, rebnconv3]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv3dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv3d)
    rebnconv2d = rebnconv_block(concatenate([rebnconv3dup, rebnconv2]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv2dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv2d)
    rebnconv1d = rebnconv_block(concatenate([rebnconv2dup, rebnconv1]), out_ch, dirate=1, dropout=dec_dropout)
    
    return rebnconv1d


# In[ ]:


def rsu6(inputs, in_ch=3, mid_ch=12, out_ch=3, enc_dropout=0.0, dec_dropout=0.0):
    rebnconvin = rebnconv_block(inputs, out_ch, dropout=enc_dropout)
    
    rebnconv1 = rebnconv_block(rebnconvin, mid_ch, dirate=1, dropout=enc_dropout)
    pool1 = MaxPooling2D((2, 2))(rebnconv1)
    rebnconv2 = rebnconv_block(pool1, mid_ch, dirate=1, dropout=enc_dropout)
    pool2 = MaxPooling2D((2, 2))(rebnconv2)
    rebnconv3 = rebnconv_block(pool2, mid_ch, dirate=1, dropout=enc_dropout)
    pool3 = MaxPooling2D((2, 2))(rebnconv3)
    rebnconv4 = rebnconv_block(pool3, mid_ch, dirate=1, dropout=enc_dropout)
    pool4 = MaxPooling2D((2, 2))(rebnconv4)
    rebnconv5 = rebnconv_block(pool4, mid_ch, dirate=1, dropout=enc_dropout)
    
    rebnconv6 = rebnconv_block(rebnconv5, mid_ch, dirate=2, dropout=dec_dropout)
    
    rebnconv5d = rebnconv_block(concatenate([rebnconv6, rebnconv5]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv5dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv5d)
    rebnconv4d = rebnconv_block(concatenate([rebnconv5dup, rebnconv4]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv4dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv4d)
    rebnconv3d = rebnconv_block(concatenate([rebnconv4dup, rebnconv3]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv3dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv3d)
    rebnconv2d = rebnconv_block(concatenate([rebnconv3dup, rebnconv2]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv2dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv2d)
    rebnconv1d = rebnconv_block(concatenate([rebnconv2dup, rebnconv1]), out_ch, dirate=1, dropout=dec_dropout)
    
    return rebnconv1d


# In[ ]:


def rsu7(inputs, in_ch=3, mid_ch=12, out_ch=3, enc_dropout=0.0, dec_dropout=0.0):
    rebnconvin = rebnconv_block(inputs, out_ch, dropout=enc_dropout)
    
    rebnconv1 = rebnconv_block(rebnconvin, mid_ch, dirate=1, dropout=enc_dropout)
    pool1 = MaxPooling2D((2, 2))(rebnconv1)
    rebnconv2 = rebnconv_block(pool1, mid_ch, dirate=1, dropout=enc_dropout)
    pool2 = MaxPooling2D((2, 2))(rebnconv2)
    rebnconv3 = rebnconv_block(pool2, mid_ch, dirate=1, dropout=enc_dropout)
    pool3 = MaxPooling2D((2, 2))(rebnconv3)
    rebnconv4 = rebnconv_block(pool3, mid_ch, dirate=1, dropout=enc_dropout)
    pool4 = MaxPooling2D((2, 2))(rebnconv4)
    rebnconv5 = rebnconv_block(pool4, mid_ch, dirate=1, dropout=enc_dropout)
    pool5 = MaxPooling2D((2, 2))(rebnconv5)
    rebnconv6 = rebnconv_block(pool5, mid_ch, dirate=1, dropout=enc_dropout)
    
    rebnconv7 = rebnconv_block(rebnconv6, mid_ch, dirate=2, dropout=dec_dropout)
    
    rebnconv6d = rebnconv_block(concatenate([rebnconv7, rebnconv6]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv6dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv6d)
    rebnconv5d = rebnconv_block(concatenate([rebnconv6dup, rebnconv5]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv5dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv5d)
    rebnconv4d = rebnconv_block(concatenate([rebnconv5dup, rebnconv4]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv4dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv4d)
    rebnconv3d = rebnconv_block(concatenate([rebnconv4dup, rebnconv3]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv3dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv3d)
    rebnconv2d = rebnconv_block(concatenate([rebnconv3dup, rebnconv2]), mid_ch, dirate=1, dropout=dec_dropout)
    rebnconv2dup = UpSampling2D((2, 2), interpolation='bilinear')(rebnconv2d)
    rebnconv1d = rebnconv_block(concatenate([rebnconv2dup, rebnconv1]), out_ch, dirate=1, dropout=dec_dropout)
    
    return rebnconv1d


# In[ ]:


def u2net_block(
    inputs,
    in_ch = 3,
    out_ch = 1,
    kernel_initializer = 'he_normal',
    padding = 'same',
    inter_enc_dropout = 0.0,
    inter_dec_dropout = 0.0,
    enc_intra_enc_dropout = 0.0,
    enc_intra_dec_dropout = 0.0,
    dec_intra_enc_dropout = 0.0,
    dec_intra_dec_dropout = 0.0,
):
    stage1 = rsu7(inputs, in_ch, 32, 64, enc_intra_enc_dropout, enc_intra_dec_dropout)
    if inter_enc_dropout > 0.0:
        stage1 = SpatialDropout2D(inter_enc_dropout)(stage1)
    pool12 = MaxPooling2D((2, 2))(stage1)
    stage2 = rsu6(pool12, 64, 32, 128, enc_intra_enc_dropout, enc_intra_dec_dropout)
    if inter_enc_dropout > 0.0:
        stage2 = SpatialDropout2D(inter_enc_dropout)(stage2)
    pool23 = MaxPooling2D((2, 2))(stage2)
    stage3 = rsu5(pool23, 128, 64, 256, enc_intra_enc_dropout, enc_intra_dec_dropout)
    if inter_enc_dropout > 0.0:
        stage3 = SpatialDropout2D(inter_enc_dropout)(stage3)
    pool34 = MaxPooling2D((2, 2))(stage3)
    stage4 = rsu4(pool34, 256, 128, 512, enc_intra_enc_dropout, enc_intra_dec_dropout)
    if inter_enc_dropout > 0.0:
        stage4 = SpatialDropout2D(inter_enc_dropout)(stage4)
    pool45 = MaxPooling2D((2, 2))(stage4)
    stage5 = rsu4f(pool45, 512, 256, 512, enc_intra_enc_dropout, enc_intra_dec_dropout)
    if inter_enc_dropout > 0.0:
        stage5 = SpatialDropout2D(inter_enc_dropout)(stage5)
    pool56 = MaxPooling2D((2, 2))(stage5)
    
    stage6 = rsu4f(pool56, 512, 256, 512, dec_intra_enc_dropout, dec_intra_dec_dropout)
    if inter_dec_dropout > 0.0:
        stage6 = SpatialDropout2D(inter_dec_dropout)(stage6)
    stage6up = UpSampling2D((2, 2), interpolation='bilinear')(stage6)
    
    stage5d = rsu4f(concatenate([stage6up, stage5]), 1024, 256, 512, dec_intra_enc_dropout, dec_intra_dec_dropout)
    if inter_dec_dropout > 0.0:
        stage5d = SpatialDropout2D(inter_dec_dropout)(stage5d)
    stage5dup = UpSampling2D((2, 2), interpolation='bilinear')(stage5d)
    stage4d = rsu4(concatenate([stage5dup, stage4]), 1024, 128, 256, dec_intra_enc_dropout, dec_intra_dec_dropout)
    if inter_dec_dropout > 0.0:
        stage4d = SpatialDropout2D(inter_dec_dropout)(stage4d)
    stage4dup = UpSampling2D((2, 2), interpolation='bilinear')(stage4d)
    stage3d = rsu5(concatenate([stage4dup, stage3]), 512, 64, 128, dec_intra_enc_dropout, dec_intra_dec_dropout)
    if inter_dec_dropout > 0.0:
        stage3d = SpatialDropout2D(inter_dec_dropout)(stage3d)
    stage3dup = UpSampling2D((2, 2), interpolation='bilinear')(stage3d)
    stage2d = rsu6(concatenate([stage3dup, stage2]), 256, 32, 64, dec_intra_enc_dropout, dec_intra_dec_dropout)
    if inter_dec_dropout > 0.0:
        stage2d = SpatialDropout2D(inter_dec_dropout)(stage2d)
    stage2dup = UpSampling2D((2, 2), interpolation='bilinear')(stage2d)
    stage1d = rsu6(concatenate([stage2dup, stage1]), 128, 16, 64, dec_intra_enc_dropout, dec_intra_dec_dropout)
    if inter_dec_dropout > 0.0:
        stage1d = SpatialDropout2D(inter_dec_dropout)(stage1d)
    
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
    
    def sig(x, n):
        return Activation('sigmoid', name=n)(x)
    
    return sig(d0, 'ad0'), sig(d1, 'ad1'), sig(d2, 'ad2'), sig(d3, 'ad3'), sig(d4, 'ad4'), sig(d5, 'ad5'), sig(d6, 'ad6')


# In[ ]:


def u2netp_block(
    inputs,
    in_ch = 3,
    out_ch = 1,
    kernel_initializer = 'he_normal',
    padding = 'same',
    inter_enc_dropout = 0.0,
    inter_dec_dropout = 0.0,
    enc_intra_enc_dropout = 0.0,
    enc_intra_dec_dropout = 0.0,
    dec_intra_enc_dropout = 0.0,
    dec_intra_dec_dropout = 0.0,
):
    stage1 = rsu7(inputs, in_ch, 16, 64, enc_intra_enc_dropout, enc_intra_dec_dropout)
    if inter_enc_dropout > 0.0:
        stage1 = SpatialDropout2D(inter_enc_dropout)(stage1)
    pool12 = MaxPooling2D((2, 2))(stage1)
    stage2 = rsu6(pool12, 64, 16, 64, enc_intra_enc_dropout, enc_intra_dec_dropout)
    if inter_enc_dropout > 0.0:
        stage2 = SpatialDropout2D(inter_enc_dropout)(stage2)
    pool23 = MaxPooling2D((2, 2))(stage2)
    stage3 = rsu5(pool23, 64, 16, 64, enc_intra_enc_dropout, enc_intra_dec_dropout)
    if inter_enc_dropout > 0.0:
        stage3 = SpatialDropout2D(inter_enc_dropout)(stage3)
    pool34 = MaxPooling2D((2, 2))(stage3)
    stage4 = rsu4(pool34, 64, 16, 64, enc_intra_enc_dropout, enc_intra_dec_dropout)
    if inter_enc_dropout > 0.0:
        stage4 = SpatialDropout2D(inter_enc_dropout)(stage4)
    pool45 = MaxPooling2D((2, 2))(stage4)
    stage5 = rsu4f(pool45, 64, 16, 64, enc_intra_enc_dropout, enc_intra_dec_dropout)
    if inter_enc_dropout > 0.0:
        stage5 = SpatialDropout2D(inter_enc_dropout)(stage5)
    pool56 = MaxPooling2D((2, 2))(stage5)
    
    stage6 = rsu4f(pool56, 64, 16, 64, dec_intra_enc_dropout, dec_intra_dec_dropout)
    if inter_dec_dropout > 0.0:
        stage6 = SpatialDropout2D(inter_dec_dropout)(stage6)
    stage6up = UpSampling2D((2, 2), interpolation='bilinear')(stage6)
    
    stage5d = rsu4f(concatenate([stage6up, stage5]), 128, 16, 64, dec_intra_enc_dropout, dec_intra_dec_dropout)
    if inter_dec_dropout > 0.0:
        stage5d = SpatialDropout2D(inter_dec_dropout)(stage5d)
    stage5dup = UpSampling2D((2, 2), interpolation='bilinear')(stage5d)
    stage4d = rsu4(concatenate([stage5dup, stage4]), 128, 16, 64, dec_intra_enc_dropout, dec_intra_dec_dropout)
    if inter_dec_dropout > 0.0:
        stage4d = SpatialDropout2D(inter_dec_dropout)(stage4d)
    stage4dup = UpSampling2D((2, 2), interpolation='bilinear')(stage4d)
    stage3d = rsu5(concatenate([stage4dup, stage3]), 128, 16, 64, dec_intra_enc_dropout, dec_intra_dec_dropout)
    if inter_dec_dropout > 0.0:
        stage3d = SpatialDropout2D(inter_dec_dropout)(stage3d)
    stage3dup = UpSampling2D((2, 2), interpolation='bilinear')(stage3d)
    stage2d = rsu6(concatenate([stage3dup, stage2]), 128, 16, 64, dec_intra_enc_dropout, dec_intra_dec_dropout)
    if inter_dec_dropout > 0.0:
        stage2d = SpatialDropout2D(inter_dec_dropout)(stage2d)
    stage2dup = UpSampling2D((2, 2), interpolation='bilinear')(stage2d)
    stage1d = rsu6(concatenate([stage2dup, stage1]), 128, 16, 64, dec_intra_enc_dropout, dec_intra_dec_dropout)
    if inter_dec_dropout > 0.0:
        stage1d = SpatialDropout2D(inter_dec_dropout)(stage1d)
    
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
    
    def sig(x, n):
        return Activation('sigmoid', name=n)(x)
    
    return sig(d0, 'ad0'), sig(d1, 'ad1'), sig(d2, 'ad2'), sig(d3, 'ad3'), sig(d4, 'ad4'), sig(d5, 'ad5'), sig(d6, 'ad6')


# In[ ]:

if __name__ == "__main__":
    inputs = Input((256, 256, 1))
    sides = u2net_block(inputs)
    
    model = Model(inputs=[inputs], outputs=sides)
    
    print(model.summary())



# In[ ]:





# In[ ]:




