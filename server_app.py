from flask import Flask, render_template
from raspberry import RaspberryThread
from light_functions import ojeblink, all_pins_off, light_show,\
cycle_all, allon_show, random_show, simple_show, cleanup
import os

# Load the env variables
if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/blink", methods=['GET'])
def blink_view():
    # Pause any running threads
    any(thread.pause() for thread in threads)

    # Start the target thread if it is not running
    if not blink_thread.isAlive():
        blink_thread.start()
    # Unpause the thread and thus execute its function
    blink_thread.resume()
    return "blink started"


@app.route("/cycleall", methods=["GET"])
def cycleall_view():
    any(thread.pause() for thread in threads)
    if not cycle_all_thread.isAlive():

        cycle_all_thread.start()
    cycle_all_thread.resume()
    return "cycle all started"


@app.route("/lightshow", methods=["GET"])
def lightshow_view():
    any(thread.pause() for thread in threads)
    if not lightshow_thread.isAlive():
        lightshow_thread.start()
    lightshow_thread.resume()
    return "lightshow started"

@app.route("/randomshow", methods=["GET"])
def random_view():
    any(thread.pause() for thread in threads)
    if not randshow_thread.isAlive():
        randshow_thread.start()
    randshow_thread.resume()
    return "random show started"

@app.route("/allon", methods=['GET'])
def allon_view():
    any(thread.pause() for thread in threads)
    if not allon_thread.isAlive():
        allon_thread.start()
    allon_thread.resume()
    return "all on show started"

@app.route("/simpleshow", methods=['GET'])
def simple_view():
    any(thread.pause() for thread in threads)
    if not simple_thread.isAlive():
        simple_thread.start()
    simple_thread.resume()
    return "simple show started"

@app.route("/shutdown", methods=['GET'])
def shutdown():
    all_pins_off()
    any(thread.pause() for thread in threads)
    return "all threads paused"


if __name__ == '__main__':
    # Create threads
    blink_thread = RaspberryThread(function=ojeblink)
    allon_thread = RaspberryThread(function=allon_show)
    randshow_thread = RaspberryThread(function=random_show)
    lightshow_thread = RaspberryThread(function=light_show)
    simple_thread =  RaspberryThread(function=simple_show)
    cycle_all_thread = RaspberryThread(function=cycle_all)

    # collect threads
    threads = [
        blink_thread,
        allon_thread,
        randshow_thread,
        lightshow_thread,
        cycle_all_thread
    ]

    # Run server
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            threaded=True
        )
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
