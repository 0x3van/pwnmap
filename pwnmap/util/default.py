import os


class DefaultUtil:

    OUT_PATH: str = os.path.join(os.getenv('APPDATA' if os.name == 'nt' else 'HOME'), '.pwnmap1', 'local')    
    """ Default output file path """