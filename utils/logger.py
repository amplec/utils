import inspect
from typing import Optional
from elasticsearch import Elasticsearch
from datetime import datetime
from zoneinfo import ZoneInfo

class Logger:
    """
    This class will implement a custom logger for the AMPLEC project.
    """
    
    def __init__(self, mode:str, elastic_url:Optional[str] = None, elastic_key:Optional[str] = None, elastic_index:Optional[str]="amplec_logs") -> None:
        """
        Constructor for the Logger-class
        :param mode: mode of the logger, can be 'console', 'elastic' or 'dual'
        :type mode: str
        :param elastic_url: URL to the ElasticSearch instance
        :type elastic_url: str
        :param elastic_key: API key for the ElasticSearch instance
        :type elastic_key: str
        :param elastic_index: Index in the ElasticSearch instance
        :type elastic_index: str
        """
        if mode not in ["console", "elastic", "dual"]:
            raise ValueError("Mode must be 'console', 'elastic' or 'dual'")
        if mode != "console" and not (elastic_url and elastic_key):
            raise ValueError("Elastic parameters need to be provided if mode is not 'console'")
        
        self.mode = mode
        self.elastic_url = elastic_url
        self.elastic_key = elastic_key
        self.elastic_index = elastic_index
    
    
    def _log(self, message:str, level:str) -> None:
        """
        Logs a message
        
        :param message: message to be logged
        :type message: str
        """
        
        call_tree = self._get_call_tree()
        
        if self.mode in ["console", "dual"]:
            print(f"{level.upper()}: {message}, {call_tree}")
        if self.mode in ["elastic", "dual"]:
            Elasticsearch(self.elastic_url, api_key=self.elastic_key).index(index=self.elastic_index, body={"message": message, "level": level, "call_tree": call_tree, "ts": datetime.now(ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%dT%H:%M:%S%z")})
        
    
    def info(self, message:str) -> None:
        """
        Logs an info message
        
        :param message: message to be logged
        :type message: str
        """
       
        self._log(message, "info")
    
    def warning(self, message:str) -> None:
        """
        Logs a warning message
        
        :param message: message to be logged
        :type message: str
        """
        
        self._log(message, "warning")
        
    def error(self, message:str) -> None:
        """
        Logs an error message
        
        :param message: message to be logged
        :type message: str
        """
        
        self._log(message, "error")
        
    def debug(self, message:str) -> None:
        """
        Logs a debug message
        
        :param message: message to be logged
        :type message: str
        """
        
        self._log(message, "debug")
        
        
    
    def _get_call_tree(self) -> str:
        stack = inspect.stack()
        call_hierarchy = []
        for frame_info in stack[1:]:  # Skip the current function
            frame = frame_info.frame
            func_name = frame_info.function
            class_name = frame.f_locals.get('self', None).__class__.__name__ if 'self' in frame.f_locals else None
            # Skip frames from the logger itself
            if func_name in ["<module>","translate_proxy_headers"] or class_name == "<module>":
                continue
            if class_name == self.__class__.__name__:
                continue
            if class_name in ["Thread","ThreadedTaskDispatcher", "HTTPChannel", "WSGITask", "Flask", "StructuredTool"]:
                continue
            if class_name:
                call_hierarchy.append(f"{class_name}.{func_name}")
            else:
                call_hierarchy.append(func_name)
        return " -> ".join(reversed(call_hierarchy))
    
    