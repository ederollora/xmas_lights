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
    any(thread.pause() for thread in threads)
    if not blink_thread.isAlive():
        blink_thread.start()
    blink_thread.resume()
    return "Blinking started"

@app.route("/cycleall", methods=["GET"])
def cycleall_view():
    any(thread.pause() for thread in threads)
    if not cycle_all_thread.isAlive():
        cycle_all_thread.start()
    cycle_all_thread.resume()
    return "Cycle all started"

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
    return "Random show started"

@app.route("/allon", methods=['GET'])
def allon_view():
    any(thread.pause() for thread in threads)
    if not allon_thread.isAlive():
        allon_thread.start()
    allon_thread.resume()
    return "All on started"

@app.route("/simpleshow", methods=['GET'])
def simple_view():
    any(thread.pause() for thread in threads)
    if not simple_thread.isAlive():
        simple_thread.start()
    simple_thread.resume()
    return "simple show started"

@app.route("/shutdown", methods=['GET'])
def shutdown():
    any(thread.pause() for thread in threads)
    all_pins_off()
    return "All threads paused and lights shut down"

@app.route("/showthreads", methods=['GET'])
def showthreads():
    any(print(thread) for thread in threads)
    return "checking thread stated"


if __name__ == '__main__':
    # Create threads
    blink_thread = ChristmasLightThread(function=ojeblink, "Ojeblink")
    allon_thread = ChristmasLightThread(function=allon_show, "All Lights On")
    randshow_thread = ChristmasLightThread(function=random_show, "Random Show")
    lightshow_thread = ChristmasLightThread(function=light_show, "Light Show")
    simple_thread =  ChristmasLightThread(function=simple_show, "Simple Show")
    cycle_all_thread = ChristmasLightThread(function=cycle_all, "Cycle All")
    # collect threads
    threads = [
        blink_thread,
        allon_thread,
        randshow_thread,
        lightshow_thread,
        simple_thread,
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
