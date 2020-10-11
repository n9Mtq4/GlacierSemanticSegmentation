import numpy as np
import gdal, osr
from pathlib import Path


def write_gtiff(array, gdal_obj, outputpath, dtype=gdal.GDT_UInt16, options=0, color_table=0, nbands=1, nodata=False):
    """
    Writes a geotiff.

    array: numpy array to write as geotiff
    gdal_obj: object created by gdal.Open() using a tiff that has the SAME CRS, geotransform, and size as the array you're writing
    outputpath: path including filename.tiff
    dtype (OPTIONAL): datatype to save as
    nodata (default: FALSE): set to any value you want to use for nodata; if FALSE, nodata is not set
    """

    gt = gdal_obj.GetGeoTransform()

    width = np.shape(array)[1]
    height = np.shape(array)[0]

    # Prepare destination file
    driver = gdal.GetDriverByName("GTiff")
    if options != 0:
        dest = driver.Create(outputpath, width, height, nbands, dtype, options)
    else:
        dest = driver.Create(outputpath, width, height, nbands, dtype)

    # Write output raster
    if color_table != 0:
        dest.GetRasterBand(1).SetColorTable(color_table)

    dest.GetRasterBand(1).WriteArray(array)

    if nodata is not False:
        dest.GetRasterBand(1).SetNoDataValue(nodata)

    # Set transform and projection
    dest.SetGeoTransform(gt)
    wkt = gdal_obj.GetProjection()
    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt)
    dest.SetProjection(srs.ExportToWkt())

    # Close output raster dataset 
    dest = None


def proc_thresholdimg(nnt_path, outt_path, ref):
    nnt = gdal.Open(nnt_path)
    nnt_data = nnt.GetRasterBand(1).ReadAsArray()
    write_gtiff(nnt_data, ref, outt_path, options=['COMPRESS=DEFLATE', 'PREDICTOR=2', 'ZLEVEL=9'], nodata=0)


if __name__ == '__main__':
    
    # name = "LC08_L1TP_044005_20160713_20170222_01_T1"
    name = list(Path("./in/").glob("*.TIF"))[0].stem[:-3]  # remove band info from name
    
    nn_path = f"./out/{name}_NN.png"
    ref_path = f"./in/{name}_B1.TIF"
    
    out_path = f"./out/{name}_NN.TIF"
    
    nn = gdal.Open(nn_path)
    ref = gdal.Open(ref_path)
    
    nn_data = nn.GetRasterBand(1).ReadAsArray()
    
    write_gtiff(nn_data, ref, out_path, options=['COMPRESS=DEFLATE', 'PREDICTOR=2', 'ZLEVEL=9'])
    
    for t in [2, 5, 7]:
        nnt_path = f"./out/{name}_NNT{t}.png"
        outt_path = f"./out/{name}_NNT{t}.TIF"
        proc_thresholdimg(nnt_path, outt_path, ref)
