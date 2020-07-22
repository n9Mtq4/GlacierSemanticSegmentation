package com.n9mtq4.gss.tilegen

import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO

/**
 * Created by will on 7/21/20 at 10:10 PM.
 *
 * @author Will "n9Mtq4" Bresnahan
 */

const val LANDSAT_IN_DIR_NAME = "../in/"
const val LANDSAT_OUT_DIR_NAME = "../netin/"

const val IMAGE_NAME = "LC08_L1TP_042005_20150814_20170226_01_T1"

fun main() {
	
	val inDir = File(LANDSAT_IN_DIR_NAME)
	val bandFiles = inDir.listFiles { _, name -> name.endsWith(".jpg") }
	
	val firstImage = ImageIO.read(bandFiles.first())
	
	val tiles = getUsingTileLocs(firstImage)
	
	for (bandFile in bandFiles) {
		
		val bandNum = getBandFromName(bandFile.name)
		
		if (bandNum in SKIP_BANDS) continue
		
		val bandImage = ImageIO.read(bandFile)
		
		if (bandImage.width != firstImage.width || bandImage.height != firstImage.height) {
			println("${bandFile.name} B$bandNum doesn't match width and height. Band width = ${bandImage.width}, Band height = ${bandImage.height}, firstImage width = ${firstImage.width}, firstImage height = ${firstImage.height}")
			continue
		}
		
		val bandDir = File(LANDSAT_OUT_DIR_NAME, "B$bandNum")
		bandDir.mkdirs()
		
		tiles
			.map { tile -> tile to extractTile(bandImage, tile) }
			.forEach { (tile, img) -> writeOutUsingTile(IMAGE_NAME, bandDir, tile, img) }
		
	}
	
}

fun writeOutUsingTile(imgName: String, bandDir: File, tile: Tile, img: BufferedImage) {
	
	val tileNamePrefix = "${imgName}_${tile.nameString}"
	ImageIO.write(img, "png", File(bandDir, "${tileNamePrefix}.png"))
	
}

fun getUsingTileLocs(img: BufferedImage) = sequence {
	
	for (y in 0 until (img.height - 2 * TILE_Y_STRIDE) step TILE_Y_STRIDE) {
		for (x in 0 until (img.width - 2 * TILE_X_STRIDE) step TILE_X_STRIDE) {
			
			yield(Tile(x, y, TILE_WIDTH, TILE_HEIGHT))
			
		}
	}
	
	return@sequence
	
}
