import time, sys, threading

class Spinner:
    busy = False
    delay = 0.1
    
    @staticmethod
    def spinning_cursor():
        while True:
            for cursor in '|/-\\': yield cursor
    
    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()
    
    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        sys.stdout.flush()
        time.sleep(self.delay)

spinner = Spinner()

def wrapper(func, args, res):
    res.append(func(*args))

def submit_and_monitor_thread(func=None, args=None):
    '''
    # func = Name of the function : String
    # args = List of arguments : Tuple
    '''
    if not func:
        Print("Error: Function required")

    sys.stdout.write("Running "+str(func.__name__)+" ... ")
    res = []
    t = threading.Thread(target = wrapper, args = (func, args, res))
    spinner.start()
    t.start()
    while t.is_alive():
        t.join(0.2)
    spinner.stop()
    print("done")
    if res:
	    return res[0]