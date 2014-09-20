import async
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


if __name__ == '__main__':
    run()
