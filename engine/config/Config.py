

ETCD_TTL = 29   # etcd 键过期时间
ETCD_GROUP = "github.com/ferris1/wind"
USE_NATS = True
USE_ETCD = True


def LaunchSingle(is_single):
    global USE_ETCD, USE_NATS
    USE_ETCD = not is_single
    USE_NATS = not is_single
