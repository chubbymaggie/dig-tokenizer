#!/usr/bin/env python

try:
    from pyspark import SparkContext
except:
    print "### NO PYSPARK"
import sys
import argparse
from digTokenizer.tokenizer import Tokenizer
from digSparkUtil import FileUtil, as_dict, dict_minus, limit_rdd

def testTokenizer(sc, input_dir, output_dir, config,
                  limit=None, 
                  debug=0, 
                  input_file_format="sequence",
                  input_data_type="json",
                  output_file_format="sequence",
                  output_data_type="json",
                  **kwargs):

    print(limit)

    futil = FileUtil(sc)

    # LOAD DATA
    rdd_ingest = futil.load_file(input_dir, file_format=input_file_format, 
                                 data_type=input_data_type)
    rdd_ingest.setName('rdd_ingest_input')

    ## (optionally) LIMIT

    rdd_limited = limit_rdd(rdd_ingest, limit=limit or None)

    ## TOKENIZE
    tokOptions = {"file_format": input_file_format,
                  "data_type": input_data_type}
    tokenizer = Tokenizer(config, **tokOptions)
    rdd_tokenized = tokenizer.perform(rdd_ingest)

    # SAVE DATA
    outOptions = {}
    futil.save_file(rdd_tokenized, output_dir, file_format=output_file_format, 
                    data_type=output_data_type, 
                    **outOptions)

def main(argv=None):
    '''this is called if run from command line'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_dir', required=True)
    parser.add_argument('--input_file_format', default='sequence', choices=('text', 'sequence'))

    parser.add_argument('-o','--output_dir', required=True)
    parser.add_argument('--output_file_format', default='sequence', choices=('text', 'sequence'))

    parser.add_argument('--config', default=None)

    parser.add_argument('-l','--limit', required=False, default=None, type=int)

    args=parser.parse_args()
    # Default configuration to empty config
    # (avoid mutable container as default)
    args.config = args.config or {}

    sparkName = "testTokenizer"
    sc = SparkContext(appName=sparkName)

    # remove positional args, everything else passed verbatim
    kwargs = dict_minus(as_dict(args), "input_dir", "output_dir", "config")
    testTokenizer(sc, args.input_dir, args.output_dir, args.config, **kwargs)

# call main() if this is run as standalone
if __name__ == "__main__":
    sys.exit(main())
