#!/usr/bin/bash
# ---------------------------------------------------------------------------
# import_to_mongo - A Script to Import the Yelp Dataset into the MongoDB

# Copyright 2016,  Naveen Jetty

# Usage: import_to_mongo [-h|--help] [-d|--dir]

# Revision history:
# 2016-12-01 Created Intial Script
# ---------------------------------------------------------------------------

PROGNAME=${0##*/}
VERSION="0.1"

clean_up() { # Perform pre-exit housekeeping
  return
}

error_exit() {
  echo -e "${PROGNAME}: ${1:-"Unknown Error"}" >&2
  clean_up
  exit 1
}

graceful_exit() {
  clean_up
  exit
}

signal_exit() { # Handle trapped signals
  case $1 in
    INT)
      error_exit "Program interrupted by user" ;;
    TERM)
      echo -e "\n$PROGNAME: Program terminated" >&2
      graceful_exit ;;
    *)
      error_exit "$PROGNAME: Terminating on unknown signal" ;;
  esac
}

usage() {
  echo -e "Usage: $PROGNAME [-h|--help] [-d|--dir]"
}

help_message() {
  cat <<- _EOF_
  $PROGNAME ver. $VERSION
  A Script to Import the Yelp Dataset into the MongoDB

  $(usage)

  Options:
  -h, --help  Display this help message and exit.
  -d, --dir  Directory of Yelp Dataset files

_EOF_
  return
}

# Trap signals
trap "signal_exit TERM" TERM HUP
trap "signal_exit INT"  INT



# Parse command-line
while [[ -n $1 ]]; do
  case $1 in
    -h | --help)
      help_message; graceful_exit ;;
    -d | --dir)
      export YELP_PATH=$2;;
      
    -* | --*)
      usage
      error_exit "Unknown option $1" ;;

  esac
  shift
done

# Main logic
mongo --eval "db.stats()" >/dev/null 2>&1  # do a simple harmless command of some sort

if [ $? -ne 0 ]; then
    error_exit "MongoDB Server is not running"
fi

cwd=$(pwd)

if [[ -z "$YELP_PATH" ]]; then
    error_exit "Path is not specified or an Empty String is specified"
fi

if [[ -d $YELP_PATH ]]; then
    echo "Validating the directory" $YELP_PATH "Completed" 
else
    error_exit $YELP_PATH" : not a directory"
fi

echo "Starting the import process of Yelp Dataset"

if [[ -f "$YELP_PATH/yelp_academic_dataset_business.json" ]]; then
    echo " "
    echo "Importing Business Collection"
    mongoimport --db yelp --collection business --file "$YELP_PATH/yelp_academic_dataset_business.json"
else
    echo "File yelp_academic_dataset_business.json not found at $YELP_PATH, skipping the import for Business"
fi

if [[ -f "$YELP_PATH/yelp_academic_dataset_tip.json" ]]; then
    echo " "
    echo "Importing Tip Collection"
    mongoimport --db yelp --collection tip --file "$YELP_PATH/yelp_academic_dataset_tip.json"
else
    echo "File yelp_academic_dataset_tip.json not found at $YELP_PATH, skipping the import for Tip"
fi

if [[ -f "$YELP_PATH/yelp_academic_dataset_review.json" ]]; then
    echo " "
    echo "Importing Review Collection"
    mongoimport --db yelp --collection reviews --file "$YELP_PATH/yelp_academic_dataset_review.json"
else
    echo "File yelp_academic_dataset_review.json not found at $YELP_PATH, skipping the import for Review"
fi

if [[ -f "$YELP_PATH/yelp_academic_dataset_checkin.json" ]]; then
    echo " "
    echo "Importing Checkin Collection"
    mongoimport --db yelp --collection checkin --file "$YELP_PATH/yelp_academic_dataset_checkin.json"
else
    echo "File yelp_academic_dataset_checkin.json not found at $YELP_PATH, skipping the import for Checkin"
fi

if [[ -f "$YELP_PATH/yelp_academic_dataset_user.json" ]]; then
    echo " "
    echo "Importing User Collection"
    mongoimport --db yelp --collection user --file "$YELP_PATH/yelp_academic_dataset_user.json"
else
    echo "File yelp_academic_dataset_user.json not found at $YELP_PATH, skipping the import for User"
fi

echo ""
echo "Importing of Yelp Dataset completed"

echo ""
echo "Indexing the collections 'Review' and 'Tip' with business_id"
mongo < EnsureIndex.js
echo ""
echo "Indexing Completed"


graceful_exit