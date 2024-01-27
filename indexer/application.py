import sys
import signal
import threading

from etc import config
from indexer import data_stream
from indexer.data_filter import operations_callback


stream_stop_event = threading.Event()

""" SEE README """
def application():
    stream_thread = threading.Thread(
        target=data_stream.run,
        args=(config.SERVICE_DID, operations_callback, stream_stop_event,)
    )
    stream_thread.start()

def sigint_handler(*_):
    print('Stopping data stream...')
    stream_stop_event.set()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)