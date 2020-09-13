package com.n9mtq4.gss.tilegen

import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO

/**
 * Created by will on 9/10/20 at 5:18 PM.
 *
 * @author Will "n9Mtq4" Bresnahan
 */
class SatImg(val bandsFiles: List<File>, val landSat: Int = 8) {
	
	val bands = HashMap<Int, BufferedImage>()
	
	init {
		
		bandsFiles
			.map { getBandFromName(it.name) to ImageIO.read(it) }
			.forEach { (bandNum, img) -> bands[bandNum] = img }
		
	}
	
	fun firstBand() = bands.values.first()
	
	operator fun get(bandNum: Int): BufferedImage =  bands[bandNum]!!
	
	fun ndsi(): BufferedImage {
		
		val greenBand = when (landSat) {
			8 -> 3
			else -> -1
		}
		val swirBand = when(landSat) {
			8 -> 6
			else -> -1
		}
		
		val greenImg = this[greenBand]
		val swirImg = this[swirBand]
		
		// calculate ndsi
		val ndsiRaster = imgMath(greenImg, swirImg) { green, swir ->
			(green - swir).toDouble() / (green + swir + 1).toDouble()
		}
		
		scaleRasterTo255(ndsiRaster, min = -0.4, max = 1.0)
		
		// set ndwi pixel values to that of the raster
 		val ndsi = BufferedImage(greenImg.width, greenImg.height, greenImg.type)
 		forPixels(ndsi.width, ndsi.height) { x, y ->
 			ndsi.raster.setSample(x, y, 0, ndsiRaster[x][y].toInt())
// 			ndsi.raster.setSample(x, y, 1, ndsiRaster[x][y].toInt())
// 			ndsi.raster.setSample(x, y, 2, ndsiRaster[x][y].toInt())
 		}
 		
 		return ndsi
		
	}
	
	fun ndwi(): BufferedImage {
		
		val greenBand = when (landSat) {
			8 -> 3
			else -> -1
		}
		val nirBand = when (landSat) {
			8 -> 5
			7 -> 4
			else -> -1
		}
		val swirBand = when(landSat) {
			8 -> 6
			7 -> 5
			else -> -1
		}
		
		val greenImg = this[greenBand]
		val nirImg = this[nirBand]
		val swirImg = this[swirBand]
		
		// calculate ndwi
		val ndwiRaster = imgMath(greenImg, nirImg) { green, nir ->
			(green - nir).toDouble() / (green + nir + 1).toDouble()
		}
		
		scaleRasterTo255(ndwiRaster, min = -0.3, max = 0.2)
		
		// set ndwi pixel values to that of the raster
		val ndwi = BufferedImage(nirImg.width, nirImg.height, nirImg.type)
		forPixels(ndwi.width, ndwi.height) { x, y ->
			ndwi.raster.setSample(x, y, 0, ndwiRaster[x][y].toInt())
//			ndwi.raster.setSample(x, y, 1, ndwiRaster[x][y].toInt())
//			ndwi.raster.setSample(x, y, 2, ndwiRaster[x][y].toInt())
		}
		
		return ndwi
		
	}
	
}
