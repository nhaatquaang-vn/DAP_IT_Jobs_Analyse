#!/bin/bash
# This script calculates simple interest given principal,
# annual rate of interest and time period in years.
#
# Formula: Simple Interest = (Principal * Rate * Time) / 100

echo "Enter the principal:"
read principal

echo "Enter the rate of interest per year (in %):"
read rate

echo "Enter the time period in years:"
read time

# Calculate simple interest
interest=$(echo "scale=2; $principal * $rate * $time / 100" | bc)

# Fallback for basic integer math if 'bc' is not installed
if [ -z "$interest" ]; then
    interest=$(( (principal * rate * time) / 100 ))
fi

echo "The simple interest is: $interest"
