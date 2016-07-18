# geo-datagen

This utility generates randomized JSON documents for use with MongoDB.

Each document contains the following fields and values:

    {
       "cuisine" : ["<string>","<string>",...],
       "grades" : [
          { 
             "date" : { "$date" : "YYYY-MM-DDTHH:MM:SS.sss-02:00"},
             "score" : "A|B|C|F"
          },
          ...
       ],
       "contact" : {
          "owner" : <string>,
          "phone" : "###-###-####",
          "email" : "<string>@example.net|com|org",
       },
      "location" : [ longitude, latitude ],
      "restaurant_name" : "<string>"
          
       
    }

`geo-datagen` outputs the result into the `restaurants.json` file for
use with `mongoimport`.

# Usage

    python geo-datagen.py -h -l <int> -d -u

* `-h` : Provides help
* `-l` | `--limit` : Creates `n` number of documents
* `-d` | `--delete` : Deletes `restaurants.json`
* `-u` | `--unique` : Generates unique phone numbers and emails. Deletes `restaurants.json`.
        Supports up to 88,000 unique documents.

# Notes

## Creating Unique Values

Running with `-u | --unique` generates unique values for 
phone numbers and emails. This may require additional memory and time,
especially with large values of `-l | --limit`. 

Note that `contact.phone` has a limited number of unique values
based on the possible combinations of 3-digit area code and 
`01XX` combinations.  Currently the limit is 88,000 documents.

## Date

The `grades.date` document contains the `$date` field. The 
`mongoimport` utility reads this in as an `ISODate()` object. 

## Contact

Contact information is completely randomized. 

Phone numbers are based on the `555` system employed by the 
North American Numbering Plan. 

Email domains use the IANA reserved domains `example.com`, `example.org`, 
and `example.net`. 

## Location

Location coordinates are in `longitude, latitude` format as required by GeoJSON. The coordinates are randomly generated between `-40,-35` longitude and `30,35` 
latitude.

# Disclaimer

This product is meant for educational or development purposes only. Any resemblance to real or fictional persons, living or dead is purely coincidental. No other warranty expressed or implied. May be too intense for some viewers. If condition persists, consult your physician. No user-serviceable parts inside. Freshest if eaten before date on carton. Subject to change without notice. Contains a substantial amount of non-tobacco ingredients. Slippery when wet. Not responsible for direct, indirect, incidental or consequential damages resulting from any defect, error or failure to perform. Not the Beatles. Penalty for private use. See label for sequence. Use only in a well-ventilated area. Keep away from fire or flames. Replace with same type. Do not fold, spindle or mutilate. No transfers issued until the bus comes to a complete stop. Although robust enough for general use, adventures into the esoteric periphery may reveal unexpected quirks. Vitamins A, D, E, and K may have been added. Not designed or intended for use in on-line control of aircraft, air traffic, aircraft navigation or aircraft communications; or in the design, construction, operation or maintenance of any nuclear facility. May contain traces of various nuts and seeds.

This supersedes all previous notices.
