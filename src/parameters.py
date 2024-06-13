import os


def check_param(env_name:str, default):
    if(os.environ.get(env_name) == None):    
        os.environ[env_name] = default
    
    return os.environ.get(env_name)
    
TEMP = check_param("TEMP","/app/tmp/")
INPUT_PATH = check_param("INPUT_PATH","/app/input/")
DATA_PATH = check_param("DATA_PATH","/app/data/")

MONGO_HOST = check_param("MONGO_HOST","mongo")
MONGO_USER = check_param("MONGO_USER","root")
MONGO_PASS = check_param("MONGO_PASS","1234qweR")
MONGO_PORT = check_param("MONGO_PORT","27017")




