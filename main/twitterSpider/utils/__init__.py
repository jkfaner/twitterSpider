from datetime import datetime

from ..settings import *
from ..utils.sqlite import SQLit3Connection


class ConfigAnalysis(SQLit3Connection):
    # 项目启动时间
    obj_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __init__(self):
        super(ConfigAnalysis, self).__init__()

        self.username = USERNAME
        self.password = PASSWORD
        self.user_agent = USER_AGENT