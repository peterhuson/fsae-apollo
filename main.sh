# Run steering wheel

# args: numLEDs, optional use debug data?
# pipe logs to log file
python3 main.py 13 --debug-data > "logs/$(date +"%FT%H%M").log"
