package com.n9mtq4.gss.tilegen

import java.io.File

/**
 * Created by will on 9/10/20 at 9:04 PM.
 *
 * @author Will "n9Mtq4" Bresnahan
 */
fun main() {
	
	val inputDir = File("../data/ls8_pretrain")
	val outputDir = File("../data/tiles/ls8_pretrain1")
	
	
	val bandDirs = arrayOf(1, 2, 3, 4, 5, 6, 7)
		.map { File(outputDir, "B$it") }
	bandDirs.forEach { it.mkdirs() }
	
	
	val imgDirs = inputDir.listFiles()!!
	
	imgDirs.forEach { ndsiProcImgDir(it, outputDir) }
	
}

fun ndsiProcImgDir(imgDir: File, outputDir: File) {
	
	val imgFiles = imgDir.listFiles()!!.toList()
	
	val mbImg = SatImg(imgFiles)
	
	val tiles = findAllTileLocs(mbImg.firstBand(), true)
			.toList()
	
	mbImg.bands.forEach { band, img -> 
		tiles.map { tile -> tile to extractTile(img, tile) }
			.map { (tile, img) -> tile to listOf(img) }
			.forEach { (tile, imgs) -> writeTileGroup(imgDir.name, "", File(outputDir, "B$band"), tile, imgs) }
	}
	
	val ndsi = mbImg.ndsi()
	
	val truthDir = File(outputDir, "truth")
	truthDir.mkdirs()
	tiles
		.map { tile -> tile to extractTile(ndsi, tile) }
		.map { (tile, img) -> tile to listOf(img) }
		.forEach { (tile, imgs) -> writeTileGroup(imgDir.name, "", truthDir, tile, imgs) }
	
}
