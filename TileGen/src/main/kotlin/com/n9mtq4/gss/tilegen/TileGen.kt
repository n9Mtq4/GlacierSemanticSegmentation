package com.n9mtq4.gss.tilegen

import java.awt.image.BufferedImage
import java.io.File
import java.io.FileNotFoundException
import javax.imageio.ImageIO

/**
 * Created by will on 7/13/20 at 6:18 PM.
 *
 * @author Will "n9Mtq4" Bresnahan
 */

const val TILE_WIDTH = 512
const val TILE_HEIGHT = 512
const val TILE_X_STRIDE = TILE_WIDTH / 2
const val TILE_Y_STRIDE = TILE_HEIGHT / 2

val SKIP_BANDS = intArrayOf(8) // landsat8 band 8 is panchromatic, so different resolution

val DATA_INPUT_DIR = File("../data/ls8")
val TILE_OUTPUT_DIR = File("../data/tiles/ls8")

data class Tile(val x1: Int, val y1: Int, val width: Int, val height: Int) {
	
	val x2: Int = x1 + width
	val y2: Int = y1 + height
	val nameString: String = "TILE${x1}_${y1}_${width}_${height}"
	
}

fun main() {
	
	TILE_OUTPUT_DIR.mkdirs()
	
	val imageDirs = DATA_INPUT_DIR.listFiles { dir, name -> File(dir, name).isDirectory }!!
	
	imageDirs.forEach { processImageDir(it) }
	
}

/**
 * Processes a directory of a landsat image.
 * Finds tiles from the truth image. Saves the bands and truth tiles in the output directory.
 * */
fun processImageDir(imageDir: File) {
	
	val imgName = imageDir.name
	val groundTruthFile = getTruthFile(imageDir)
	val otherBands = imageDir.listFiles { _, name -> name != groundTruthFile.name }!!
	
	val groundTruth = ImageIO.read(groundTruthFile)
	val tiles = findTileLocs(groundTruth).toList()
	
	// extract truth files
	val truthDir = File(TILE_OUTPUT_DIR, "truth")
	truthDir.mkdirs()
	tiles
		.map { tile -> tile to extractTile(groundTruth, tile) }
		.forEach { (tile, img) -> ImageIO.write(img, "png", File(truthDir, "${imgName}_${tile.nameString}_truth.png")) }
	
	// extract other bands
	for (bandFile in otherBands) {
		
		val bandNum = getBandFromName(bandFile.name)
		
		if (bandNum in SKIP_BANDS) continue
		
		val bandImage = ImageIO.read(bandFile)
		
		if (bandImage.width != groundTruth.width || bandImage.height != groundTruth.height) {
			println("${imageDir.name} B$bandNum doesn't match width and height. Band width = ${bandImage.width}, Band height = ${bandImage.height}, truth width = ${groundTruth.width}, truth height = ${groundTruth.height}")
			continue
		}
		
		val bandDir = File(TILE_OUTPUT_DIR, "B$bandNum")
		bandDir.mkdirs()
		
		tiles
			.map { tile -> tile to extractTile(bandImage, tile) }
			.forEach { (tile, img) -> ImageIO.write(img, "png", File(bandDir, "${imgName}_${tile.nameString}_B$bandNum.png")) }
		
	}
	
}

/**
 * Get the band number from the file name.
 * for example, LC08_L1TP_045005_20190814_20190820_01_T1_B4.TIF returns 4
 * */
fun getBandFromName(name: String): Int {
	
	val regex = """B(?<band>\d)""".toRegex()
	return regex.find(name)!!.groups["band"]!!.value.toInt()
	
}

/**
 * Returns a new buffered image of the tile from image.
 * */
fun extractTile(image: BufferedImage, tile: Tile): BufferedImage {
	
	return image.getSubimage(tile.x1, tile.y1, tile.width, tile.height)
	
}

/**
 * Gets the ground truth file from an image dir.
 * Gets the file with "truth" in its name
 * */
fun getTruthFile(dir: File): File {
	
	return dir.listFiles { _, name -> "truth" in name }?.first() ?: throw FileNotFoundException("No truth file found in ${dir.absolutePath}")
	
}

/**
 * Gets a sequence of (x1, y1) of tiles that meet the criteria for a tile to be used in the dataset.
 * The width and height of the tiles are [TILE_WIDTH] and [TILE_HEIGHT]
 * */
fun findTileLocs(groundTruth: BufferedImage) = sequence {
	
	for (y in 0 until (groundTruth.height - 2 * TILE_Y_STRIDE) step TILE_Y_STRIDE) {
		for (x in 0 until (groundTruth.width - 2 * TILE_X_STRIDE) step TILE_X_STRIDE) {
			
			if (isValidTile(groundTruth, x, y, TILE_WIDTH, TILE_HEIGHT)) {
				yield(Tile(x, y, TILE_WIDTH, TILE_HEIGHT))
			}
			
		}
	}
	
	return@sequence
	
}

/**
 * Checks if this is a good tile to use. The number of white pixels in the ground truth must be
 * greater than a threshold
 * */
fun isValidTile(groundTruth: BufferedImage, x1: Int, y1: Int, width: Int, height: Int): Boolean {
	
	val whiteColor = -1
	
	val x2 = x1 + width
	val y2 = y1 + height
	
	assert(x1 in 0 until groundTruth.width)
	assert(x2 in 0 until groundTruth.width)
	assert(y1 in 0 until groundTruth.height)
	assert(y2 in 0 until groundTruth.height)
	
	val totalPixels = width * height
	var whitePixels = 0
	
	// count number of white pixels
	for (y in y1 until y2) {
		for (x in x1 until x2) {
			
			if (groundTruth.getRGB(x, y) == whiteColor) whitePixels++
			
		}
	}
	
	return whitePixels >= (totalPixels / 20)
	
}
