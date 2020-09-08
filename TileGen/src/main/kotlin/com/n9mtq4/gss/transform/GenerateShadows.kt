package com.n9mtq4.gss.transform

import com.n9mtq4.gss.tilegen.TILE_HEIGHT
import com.n9mtq4.gss.tilegen.TILE_WIDTH
import java.awt.image.BufferedImage
import kotlin.math.exp
import kotlin.math.sqrt
import kotlin.random.Random

/**
 * Created by will on 9/7/20 at 8:10 PM.
 *
 * @author Will "n9Mtq4" Bresnahan
 */

fun main() {
	
	val img = BufferedImage(TILE_WIDTH, TILE_HEIGHT, BufferedImage.TYPE_INT_RGB)
	
	val mask = createShadowMask(img.width, img.height, 0)
	
	for (y in 0 until img.height) {
		for (x in 0 until img.width) {
			
			val gray = (255 * mask[x][y]).toInt()
			img.setRGB(x, y, rgb2int(gray, gray, gray))
			
		}
	}
	
	println("perlin noise test done")
	
}

fun applyShadow(tile: BufferedImage, seed: Int): BufferedImage {
	
	val shadowed = BufferedImage(tile.width, tile.height, tile.type)
	val shadowMask = createShadowMask(shadowed.width, shadowed.height, seed)
	
	for (y in 0 until shadowed.height) {
		for (x in 0 until shadowed.width) {
			
			val grey = tile.raster.getSample(x, y, 0)
			val shadowGrey = (grey * shadowMask[x][y]).toInt()
			
			shadowed.raster.setSample(x, y, 0, shadowGrey)
			
		}
	}
	
	return shadowed
	
}

fun createShadowMask(width: Int = TILE_WIDTH, height: Int = TILE_HEIGHT, seed: Int, scale : Double = 0.008): Array<DoubleArray> {
	
	val z = 4.2
	val random = Random(seed)
	val noiseXOff = random.nextInt(0, 10000)
	val noiseYOff = random.nextInt(0, 10000)
	val darkness = random.nextDouble(0.4, 0.8)
	
	return Array(width) { x -> 
		val nx = scale * x + noiseXOff
		DoubleArray(height) { y ->
			val ny = scale * y + noiseYOff
			(darkness + rampFunc(Perlin.noise(nx, ny, z))).coerceIn(0.0, 1.0)
		}
	}
	
}

fun sigmoid(x: Double) = 1.0 / (1.0 + exp(-x))

fun rampFunc(noise: Double, threshold: Double = -0.2, steepness: Double = 200.0): Double {
	val noiseRange = sqrt(3.0 / 4.0)
	return sigmoid(steepness * ((noise / noiseRange) - threshold))
}

fun rgb2int(r: Int, g: Int, b: Int): Int {
	return ((r and 255) shl 16) or ((g and 255) shl 8) or ((b and 255) shl 0)
}
