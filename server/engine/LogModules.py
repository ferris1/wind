
import sys, logging, logging.handlers


def init_logging(srv):
    file_name = f'{srv.name}.{((str(sys.argv[1])) if len(sys.argv) > 1 else "")}'
    set_logging(f"{srv.name}", True, file_name=file_name)


def set_logging(name="test", to_console=True, to_file=True, file_name=""):
    cp = "./log"
    from pathlib import Path
    Path(cp).mkdir(parents=True, exist_ok=True)
    log_level = logging.INFO

    format_str = f'[wind][%(asctime)s][{name}][%(levelname)s][%(filename)s:%(lineno)d %(funcName)s]: %(message)s'
    formatter = logging.Formatter(format_str)
    logging.getLogger().handlers.clear()

    # 到控制台
    if to_console:
        c_handle = logging.StreamHandler()
        c_handle.setLevel(log_level)
        c_handle.setFormatter(formatter)
        logging.getLogger().addHandler(c_handle)

    # 每天一个日志文件
    if to_file and file_name is not None:
        file_out = cp + "/" + file_name + '.log'
        tf_handler = logging.handlers.TimedRotatingFileHandler(file_out, 'D', 1, 0, 'utf-8')
        tf_handler.setLevel(log_level)
        tf_handler.setFormatter(formatter)
        logging.getLogger().addHandler(tf_handler)

