# GPX Favorites merge

This tool merges multiple GPX files with favourites data with dedupliucation using an intermediate CSV file allowing modification.

I use this tool to synchronize the `favourites.gpx` files of multiple [OSMAnd](https://osmand.net/) installations.
The tools is *only* tested with files from OSMAnd.

## Usage

To merge multiple files into one:
```
./merge.py gpx2csv in1.gpx in2.gpx data.csv categories.json
```

This results in two files:
* `data.csv`: You can now edit this file with your favorite editor (text/spreadsheet programs) to spot and remove any similar but not exact duplicate entries. The file is sorted by the average of latitude and longitude.
* `categories.json`: Contains the mapping of categories (also: types) and colors.

Then you can generate the GPX file:
```
./merge.py csv2gpx data.csv categories.json output.gpx
```
