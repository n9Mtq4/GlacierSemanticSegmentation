package com.n9mtq4.gss.tilegen

import com.n9mtq4.gss.transform.applyShadow
import java.awt.image.BufferedImage
import java.io.File
import java.io.FileNotFoundException
import javax.imageio.ImageIO

/**
 * Created by will on 7/13/20 at 6:18 PM.
 *
 * @author Will "n9Mtq4" Bresnahan
 */

const val TILE_WIDTH = 256
const val TILE_HEIGHT = 256
const val TILE_X_STRIDE = TILE_WIDTH / 2
const val TILE_Y_STRIDE = TILE_HEIGHT / 2

const val NO_TRANSFORMS = false

val INCLUDE_BANDS = intArrayOf(1, 2, 3, 4, 5, 6, 7)

val DATA_INPUT_DIR = File("../data/test")
val TILE_OUTPUT_DIR = File("../data/tiles/test")

val FULL_IMGS = arrayOf<String>(
//	"LC08_L1TP_045005_20190814_20190820_01_T1",
//	"LE07_L1TP_040005_20020719_20170129_01_T1"
)

data class Tile(val x1: Int, val y1: Int, val width: Int, val height: Int) {
	
	val x2: Int = x1 + width
	val y2: Int = y1 + height
	val nameString: String = "TILE${x1}_${y1}_${width}_${height}"
	
}

fun main() {
	
	tileGenGeneration()
	
}

fun tileGenGeneration() {
	
	TILE_OUTPUT_DIR.mkdirs()
	
//	val tileAllImgs = listOf("LC08_L1TP_044006_20150711_20170227_01_T1")
	val tileAllImgs = FULL_IMGS
//	val tileAllImgs = emptyArray<String>()
	
	val imageDirs = DATA_INPUT_DIR.listFiles { dir, name -> File(dir, name).isDirectory }!!
	
	imageDirs.forEach { processImageDir(it, it.name in tileAllImgs) }
	
}

/**
 * Processes a directory of a landsat image.
 * Finds tiles from the truth image. Saves the bands and truth tiles in the output directory.
 * */
fun processImageDir(imageDir: File, tileAll: Boolean) {
	
	println("Generating tiles for ${imageDir.name}")
	
	val imgName = imageDir.name
	val groundTruthFile = getTruthFile(imageDir)
	val otherBands = imageDir.listFiles { _, name -> name != groundTruthFile.name }!!
		.filter { it.extension in arrayOf("png", "jpg", "jpeg") }
	
	val groundTruth = ImageIO.read(groundTruthFile)
	val firstBand = ImageIO.read(otherBands.first())
	val tiles = findTileLocs(groundTruth, firstBand, tileAll).toList()
	
	// extract truth files
	val truthDir = File(TILE_OUTPUT_DIR, "truth")
	truthDir.mkdirs()
	tiles
		.map { tile -> tile to extractTile(groundTruth, tile) }
		.map { (tile, img) -> tile to applyTileTransformations(tile, img, -1) }
		.forEach { (tile, imgs) -> writeTileGroup(imgName, "", truthDir, tile, imgs) }
	
	// extract other bands
	for (bandFile in otherBands) {
		
		val bandNum = getBandFromName(bandFile.name)
		
		if (bandNum !in INCLUDE_BANDS) continue
		
		val bandImage = ImageIO.read(bandFile)
		
		if (bandImage.width != groundTruth.width || bandImage.height != groundTruth.height) {
			println("${imageDir.name} B$bandNum doesn't match width and height. Band width = ${bandImage.width}, Band height = ${bandImage.height}, truth width = ${groundTruth.width}, truth height = ${groundTruth.height}")
			continue
		}
		
		val bandDir = File(TILE_OUTPUT_DIR, "B$bandNum")
		bandDir.mkdirs()
		
		// try mean and std match from http://www.fmwconcepts.com/imagemagick/index.php matchimage
//		val adjBandImage = stretchToMinMax(bandImage)
		val adjBandImage = bandImage
		
		tiles
			.map { tile -> tile to extractTile(adjBandImage, tile) }
			.map { (tile, img) -> tile to applyTileTransformations(tile, img, bandNum) }
			.forEach { (tile, imgs) -> writeTileGroup(imgName, "", bandDir, tile, imgs) }
		
	}
	
}

/**
 * Writes out a group of tiles
 * */
fun writeTileGroup(imgName: String, bandStr: String, bandDir: File, tile: Tile, imgs: List<BufferedImage>) {
	
	val tileNamePrefix = "${imgName}_${tile.nameString}_$bandStr"
	
	imgs
		.map { img2ByteGray(it) }
		.forEachIndexed { index, img -> 
			ImageIO.write(img, "png", File(bandDir, "${tileNamePrefix}_T${index}.png"))
		}
	
}

