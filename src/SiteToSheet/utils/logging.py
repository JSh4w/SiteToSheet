import logging
import sys
from typing import Optional

def setup_logger(name: str, level: int = logging.INFO, 
                log_format: Optional[str] = None,
                log_file: Optional[str] = None) -> logging.Logger:
    """Configure and return a logger instance."""
    logger = logging.getLogger(name)
    
    # Only configure if handlers don't exist
    if not logger.handlers:
        # Use provided format or default
        formatter = logging.Formatter(
            log_format or '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Add file handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
    logger.setLevel(level)
    return logger


def log_function_call(func):
    "Decorator to log function calls"
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling function '{func.__name__} with args {args} and kweyword arguments {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} returned : {result}")
            return result
        except Exception as e:
            logging.error(f"Function {func.__name__} raised an exception: {e}")
            raise
    return wrapper 

