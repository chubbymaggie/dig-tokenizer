dig-tokenizer is a python library which will produce tokens with different options on multiple fields. 

dig-tokenizer will help you:
* Generate tokens of your choice using a simple config file.
* Perform clustering based on the tokens generated using the library [dig-lsh-clustering](https://github.com/usc-isi-i2/dig-lsh-clustering/tree/devel)


#### Tools built with dig-tokenizer:
[dig-lsh-clustering](https://github.com/usc-isi-i2/dig-lsh-clustering):
This is an implementation of Locality Sensitive Hashing(LSH) Algorithm in python. You can cluster the similar documents using this library.


#### Requirements
* Spark: Visit http://spark.apache.org/downloads.html, select the package type of “Pre-built for Hadoop 2.4 and later,” and then click on the link for “Download Spark” This will download a compressed TAR file, or tarball. Uncompress the file into ```<spark-folder>```.
* Run `./make-spark.sh` every time to build the zip files required by spark every time you pull in new code

#### How to install
pip install digTokenizer

#### Usage
*You can run the following command cloning this repo with the config file and input files like following:

```
python digTokenizer/test/testTokenizer.py -i input \
      --input_file_format text -o output \
      --config digTokenizer/test/tests/text-json/config/config.json \
      --output_file_format text
```
If you want to import this library into your code please check [here](https://github.com/usc-isi-i2/dig-tokenizer/blob/devel/digTokenizer/test/testTokenizer.py) for the usage. 


#### Examples
To run this code, you have to input a config file which specifies how tokens should look like. Let's look at an example.

#####Sample config file:
```
{
  "fieldConfig": {
    "0": {
      "path": ".description",
      "allow_blank":false
    }
  },
  "defaultConfig": {
    "analyzer": {
      "tokenizers": [
        "whitespace"
      ]
    }
  },
  "settings": {
      }
}
```

Sample Input : 
```
http://dig.isi.edu/ht/data/1000330/webpage  { "pageurl": "https://www.naughtyreviews.com/1234",
"title": "This is the title", 
"description": ["Hi, How is your day ? Here is the description"]}
```
Input should be in the format ```<unique-id><tab space><json line>```

In "fieldConfig" of config file , you mention the json field path in the jq format. If you don't know about jq check here https://stedolan.github.io/jq/manual/. If you want tokens for more than one field, you can add more fields with numbers "1", "2" etc. "prefix" will enable to add a prefix to every token generated from that particular field. 

Sample Output :
```
http://dig.isi.edu/ht/data/1000330/webpage	[["Hi,", "How", "is", "your", "day", "?", "Here", "is", "the", "description"]]
```
Output tokens are generated by whitespace split. 

Other options for tokenizer are :

(a) word-ngram : Here with the given size n words are combined and emmitted as a token. In the above example if n=2 output 
will be
```
http://dig.isi.edu/ht/data/1000330/webpage	[["Hi,How", "Howis", "isyour", "yourday", "day?", "?Here", "Hereis", "isthe", "thedescription"]]
```

(b) character-ngram : In this case with the given size n, n characters are taken and emitted as a token. In the above example if n = 4

output will be 
```
http://dig.isi.edu/ht/data/1000330/webpage	[["$$$H", "$$Hi", "$Hi,", "Hi, ", "i, H", ", Ho", " How", "How ", "ow i", "w is", " is ", "is y", "s yo", " you", "your", "our ", "ur d", "r da", " day", "day ", "ay ?", "y ? ", " ? H", "? He", " Her", "Here", "ere ", "re i", "e is", " is ", "is t", "s th", " the", "the ", "he d", "e de", " des", "desc", "escr", "scri", "crip", "ript", "ipti", "ptio", "tion", "ion$", "on$$", "n$$$"]]
````

And config file looks like as follows :
```
{
  "fieldConfig": {
    "0": {
      "path": ".description",
      "allow_blank":false
    }
  },
  "defaultConfig": {
    "analyzer": {
      "tokenizers": [
        "char_n_4"
      ]
    }
  },
  "settings": {
 "char_n_4": {
      "type": "character_ngram",
      "size": 4
    }
      }
}
```
### Some More Options:
#### Filter :
* lowercase -> this will produce lowercased tokens
* uppercase -> this will produce uppercased tokens
* latin -> this will convert all non-english characters to the nearest english character if possible. For example à to a, ñ to n
* mostlyHTML -> if that field has more than 40 html tags like <title>,</title>, <a>,</a> etc, then there will be no tokens will be emmitted.


#### Regex expressions :
* If you want to apply some regex expressions on the fields you can add them in the config file. Two kinds of options are available. 
 * Word level regexes : You can check the example of those expressions click here [word regex](https://github.com/usc-isi-i2/dig-tokenizer/blob/master/unicode-tokenizer.json#L12)
Format is as follows :
```
            {
              "regex": "<regex expression here>",
              "replacement": "<if you replace the matching characters",
              "desc": "<description>"
            }
```
 * Sentence level regexes : You can check the example of those expressions click here [sent regex config](https://github.com/usc-isi-i2/dig-tokenizer/blob/master/unicode-tokenizer.json#L40)
Format is same.

The reason for allowing two types is the regex expression you want to match may not be a complete in a word, but it's a complete match over the complete sentence (if the field has more than one word)

#### Stop words :
If you don't want to emit tokens for some words you can add them in stop words list present in config file click here [stop words config](https://github.com/usc-isi-i2/dig-tokenizer/blob/master/unicode-tokenizer.json#L141)
```
"stop_default": {
                  "type": "stop",
                  "words": ["a","an","and","are","as"]
               }
```

#### Default Config:
If you hate writing seperate type of configuration for every field you can write a default config click here [default config example](https://github.com/usc-isi-i2/dig-tokenizer/blob/master/unicode-tokenizer.json#L99)
```
"defaultConfig": {
    "analyzer": {
      "replacements": [
        {
          "regex": "[^\\w\\s]",
          "replacement": "",
          "description": "replace special chars"
        }
      ],
      "filters": [
        "lowercase",
        "latin"
      ],
      "tokenizers": [
        "character_n_5"
      ]
    }
  }
```
At the end you can see complete config file with all the options [config file with all the options](https://github.com/usc-isi-i2/dig-tokenizer/blob/master/unicode-tokenizer.json)



