from enum import Enum


class ProjectPostgresRegExp(str, Enum):
    PCA = r"payment[_\-]collector[a-z_\-]*_postgres"
    ECDL = r"d[_\-]local[a-z_\-]*_postgres"
    LMS = r"[_\-]lite[a-z_\-]*_postgres"


class TerminalColor(str, Enum):
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END_COLOR = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
