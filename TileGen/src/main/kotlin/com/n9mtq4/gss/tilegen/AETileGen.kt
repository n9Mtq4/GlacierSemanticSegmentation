package com.n9mtq4.gss.tilegen

import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO

/**
 * Created by will on 9/8/20 at 9:36 PM.
 *
 * @author Will "n9Mtq4" Bresnahan
 */

val DATA_AE_INPUT_DIR = File("../data/ls78_ae")
val TILE_AE_OUTPUT_DIR = File("../data/tiles/ls78_ae")

fun main() {
	
	TILE_AE_OUTPUT_DIR.mkdirs()
	
//	val tileAllImgs = listOf("LC08_L1TP_044006_20150711_20170227_01_T1")
//	val tileAllImgs = FULL_IMGS
	val tileAllImgs = emptyArray<String>()
	
	val imageDirs = DATA_AE_INPUT_DIR.listFiles { dir, name -> File(dir, name).isDirectory }!!
	
	imageDirs.forEach { processAEImageDir(it, it.name in tileAllImgs) }
	
}

/**
 * Processes a directory of a landsat image.
 * Finds tiles from the truth image. Saves the bands and truth tiles in the output directory.
 * */
fun processAEImageDir(imageDir: File, tileAll: Boolean) {
	
	val imgName = imageDir.name
	val otherBands = imageDir.listFiles()!!
	
	val firstBand = ImageIO.read(otherBands.first())
	val allTiles = findAllTileLocs(firstBand, tileAll)
		.toList()
	
	val tiles = allTiles
		.shuffled()
		.take(allTiles.size / 4)
	
	// extract other bands
	for (bandFile in otherBands) {
		
		val bandNum = getBandFromName(bandFile.name)
		
		if (bandNum !in INCLUDE_BANDS) continue
		
		val bandImage = ImageIO.read(bandFile)
		
//		if (bandImage.width != groundTruth.width || bandImage.height != groundTruth.height) {
//			println("${imageDir.name} B$bandNum doesn't match width and height. Band width = ${bandImage.width}, Band height = ${bandImage.height}, truth width = ${groundTruth.width}, truth height = ${groundTruth.height}")
//			continue
//		}
		
		val bandDir = File(TILE_AE_OUTPUT_DIR, "B$bandNum")
		bandDir.mkdirs()
		
		// try mean and std match from http://www.fmwconcepts.com/imagemagick/index.php matchimage
		val adjBandImage = stretchToMinMax(bandImage)
//		val adjBandImage = bandImage
		
		tiles
			.map { tile -> tile to extractTile(adjBandImage, tile) }
			.map { (tile, img) -> tile to listOf(img) }
			.forEach { (tile, imgs) -> writeTileGroup(imgName, "", bandDir, tile, imgs) }
		
	}
	
}

fun findAllTileLocs(firstBand: BufferedImage, tileAll: Boolean) = sequence {
	
	for (y in 0 until (firstBand.height - 2 * TILE_Y_STRIDE) step TILE_Y_STRIDE) {
		for (x in 0 until (firstBand.width - 2 * TILE_X_STRIDE) step TILE_X_STRIDE) {
			
			if (tileNotBlack(firstBand, x, y, TILE_WIDTH, TILE_HEIGHT)) {
				yield(Tile(x, y, TILE_WIDTH, TILE_HEIGHT))
			}
			
		}
	}
	
	return@sequence
	
}
