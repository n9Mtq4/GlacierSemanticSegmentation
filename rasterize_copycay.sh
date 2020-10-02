#!/bin/bash
set -e #exit if you get any errors

echo "Make sure your vector and raster have the same projection"

vector=${1?Error: no vector name given}
raster=${2?Error: no raster name given}

#get names so that you can export the names in the formate vector_raster
vector_name="${1##*/}"
raster_name="${2##*/}"
vector_name="${vector_name%.*}"
raster_name="${raster_name%.*}"




function gdal_extent_gdalwarp_te() {
    if [ -z "$1" ]; then
        echo "Missing arguments. Trouble with raster extent"
        return
    fi
    EXTENT=$(gdalinfo "$1" |\
        grep "Lower Left\|Upper Right" |\
        sed "s/Lower Left  //g;s/Upper Right //g;s/).*//g" |\
        sed 's/ *$//g' |\
        tr -d "\n[(,]")
    echo -n "$EXTENT"
}

function gdal_pixelsize_gdalwarp_tr() {
    if [ -z "$1" ]; then
        echo "Missing arguments. Trouble with pixel size"
        return
    fi
    EXTENT=$(gdalinfo "$1" |\
        grep "Pixel Size" |\
        sed "s/Pixel Size =//g; s/,/ /g" |\
        tr "\n" " " |\
        tr -d "[(,])-")
    echo -n "$EXTENT"
}

ExtractedSRS=$(gdalsrsinfo -o proj4 $raster | tr -d "'")
ExtractedExtent=$(gdal_extent_gdalwarp_te $raster)
ExtractedResolution=$(gdal_pixelsize_gdalwarp_tr $raster)

#Figure out where Landsat scene has data so that only the glacier outlines that match with the landsat scene will be included
echo "create mask"
output_mask="${raster_name}_mask.TIF"
gdal_calc.py -A $raster --outfile $output_mask --calc="(A>0)*1+(A<1)*0"

#rasterize the vector to Landsat scene area
echo "rasterize glacier outlines"
output_name="${vector_name}_rasterized_${raster_name}.TIF"
gdal_rasterize -burn 1 -te $ExtractedExtent -tr $ExtractedResolution $vector $output_name

echo "mask glaciers by landsat scene"
glaciers_masked_to_landsat="${vector_name}_matched_${raster_name}.TIF"
gdal_calc.py -A $output_name -B $output_mask --outfile=$glaciers_masked_to_landsat --calc="A*B"

echo "convert to png"
output_png_name="${raster_name%_*}_truth"
convert -quality 100 $glaciers_masked_to_landsat $output_png_name.png
