# Image Analyser Project, "Mapp" by Derick Su

## Project Description
**Mapp** analyses the sizes of contigouous "countries" of colour (henceforth referred to as "countries") in the provided images. Using commands, the user can then gather data of the countries using commands.

# Usage

# Commands
**Commands** are what the user types in the *Enter Command:* field. Commands are used to obtain the data which is collected by the program. There are two types of **Commands**, **Global Commands** which are commands used to anaylse countries from all images and compare them, and **Single Image Commands** which only analyse countries within one image.

## Global Commands
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

# Test Cases

# Development