dig-tokenizer
==================

Tokenizing documents based on configuration/rules


Requirements:
-------------
* Spark: Visit http://spark.apache.org/downloads.html, select the package type of “Pre-built for Hadoop 2.4 and later,” and then click on the link for “Download Spark” This will download a compressed TAR file, or tarball. Uncompress the file into ```<spark-folder>```.

* Run `./make-spark.sh` every time to build the zip files required by spark every time you pull in new code


Running Tokenizer:
------------------
```
tokenizer.py [options] inputFile configFile outputDir
```

Example Invocation:
```
cd <spark-folder>
./bin/spark-submit \
    --master local[*] \
    --executor-memory=4g \
    --driver-memory=4g \
    --py-files ~/github/dig-tokenizer/digTokenizer/tokenizer.zip \
    ~/github/dig-tokenizer/digTokenizer/tokenizer.py \
    ~/github/datasets/sample-ad-location/sample.tsv \
    ~/github/dig-tokenizer/sample_config.json \
    ~/github/datasets/sample-ad-location/tokens

```

To tokenize a sequence file containing json data, the config file must contain "path" to each field that should be
extracted.
```
./bin/spark-submit \
    --master local[*] \
    --executor-memory=4g \
    --driver-memory=4g \
    --py-files ~/github/dig-tokenizer/digTokenizer/tokenizer.zip \
    ~/github/dig-tokenizer/digTokenizer/tokenizer.py \
    --type json --inputformat sequence \
    ~/github/datasets/body_text/sample-ad.seq \
    ~/github/dig-tokenizer/sample_json_config.json \
    ~/github/datasets/body_text/seq_tokens
```
