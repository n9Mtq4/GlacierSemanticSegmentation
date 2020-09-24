package com.n9mtq4.gss.iface

import com.n9mtq4.gss.tilegen.*
import java.io.File
import java.lang.RuntimeException

/**
 * Created by will on 7/24/20 at 1:37 AM.
 *
 * @author Will "n9Mtq4" Bresnahan
 */

/**
 * really simple and bad interface for scripts
 * */
fun main(args: Array<String>) {
	
	if (args.size != 1) {
		println("Expected 1 argument. Pick generate, l2t, or stitch")
		return
	}
	
	when (args[0]) {
		
		"generate" -> tileGenGeneration()
		"l2t" -> ifaceLandsat2Tiles()
		"stitch" -> ifaceStitch()
		else -> println("Unknown option. Pick l2t or stitch")
		
	}
	
}

fun getImageNameFromFileName(fileName: String): String {
	
	val nameRegex = """(?<name>.*)_B\d\.(TIF|jpg)""".toRegex()
	val regexGroups = nameRegex.find(fileName)!!.groups
	return regexGroups["name"]?.value ?: throw RuntimeException("$fileName doesn't match a landsat file name")
	
}

fun getImageNameFromInDir(): String {
	
	val inputFileName = File("./in/")
		.listFiles { _, name -> name.endsWith(".TIF") || name.endsWith(".jpg") }!!
		.first().name
	
	return getImageNameFromFileName(inputFileName)
	
}

fun ifaceLandsat2Tiles() {
	
	val imageName = getImageNameFromInDir()
	landsat2Tiles("./in/", "./netin/", imageName)
	
}

fun ifaceStitch() {
	
	val imageName = getImageNameFromInDir()
	stitch("./in/", "./netout/", "./out/", imageName)
	
}
