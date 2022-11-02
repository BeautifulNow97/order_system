# 日志配置
# 是否开启log日志
import os
import datetime

LOG_ENABLED = os.getenv('LOG_ENABLED', 'True').upper() == 'TRUE'
# 是否输出到控制台
LOG_TO_CONSOLE = os.getenv('LOG_TO_CONSOLE', 'True').upper() == 'TRUE'
# 是否输出到文件
LOG_TO_FILE = os.getenv('LOG_TO_FILE', 'True').upper() == 'TRUE'
# 日志等级
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
# 每条日志输出格式
log_format = '%(levelname)s - %(asctime)s - process: %(process)d - %(filename)s - %(name)s - %(lineno)d - %(module)s - %(message)s'
LOG_FORMAT = os.getenv('LOG_FORMAT', log_format)

# 项目绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 日志存放路径
PATH = os.path.join(BASE_DIR, 'logs')
isExists = os.path.exists(PATH)
# 判断结果
if not isExists:
    # 如果不存在则创建目录
    os.makedirs(PATH)
now_date = datetime.datetime.now().strftime("%Y-%m-%d")
# 日志文件的绝对路径
LOG_PATH = os.path.join(PATH, f'proxy-log-{now_date}.log')

from logger import Logger

log = Logger().get_logger()
