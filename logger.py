import logging

def start_logging(name):
    custome_logger = logging.getLogger(name)
    custome_logger.setLevel(logging.DEBUG)  

    # set printing to terminal
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter(fmt='[%(levelname)5s] - %(module)11s - %(threadName)-6s - %(funcName)15s() : %(message)s')
    stream_handler.setFormatter(stream_formatter)
    custome_logger.addHandler(stream_handler)
    
    # set printing to file "logger.log"
    file_handler = logging.FileHandler('logger.log', 'w+')
    file_formatter = logging.Formatter(fmt='(%(asctime)s) [%(levelname)5s] - %(module)19s - %(threadName)-10s - %(funcName)19s() : %(message)s')
    file_handler.setFormatter(file_formatter)
    custome_logger.addHandler(file_handler)
    
    return custome_logger
