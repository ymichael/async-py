import argparse
import task
import red
import time


def run():
    print 'WORKER STARTED...'
    task_queue = red.get_queue()
    while True:
        try:
            if len(task_queue) != 0:
                current_task = task_queue.remove()
                async.exec_task(current_task)
            else:
                time.sleep(1)
        except Exception, e:
            print 'ERROR:', str(e)


def main(args):
    redis_conn = red.get_redis_conn(host=args.host, port=args.port, db=args.db)
    redis_queue = red.RedisQueue(args.queue, redis_conn)
    # TODO.



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='async-py task worker')

    # Worker configuration
    worker_config = parser.add_argument_group('Worker configuration')
    worker_config.add_argument('-q', '--queue', required=True,
        help='The async-py task queue to pull tasks from.')

    # Redis connection information.
    redis_information = parser.add_argument_group('Redis connection information')
    redis_information.add_argument(
        '-r', '--host', default='localhost', help='Redis host.')
    redis_information.add_argument(
            '-p', '--port', default=6379, help='Redis port.')
    redis_information.add_argument('-d', '--db', default=0, help='Redis db.')

    args = parser.parse_args()
    main(args)
