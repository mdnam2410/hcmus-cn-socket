# need image magick
cd ./512
mogrify -resize 16x16 -quality 100 -path ../16/ *.png
mogrify -resize 64x64 -quality 100 -path ../64/ *.png
mogrify -resize 32x32 -quality 100 -path ../32/ *.png

