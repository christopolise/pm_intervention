from time import sleep
from pyvesync import VeSync
from yaml import safe_load
import datetime

with open("cred.yaml") as f:
    config = safe_load(f)

manager = VeSync(config["email"], config["password"], "TIME_ZONE", debug=False)
manager.login()
manager.update()
my_fan = manager.fans[0]
my_fan.manual_mode()  # Not entirely sure why but this seems necessary
my_fan.change_fan_speed()  # Not entirely sure why but this seems necessary

while True:

    if (
        datetime.datetime.now().hour == config["trigger_time"]["hour"]
        and datetime.datetime.now().minute == config["trigger_time"]["min"]
    ):
        my_fan.change_fan_speed(speed=4)
        while (
            not datetime.datetime.now().hour
            == config["trigger_time"]["hour"] + config["cleaning_interval"]["hour"]
            and datetime.datetime.now().minute
            <= config["trigger_time"]["min"] + config["cleaning_interval"]["min"]
        ):
            sleep(60)

    if my_fan.air_quality >= config["aq_threshhold"]:
        my_fan.change_fan_speed(speed=4)
        # We'll figure out how to adapt
    else:
        if my_fan.fan_level != 1:
            my_fan.change_fan_speed(speed=1)
