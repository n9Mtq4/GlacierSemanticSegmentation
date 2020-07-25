package com.n9mtq4.gss.tilegen

import java.awt.image.BufferedImage
import kotlin.math.roundToInt

/**
 * Created by will on 7/25/20 at 4:59 PM.
 *
 * @author Will "n9Mtq4" Bresnahan
 */
fun stretchToMinMax(img: BufferedImage): BufferedImage {
	
	val newImg = BufferedImage(img.width, img.height, BufferedImage.TYPE_BYTE_GRAY)
	
	// get the min and max value
	var min = Int.MAX_VALUE
	var max = Int.MIN_VALUE
	for (y in 0 until img.height) {
		for (x in 0 until img.width) {
			
			val grey = img.raster.getSample(x, y, 0)
			@Suppress("ConvertTwoComparisonsToRangeCheck")
			if (grey < min && grey >= 3) min = grey // min will always be 0 with black rotation border, so make it at least 3
			if (grey > max) max = grey
			
		}
	}
	
	val scale = 255.0 / (max - min).toDouble()
	
	// stretch the new image
	for (y in 0 until img.height) {
		for (x in 0 until img.width) {
			
			val oldGrey = img.raster.getSample(x, y, 0)
			val newGrey = ((oldGrey - min) * scale).roundToInt().coerceIn(0, 255)
			newImg.raster.setSample(x, y, 0, newGrey)
			
		}
	}
	
	return newImg
	
}
