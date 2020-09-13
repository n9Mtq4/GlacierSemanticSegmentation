package com.n9mtq4.gss.tilegen

import java.awt.image.BufferedImage
import kotlin.math.roundToInt

/**
 * Created by will on 9/10/20 at 5:38 PM.
 *
 * @author Will "n9Mtq4" Bresnahan
 */

inline fun forPixels(width: Int, height: Int, body: (Int, Int) -> Unit) {
	for (y in 0 until height) {
		for (x in 0 until width) {
			body(x, y)
		}
	}
}

inline fun imgMath(i1: BufferedImage, i2: BufferedImage, band: Int = 0, func: (Int, Int) -> Double): Array<DoubleArray> {
	
	val outputRaster = Array(i1.width) { DoubleArray(i1.height) { 0.0 } }
	
	forPixels(i1.width, i1.height) { x, y ->
		
		val i1Val = i1.raster.getSample(x, y, band)
		val i2Val = i2.raster.getSample(x, y, band)
		
		outputRaster[x][y] = func(i1Val, i2Val)
		
	}
	
	return outputRaster
	
}

fun scaleRasterTo255(raster: Array<DoubleArray>, min: Double? = null, max: Double? = null) {
	
	val minVal = min ?: d2RasterMin(raster)
	val maxVal = max ?: d2RasterMax(raster)
	val scale = 255.0 / (maxVal - minVal)
	
	forPixels(raster.size, raster[0].size) { x, y ->
		raster[x][y] = ((raster[x][y] - minVal) * scale).coerceIn(0.0, 255.0)
	}
	
}

fun d2RasterMax(raster: Array<DoubleArray>): Double {
	return raster.map { it.max()!! }.max()!!
}

fun d2RasterMin(raster: Array<DoubleArray>): Double {
	return raster.map { it.min()!! }.min()!!
}
