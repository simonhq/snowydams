############################################################
#
# This class aims to get the Snowy Hydro catchment levels
#
# written to be run from AppDaemon for a HASS or HASSIO install
#
# updated: 08/05/2020
# 
############################################################

############################################################
# 
# In the apps.yaml file you will need the following
# updated for your database path, stop ids and name of your flag
#
# snowy_dams:
#   module: snowydams
#   class: Get_Snowy_Dams
#   DAM_FLAG: "input_boolean.check_snowy_dams"
#
############################################################

# import the function libraries
import requests
import datetime
import json
from bs4 import BeautifulSoup
import appdaemon.plugins.hass.hassapi as hass

class Get_Snowy_Dams(hass.Hass):

    # the name of the flag in HA (input_boolean.xxx) that will be watched/turned off
    DAM_FLAG = ""
    URL = "https://www.snowyhydro.com.au/our-energy/water/storages/lake-levels-calculator/"

    up_sensor = "sensor.snowy_dam_last_updated"
    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    # run each step against the database
    def initialize(self):

        # get the values from the app.yaml that has the relevant personal settings
        self.DAM_FLAG = self.args["DAM_FLAG"]

        # create the original sensor
        self.load()

        # listen to HA for the flag to update the sensor
        self.listen_state(self.main, self.DAM_FLAG, new="on")

    # run the app
    def main(self, entity, attribute, old, new, kwargs):
        """ create the sensor and turn off the flag
            
        """
        # create the sensor with the dam information 
        self.load()
        
        # turn off the flag in HA to show completion
        self.turn_off(self.DAM_FLAG)

    def load(self):
        """ parse the ICON Water ACT dam level website
        """

        #connect to the website and scrape the dam levels for the ACT
        url = self.URL
        response = requests.request("GET", url, headers=self.headers, data = self.payload)
        
        #create a sensor to keep track last time this was run
        tim = datetime.datetime.now()
        date_time = tim.strftime("%d/%m/%Y, %H:%M:%S")
        self.set_state(self.up_sensor, state=date_time, replace=True, attributes= {"icon": "mdi:timeline-clock-outline", "friendly_name": "Snowy Dam Levels Data last sourced"})
        
        soup = BeautifulSoup(response.text, "html.parser")

        #get the 7th script block with the variables in it
        page = soup.findAll('script')[14]
        #convert the soup variable into a string so we can manipulate
        tags = str(page)
        self.log(tags)
        #split by the 'var ' so we can get the correct variable values
        stags = tags.split("var ")
        #get the 3rd variable field from the list (lifestyle)
        stags = stags[1]
        self.log(stags)
        #remove the js variable and ; so we get to the raw data
        stags = stags.replace("data_year_current = ", "")
        stags = stags.replace(";", "")
        #convert to json
        jtags = json.loads(stags)
        
        #get yesterdays info
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        yester_date = yesterday.strftime("%Y-%m-%d")

        #get the second series - with percentages and remaining volumes
        dams = jtags['snowyhydro']['level']
        for dam in dams:
            if str(dam["-date"]) == yester_date:
                lakes = dam["lake"]
                for lake in lakes:
                    lname = lake["-name"]
                    ldate = lake["-dataTimestamp"]
                    lvol = lake["#text"]
                
                    if lname == "Lake Eucumbene":
                        sensorname = "sensor.snowy_dam_eucumbene"
                    elif lname == "Lake Jindabyne":
                        sensorname = "sensor.snowy_dam_jindabyne"
                    elif lname == "Tantangara Reservoir":
                        sensorname = "sensor.snowy_dam_tantangara"
                    else:
                        sensorname = ""

                    if sensorname != "":
                        #create the sensors for each of the dams and the combined volumes
                        self.set_state(sensorname, state=lvol, replace=True, attributes= {"icon": "mdi:cup-water", "friendly_name": "Snowy - " + lname + " level", "unit_of_measurement": "%", "Measurement Record Date": ldate})
