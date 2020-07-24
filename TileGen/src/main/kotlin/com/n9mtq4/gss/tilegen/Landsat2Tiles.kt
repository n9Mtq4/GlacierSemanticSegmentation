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

const val IMAGE_NAME = "LC08_L1TP_044005_20160713_20170222_01_T1"

fun main() {
	
	landsat2Tiles(LANDSAT_IN_DIR_NAME, LANDSAT_OUT_DIR_NAME, IMAGE_NAME)
	
}

fun landsat2Tiles(landSatInDirName: String, landSatOutDirName: String, imageName: String) {
	
	val inDir = File(landSatInDirName)
	val bandFiles = inDir.listFiles { _, name -> name.endsWith(".jpg") }!!
	
	val firstImage = ImageIO.read(bandFiles.first())
	
	val tiles = getUsingTileLocs(firstImage)
	
	for (bandFile in bandFiles) {
		
		println("Tiling image ${bandFile.name}")
		
		val bandNum = getBandFromName(bandFile.name)
		
		if (bandNum !in INCLUDE_BANDS) continue
		
		val bandImage = ImageIO.read(bandFile)
		
		if (bandImage.width != firstImage.width || bandImage.height != firstImage.height) {
			println("${bandFile.name} B$bandNum doesn't match width and height. Band width = ${bandImage.width}, Band height = ${bandImage.height}, firstImage width = ${firstImage.width}, firstImage height = ${firstImage.height}")
			continue
		}
		
		val bandDir = File(landSatOutDirName, "B$bandNum")
		bandDir.mkdirs()
		
		tiles
			.map { tile -> tile to extractTile(bandImage, tile) }
			.forEach { (tile, img) -> writeOutUsingTile(imageName, bandDir, tile, img) }
		
	}
	
}

fun writeOutUsingTile(imgName: String, bandDir: File, tile: Tile, img: BufferedImage) {
	
	val tileNamePrefix = "${imgName}_${tile.nameString}"
	ImageIO.write(img, "png", File(bandDir, "${tileNamePrefix}.png"))
	
}

fun getUsingTileLocs(img: BufferedImage) = sequence {
	
	for (y in 0 until (img.height - TILE_HEIGHT) step TILE_Y_STRIDE) {
		for (x in 0 until (img.width - TILE_WIDTH) step TILE_X_STRIDE) {
			
			yield(Tile(x, y, TILE_WIDTH, TILE_HEIGHT))
			
		}
	}
	
	return@sequence
	
}
