package com.n9mtq4.gss.tilegen

import java.awt.image.BufferedImage

/**
 * Created by will on 7/25/20 at 2:44 PM.
 *
 * @author Will "n9Mtq4" Bresnahan
 */
@OptIn(ExperimentalStdlibApi::class)
fun equalizeHistogram(srcImg: BufferedImage): BufferedImage {
	
//	https://github.com/torywalker/histogram-equalizer/blob/master/HistogramEqualization.ipynb
	
	val newImg = BufferedImage(srcImg.width, srcImg.height, BufferedImage.TYPE_BYTE_GRAY)
	
	val histogram = getHistogram(srcImg)
	
	// clear the bin for black pixels. most of the pixels in the image are black due to the border filling in the 
	// border from the image rotation. this messes up the histogram equalization
	histogram[0] = 0L
	
	val csum = histogram
		.runningReduce { acc, i -> acc + i }
		.toLongArray()
	
	val mincs = csum.min()!!
	val maxcs = csum.max()!!
	
	val nj = csum.map { 255 * (it - mincs) }
	val N = maxcs - mincs
	
	val ncs = nj.map { it / N }
	
	for (y in 0 until srcImg.height) {
		for (x in 0 until srcImg.width) {
			
			val newGrey = ncs[getGreyFromImg(srcImg, x, y)].toInt()
			newImg.raster.setSample(x, y, 0, newGrey)
			
		}
	}
	
	return newImg
	
}

fun getHistogram(img: BufferedImage): LongArray {
	
	val histogram = LongArray(256) { 0L }
		
	for (y in 0 until img.height) {
		for (x in 0 until img.width) {
			
			val grey = getGreyFromImg(img, x, y)
			histogram[grey]++
			
		}
	}
	
	return histogram
	
}

fun getGreyFromImg(img: BufferedImage, x: Int, y: Int): Int {
	
	return img.raster.getSample(x, y, 0)
//	return img.getRGB(x, y) and 0xFF
	
}
