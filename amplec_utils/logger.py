import inspect

class Logger:
    """
    This class will implement a custom logger for the AMPLEC project.
    """
    
    def __init__(self, mode:str, file_path:str=None) -> None:
        """
        Constructor for the Logger-class
        :param mode: mode of the logger, can be 'console', 'file' or 'dual'
        :type mode: str
        :param file_path: path to the file where the logs should be written to
        :type file_path: str
        """
        if mode not in ["console", "file", "dual"]:
            raise ValueError("Mode must be 'console', 'file' or 'dual'")
        if mode != "console" and not file_path:
            raise ValueError("File path must be provided if mode is not 'console'")
        
        self.mode = mode
        self.file_path = file_path
    
    
    def _log(self, message:str, level:str) -> None:
        """
        Logs a message
        
        :param message: message to be logged
        :type message: str
        """
        
        call_tree = self._get_call_tree()
        
        if self.mode in ["console", "dual"]:
            print(f"{level.upper()}: {message}, {call_tree}")
        if self.mode in ["file", "dual"]:
            with open(self.file_path, "a") as f:
                f.write(f"{level.upper()}: {message}, {call_tree}\n")
        
    
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
            if class_name == self.__class__.__name__:
                continue
            if class_name:
                call_hierarchy.append(f"{class_name}.{func_name}")
            else:
                call_hierarchy.append(func_name)
        return " -> ".join(reversed(call_hierarchy))
    
    