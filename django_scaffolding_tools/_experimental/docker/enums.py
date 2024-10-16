from enum import Enum


class ProjectPostgresRegExp(str, Enum):
    CLAVE = r"clave[a-z_\-]*_postgres"
    CUP = r"[_\-]cupos[a-z_\-]*_postgres"
    ECDL = r"d[_\-]local[a-z_\-]*_postgres"
    LMS = r"[_\-]lite[a-z_\-]*_postgres"
    MIN = r"[_\-]?mobile[a-z_\-]*_postgres"
    MPI = r"multipagos[a-z_\-]*_postgres"
    OXXO = r"oxxo[a-z_\-]*_postgres"
    PCA = r"payment[_\-]collector[a-z_\-]*_postgres"
    PJ_PAYMENT = r"[_\-]?pj_django_payments[a-z_\-]*_postgres"
    PPI = r"puntopago[a-z_\-]*_postgres"
    PQP = r"[_\-]?queue_[a-z_\-]*_postgres"
    PRO = r"payment[_\-]router[a-z_\-]*_postgres"
    REFACIL = r"refacil[a-z_\-]*_postgres"
    SIX = r"six[a-z_\-]*_postgres"
    SLACK = r"[_\-]?slack_[a-z_\-]*_postgres"
    WOMPI = r"wompi[a-z_\-]*_postgres"
    MONITORING = r"monitoring[a-z_\-]*_postgres"
    WUI = r"wu[a-z_\-]*_postgres"

    # = r"oxxo[a-z_\-]*_postgres"


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
