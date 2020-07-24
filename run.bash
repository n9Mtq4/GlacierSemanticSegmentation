
echo Setting up and deleting old data
mkdir -p netin
mkdir -p netout
mkdir -p out

rm -r ./netin/B*
rm ./netout/*.png

echo Converting TIF to JPEG
pushd ./in/ || return 1
for f in *.TIF ; do
    convert -quality 100 "$f" "$f.jpg"
done
popd || return 1

echo Tiling images
java -jar TileGen-1.0-SNAPSHOT-all.jar l2t

echo Running network
python3 usenetwork.py

echo Stitching tiles
java -jar TileGen-1.0-SNAPSHOT-all.jar stitch

echo Converting network output to TIF
python3 png2geotiff.py
