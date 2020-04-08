import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

import sys

def gc_logger(name, level=logging.INFO, stream=False):
    client = google.cloud.logging.Client(project=project)    
    handler = CloudLoggingHandler(client, name=name)

    logger = logging.getLogger(name)
    
    if not len(logger.handlers):
        logger.setLevel(level)
        logger.addHandler(handler)
        if stream == True:
            out_hdlr = logging.StreamHandler(sys.stdout)
            logger.addHandler(out_hdlr)

    return logger