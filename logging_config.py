import logging

def debug_mode(debug):
    
    #logging configuration
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

    if len(debug) > 1 and debug[1] == '--debug':
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('Debug mode enabled')

