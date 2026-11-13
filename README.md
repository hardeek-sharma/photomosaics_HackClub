# photomosaics_HackClub
A terminal program that makes an image out of other images

The program starts with the square program which asks the user for a directory full of images. It makes those  
images into squares and outputs them into either ./square_images/ or a user chosen directory. Then each images   
average color is gotten and put into colors.json as cache for the main program.

In the main program, it asks the user for an initial image to be made up of smaller images later on. It then   
asks for the quality of the mosaic, how many pixels in the initial image an image tile with take up in the new  
mosaic. After it asks for the tile size, how big each small image in the mosaic will be. Finally, it will make   
the mosaic out of the little images and, depending on the quality the user chose, it will look like the initial image.   

## EXAMPLE
Initial Image  
<img src="https://imgur.com/sd5Ns1H.jpg" width="800">  
  
Photomosaic Image (25 square size, 100 tile size)
#### Image might look lower quality than it is because of github resizing  
<img src="https://imgur.com/wPYdThG.jpg" width="800" alt=""> 

## How to Run
#### (This has only been tested on a Mac so instructions are only for Mac)
1. Download the most recent executables from the [releases page](https://github.com/hardeek-sharma/photomosaics_HackClub/releases) (Main and Square)
2. Open up Terminal.app and cd to where the file is downloaded
3. type "chmod +x " and drag the executable over to the terminal line so it autofills in its path (Do this for main and square)
4. The terminal thing might look like this: chmod +x /Users/name/Downloads/main (and square)
5. Type ./square to load in the tile image cache (Depending on the amount of images and their quality, this will take a while)
6. Type ./main to make photomosaics (Depending on the quality, this will take a while)
7. repeat from 5 if you want to use different images