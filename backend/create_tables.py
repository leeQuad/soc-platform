from app.db.base import Base
from app.db.session import engine
from app.models.port_scan import PortScan
from app.models.log_parse import LogParse
from app.models.file_integrity import FileIntegrity
from app.models.user import User
from app.models.alert import Alert
from app.models.threat import Threat

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")