# Image Analyser Project, "Mapp" by Derick Su

## Project Description
**Mapp** analyses the sizes of contiguous masses of colour (henceforth referred to as "countries") in the provided images. Using commands, the user can then gather data of the countries using commands. 
### Countries
A "country", as mentioned before, is a contiguous masses of pixels with a colour in the following list: 
<ul>
<li><b>Red</b>: in RGB value defined as: 255~125, 130~0, 130~0</li>
<li><b>Green</b>: in RGB value defined as: 130~0,  255~125, 130~0</li>
<li><b>Blue</b>: in RGB value defined as: 130~0, 130~0,  255~125</li>
<li><b>Orange</b>: in RGB value defined as: 255~125, 165~40, 130~0</li>
<li><b>Yellow</b>: in RGB value defined as: 255~125, 255~125, 130~0</li>
<li><b>Pink</b>: in RGB value defined as: 255~125, 130~0, 255~125</li>
<li><b>White</b>: in RGB value defined as: 255~125, 255~125, 255~125</li>
<li><b>Black</b>: in RGB value defined as: 130~0, 130~0, 130~0</li>
<li><b>Unidentified</b>: any value RGB value which do not fit the other colours</li>
</ul>
Different colours which fit into the same categories which are adjacent to each other but not being the exact same colour will still be counted as one country.

# Usage
First the user will enter the amount of images they wish to analyse. After, they must enter images which must be located in the same folder as the program and the file extension must be in the entered name.

# Commands
**Commands** are what the user types in the *Enter Command:* field. Commands are used to obtain the data which is collected by the program. There are two types of **Commands**: **Global Commands** which are commands used to anaylse countries from all images and compare them, and **Single Image Commands** which only analyse countries within one image.

## Global Commands
### HELP
Returns all possible commands.
### ALLIMG
Returns a list with all images which has been inputted into the program.
### TOP
Returns an ordered list, from largest to smallest, of the top 5 largest countries in the database.
### LARGE
Returns an ordered list, from largest to smallest, of the largest country of each image.
### ONEIMG
Returns list of all avaliable images and begins the single image command interface.

## Single Image Commands
To access Single Image Commands, the user must enter the ONEIMG command and then enter the filename of the desired image
### COUNTRY
Displays the a blacked out image with only the selected country coloured white.
### ALLCOUNTRY
Returns list of all avaliable countries.
### FIND
Returns the size of the country and rank of it compared to other countries in the same image.
### SHOW
Displays an image of all countries in random colours, mainly used for debugging.
### SHOWOG
Displays the original image.
### TOP
Returns the top 5 largest countries. If there are less, it displays all countries from largest to smallest.

# Test Cases
*note: UI elements are not included as "output"
## Input: 
```
dnfjksdl
```
### Output:
```
Not a valid Input!
```

## Input: 
```
3
EastAsiaHanDynasty.png
ww1.png
randomMap.png
tOP
```
### Output:
```
Number 1 largest country is country 398 from randomMap.png with 238912 pixels
Number 2 largest country is country 284 from randomMap.png with 210206 pixels
Number 3 largest country is country 399 from randomMap.png with 177353 pixels
Number 4 largest country is country 0 from EastAsiaHanDynasty.png with 93380 pixels
Number 5 largest country is country 2 from randomMap.png with 77457 pixels
```
## Input: 
```
3
EastAsiaHanDynasty.png
ww1.png
randomMap.png
LARGE
```
### Output:
```
Number 1 largest country is country 398 from randomMap.png with 238912 pixels
Number 2 largest country is country 0 from EastAsiaHanDynasty.png with 93380 pixels
Number 3 largest country is country 769 from ww1.png with 33008 pixels
```

## Input: 
```
3
EastAsiaHanDynasty.png
ww1.png
randomMap.png
oneimg
ww1.png
AllCOuntry
```
### Output:
```
List of avaliable images: ['EastAsiaHanDynasty.png', 'ww1.png', 'randomMap.png']
The avaliable countries (largest to smallest): [769, 278, 4, 338, 189, 91, 669, 3, 318, 272, 675, 195, 44, 590, 600, 596, 12, 597, 1, 538, 170, 183, 243, 737, 516, 665, 667, 281]
```

## Input: 
```
3
EastAsiaHanDynasty.png
ww1.png
randomMap.png
oneimg
ww1.png
top
```
### Output:
```
List of avaliable images: ['EastAsiaHanDynasty.png', 'ww1.png', 'randomMap.png']
The top 5 countries are: [769, 278, 4, 338, 189]
```

## Input: 
```
3
EastAsiaHanDynasty.png
ww1.png
randomMap.png
oneimg
ww1.png
country
769
```
### Output:
![Russia](README_ASSETS/group769(Russia).png)


# Development
Compared to **Taiga**, **Mapp**'s development was much slower, with a gradual implementation of processes, some not even expected from the start. The first big issue encountered during the development of **Mapp** was the issue of redundant countries. This would occur as the countries wouldn't know that other countries that touched it with the same colour should be consolidated into one larger country. This was particularly prominent in ledges facing right, which would cause this stripe like effect. To solve this issue, I originally tried to just implement the consolidation code while creating the countries, however, this was very buggy, often not working at all. Even when it did work, it would take nearly half an hour to process one image. Eventually, I made the consolidation process run in a seperate loop, which would make it easier to debug and optimize. The biggest problem that **Mapp** faced during its development was its terrible optimization. One of the ways which made it faster was reducing the print statements showing it's progress. I decided to limit it to 1 print every 100000 pixels as it would print around every 5 to 10 percent on a resonably sized image. I also imported all of the pixels of the image into a list, which somewhat increased the speed, though the effectiveness of this optimization is debatable.

# Real World Use
**Mapp** is more so a component program that can be used in combination with other programs to serve a more practical real life purpose. **Mapp** doesn't currently have a command to return the colour of the clump, but it does store the colour of the country which is used in the consolidation process. **Mapp** can be used as components in programs to detect outliers of colour, or the sizes of clouds in meteorology, or the number of objects in an image.