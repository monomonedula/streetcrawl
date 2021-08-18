[![Build Status](https://app.travis-ci.com/monomonedula/streetcrawl.svg?branch=master)](https://app.travis-ci.com/monomonedula/streetcrawl)
[![codecov](https://codecov.io/gh/monomonedula/streetcrawl/branch/master/graph/badge.svg?token=8rmLvt9atm)](https://codecov.io/gh/monomonedula/streetcrawl)
[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)

# Streetcrawl 
### Google Streetview pictures collector

Streetcrawl is a tool collecting panoram photos from [Google Streetview Static API](https://developers.google.com/maps/documentation/streetview/overview).


## Installation
```shell
pip install streetcrawl
```

## Usage

Before running this tool set the environment variable `STREETVIEW_API_KEY` with your Google Streetview API key.

Example invokation:
```shell
python streetcrawl 50.46744390530811,30.48305902638788 catalog/
```
or 

```shell
python streetcrawl 50.46744390530811,30.48305902638788 catalog/ --fov 120 --square-side 2000 --step 15
```


The first param is the latitude and longitude (no space between them) of the point you 
want to be the centre of the area to explore.

Next parameter is the folder to store the panoramas to.

The crawler makes an imaginary square grid with the centre at the point we specified earlier.
For every node of the grid it makes an API call asking google where's the closest panorama.
It then collects the panorama pictures to the destination folder putting every panorama pics to a subfolder named by the panorama's ID.
It also creates `index.csv` file in the destination folder where it stores the info about everry panorama's coordinates.

Optional params:
* `--fov` -- field of view. A panorama is 360 degrees, so if the field of view is 120 the panorama will be stored as 3 pics with 120 degree fov each.
Google allows for max field of view to be equal 120. Note also that `360 % fov` must be `0`
* `--square-side` -- the side of the square region to be crawled in meters. Defaults to 1500.
* `--step` -- the grid step. The larger the step the less dense the grid is, the bigger chance that you will miss some panoramas in the explored region.
 However, specifing step less than 10 meters usually doesn't make sense since the panoramas themselves are not so dense.
* `--resolution` -- resolution of the images to be collected. Example value: `400x800` which means 400 pixels width and 800 pixels height. Defaults to `600x600`.
* `--glue` -- a flag which, if set, glues together parts of fetched panoramas, so every panorama is stored as a single image.

### To be done
Exponential backoff and throttling if starting to get `403` responses.