import json, logging, sys, os, datetime, re 
from PySide6.QtWidgets import QMessageBox

# For displaying error messages with the critical icon
class ErrorBox(QMessageBox):
    def __init__(self, msg):
        super().__init__()
        self.setText(msg)
        self.setIcon(QMessageBox.Icon.Critical)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

parent_dir = resource_path(os.path.dirname(os.path.dirname(__file__))) # Get the parent directory of the current file path

def read_config() -> dict:
    '''Read the config.json file and return contents as a dictionary'''
    try: 
        with open(parent_dir + "\\config\\config.json") as fconfig:
            config = json.load(fconfig)
            return config
    except Exception as e:
        print("Failed to open config.json: ", e)
        raise e 
    
def update_config(newdict: dict) -> None:
    '''Update the config.json file'''
    try:
        with open(parent_dir + "\\config\\config.json", "w") as fconfig:
            json.dump(newdict, fconfig, indent=4)
    except Exception as e:
        print("Failed to update config.json")
        raise e

def get_logger(name: str, mode='a') -> logging.Logger:
    '''Return a logger object with the name (name), with default mode of "a" (append)'''
    config = read_config()["logging"]
    logging.basicConfig(level=logging.DEBUG, format=config["format"], style="{", filename=os.path.dirname(__file__) + config["outfile"], filemode=mode)
    return logging.getLogger(name)

def get_datetime_now():
    '''Return the current date time in the specified format (e.g. 2025-05-06 18:48:20+08)'''
    return datetime.datetime.now().astimezone().isoformat(timespec='seconds', sep=' ')

def check_task_re(task: str) -> tuple:
    '''Checks using regex if ^[NUM]-[NUM]^ exists in the string 'task' '''
    s = re.search(r"\^\d+-\d+\^", task)
    if s:
        s = s.group()
        idx = task.find(s)
        nums = [int(i) for i in re.findall("\\d+", s)]
        start, end = sorted(nums)
        return True, (int(start), int(end)), (task[:idx], task[idx + len(s):])
    else:
        return False, None, None

