# Google timeline visit calculator
Allows you to get a general overview about how much time you spent in a country, city and visiting around :)

## Features

- Parse "Location History.json" Google Maps timeline
- Filter base on location source or timeframe
- Filter visits base on distance radius
- Keep track of all the visits made to different countries
- Summary of all visits, total time in each country (stdout and json file)

## Why?

I'm aware there are some tools already out there to do similar things
but I couldn't fine any that would calculate the time I spent in each country.

I wanted to do something with the data Google collects from me and use it
for my own benefit. I need, for an immigration paperwork to provide proof of all time spent
I spent outside the country. I created this tool to help me with that task but
it can be use for multiple other applications

## How does it work?
### Get your data together
You go to [Google](https://takeout.google.com/settings/takeout) and ask for the export.
You'll get a huge (or not) json file with all your location history

![Google Takeout file example](https://github.com/guanana/google-timeline-visit-calculator/blob/main/img/Google_Timeline_Export.png?raw=true)

### Parse your data 
Once you get the file you need to parse it for it to be processed.
Run `python parse_json.py --help` to get all the possible options, ie:
```shell
usage: parse_json.py [-h] [-i INPUT] [-o OUTPUT] [-s START_DATE] [-e END_DATE] [--start_time START_TIME] [--end_time END_TIME] [-a ACCURACY] [-x {GPS,CELL,WIFI}]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input File (Location History.json)
  -o OUTPUT, --output OUTPUT
                        Output File
  -s START_DATE, --start_date START_DATE
                        The Start Date - format YYYY-MM-DD (defaults to 0h00m)
  -e END_DATE, --end_date END_DATE
                        The End Date - format YYYY-MM-DD (defaults to 23h59m59s)
  --start_time START_TIME
                        The Start Time - format HH:MM, only used if Start Date is set
  --end_time END_TIME   The End Time - format HH:MM, only used if End Date is set
  -a ACCURACY, --accuracy ACCURACY
                        Maximum accuracy (in meters), lower is better.
  -x {GPS,CELL,WIFI}, --source {GPS,CELL,WIFI}
                        If you only care about data collected with specific source, like GPS, CELL, WIFI

```
### Process your data
Once you have your output file you just need to run the main.py file with the parameters required,
again please run `python main.py --help` to see all possible options
```shell
usage: main.py [-h] [-i INPUT] [--no_show_visits] [--disable_output] [-o OUTPUT_FILE] [-r RADIUS] [-t MIN_TIME_CONSIDER]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input parsed file
  --no_show_visits      If you want to disable visits details
  --disable_output      Output to file is by default, if you set this you'll disable it
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output file name
  -r RADIUS, --radius RADIUS
                        Min movement in KM to consider it a visit
  -t MIN_TIME_CONSIDER, --min_time_consider MIN_TIME_CONSIDER
                        Min time to record a visit, time will be regardless added to country

```
### Get your result
If you've done all correctly you should get an output on the screen and a output json file
If you want to analize the data in a more readable way or work with it any Json Parser will do the job


![Output](https://github.com/guanana/google-timeline-visit-calculator/blob/main/img/Json_output.png?raw=true)