fun img2ByteGray(img: BufferedImage): BufferedImage {
	
	// early return if already correct type
	if (img.type == BufferedImage.TYPE_BYTE_GRAY) return img
	
	val byteImg = BufferedImage(img.width, img.height, BufferedImage.TYPE_BYTE_GRAY)
	
	// conversion path for binary
	if (img.type == BufferedImage.TYPE_BYTE_BINARY) {
		forPixels(img.width, img.height) { x, y ->
			val color = img.raster.getSample(x, y, 0) * 255
			byteImg.raster.setSample(x, y, 0, color)
		}
	}
	
	// conversion path for ushort
	if (img.type == BufferedImage.TYPE_USHORT_GRAY) {
		forPixels(img.width, img.height) { x, y ->
			val color = img.raster.getSample(x, y, 0) shr 8
			byteImg.raster.setSample(x, y, 0, color)
		}
	}
	
	return byteImg
	
}

/**
 * Apply transformations to a tile.
 * Does rotation, y-reflection
 * */
fun applyTileTransformations(tile: Tile, tileImg: BufferedImage, band: Int): List<BufferedImage> {
	
	if (NO_TRANSFORMS) return listOf(tileImg)
	
	if (band < 0) return listOf(tileImg, tileImg)
	
	val seed = tile.x1 * tile.x2 * tile.y1 * tile.y2
	val shadowedTileImg = applyShadow(tileImg, seed)
	
	return listOf(tileImg, shadowedTileImg)
	
}

/**
 * Mirrors a buffered image along the y-axis
 * */
fun mirrorImage(tileImg: BufferedImage): BufferedImage {
	
	val width = tileImg.width
	val height = tileImg.height
	val mirroredTile = BufferedImage(width, height, tileImg.type)
	
	for (y in 0 until height) {
		for (x in 0 until width) {
			
			mirroredTile.setRGB(width - x - 1, y, tileImg.getRGB(x, y))
			
		}
	}
	
	return mirroredTile
	
}

/**
 * Rotate a buffered image 90 degrees
 * https://stackoverflow.com/a/52663539/5196460
 * */
fun rotateImageClockwise90(src: BufferedImage): BufferedImage {
	val width = src.width
	val height = src.height
	val dest = BufferedImage(height, width, src.type) // rotation swaps width and height
	val graphics2D = dest.createGraphics()
	graphics2D.translate((height - width) / 2, (height - width) / 2)
	graphics2D.rotate(Math.PI / 2, height / 2.toDouble(), width / 2.toDouble())
	graphics2D.drawRenderedImage(src, null)
	return dest
}

/**
 * Get the band number from the file name.
 * for example, LC08_L1TP_045005_20190814_20190820_01_T1_B4.TIF returns 4
 * */
fun getBandFromName(name: String): Int {
	
	val regex = """B(?<band>\d)""".toRegex()
	return regex.find(name)?.groups?.get("band")?.value?.toInt() ?: throw IllegalArgumentException("Can't extract band number from '$name'")
	
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
fun findTileLocs(groundTruth: BufferedImage, firstBand: BufferedImage, tileAll: Boolean) = sequence {
	
	for (y in 0 until (groundTruth.height - 2 * TILE_Y_STRIDE) step TILE_Y_STRIDE) {
		for (x in 0 until (groundTruth.width - 2 * TILE_X_STRIDE) step TILE_X_STRIDE) {
			
			if ((tileAll && tileNotBlack(firstBand, x, y, TILE_WIDTH, TILE_HEIGHT)) || isValidTile(groundTruth, x, y, TILE_WIDTH, TILE_HEIGHT)) {
				yield(Tile(x, y, TILE_WIDTH, TILE_HEIGHT))
			}
			
		}
	}
	
	return@sequence
	
}

fun tileNotBlack(band: BufferedImage, x1: Int, y1: Int, width: Int, height: Int): Boolean {
	
	val blackColor = -16777216
	
	val x2 = x1 + width
	val y2 = y1 + height
	
	assert(x1 in 0 until band.width)
	assert(x2 in 0 until band.width)
	assert(y1 in 0 until band.height)
	assert(y2 in 0 until band.height)
	
	val totalPixels = width * height
	var blackPixels = 0
	
	// count number of white pixels
	for (y in y1 until y2) {
		for (x in x1 until x2) {
			
			if (band.getRGB(x, y) == blackColor) blackPixels++
			
		}
	}
	
	return blackPixels < (12 * (totalPixels / 20))
	
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
	
	return (whitePixels >= (totalPixels / 60)) // && (whitePixels <= (29 * (totalPixels / 30)))
	
}
