package com.n9mtq4.gss.tilegen

import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO

/**
 * Created by will on 7/21/20 at 11:10 PM.
 *
 * @author Will "n9Mtq4" Bresnahan
 */

val TILE_FNAME_REGEX = """.+TILE(?<x>\d+)_(?<y>\d+)_(?<width>\d+)_(?<height>\d+).+""".toRegex()

const val PRED_IN_DIR = "../netout/"
const val PRED_OUT_DIR = "../out/"

const val X_MARGIN = (TILE_WIDTH - TILE_X_STRIDE) / 2
const val Y_MARGIN = (TILE_HEIGHT - TILE_Y_STRIDE) / 2

fun main() {
	
	stitch(LANDSAT_IN_DIR_NAME, PRED_IN_DIR, PRED_OUT_DIR, IMAGE_NAME)
	
}

fun stitch(landSatInDirName: String, predInDir: String, predOutDir: String, imageName: String) {
	
	val srcImgFile = File(landSatInDirName, "${imageName}_B1.TIF.jpg")
	val srcImg = ImageIO.read(srcImgFile)
	
	val srcWidth = srcImg.width
	val srcHeight = srcImg.height
	
	val predImage = BufferedImage(srcWidth, srcHeight, BufferedImage.TYPE_BYTE_GRAY)
	
	val tileFiles = File(predInDir).listFiles { _, name -> name.endsWith(".png") }!!
	
	tileFiles
		.asSequence()
		.map { ImageIO.read(it) to getTileFromName(it.name) }
		.forEach { (img, tile) -> writeTileCenter(predImage, img, tile) }
	
	val outFile = File(predOutDir, "${imageName}_NN.png")
	ImageIO.write(predImage, "png", outFile)
	
	thresholdImg(predImage)
	
	val outFileThresh = File(predOutDir, "${imageName}_NNT.png")
	ImageIO.write(predImage, "png", outFileThresh)
	
}

fun thresholdImg(predImage: BufferedImage) {
	
	val black = -16777216
	val white = -1
	
	for (y in 0 until predImage.height) {
		for (x in 0 until predImage.width) {
			
			val color = predImage.getRGB(x, y)
			val newColor = if (color == black) white else black
			predImage.setRGB(x, y, newColor)
			
		}
	}
	
}

fun writeTileCenter(fullImg: BufferedImage, tileImg: BufferedImage, tile: Tile) {
	
	for (ty in Y_MARGIN until tile.height - Y_MARGIN) {
		for (tx in X_MARGIN until tile.width - X_MARGIN) {
			
			val fy = tile.y1 + ty
			val fx = tile.x1 + tx
			
			val color = tileImg.getRGB(tx, ty)
			fullImg.setRGB(fx, fy, color)
			
		}
	}
	
}

fun getTileFromName(name: String): Tile {
	
	val regexGroups = TILE_FNAME_REGEX.find(name)!!.groups
	val x = regexGroups["x"]!!.value.toInt()
	val y = regexGroups["y"]!!.value.toInt()
	val width = regexGroups["width"]!!.value.toInt()
	val height = regexGroups["height"]!!.value.toInt()
	
	return Tile(x, y, width, height)
	
}
