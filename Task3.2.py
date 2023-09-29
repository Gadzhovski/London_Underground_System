"""THE TASK IS TO BUILD COMMAND LINE INTERFACE TO DISPLAY THE OPERATION OF DIFFERENT TFL SERVICE"""
"""The program use real data from tfl to show CLI"""

import requests as rqs
import xmltodict as xmldic
import datetime

class London_underground_info:
    def __init__(self):
        self.lines = {}
        self.disrupt = []
        self.underground()
        self.print_realtime_data()

    def underground(self):
        # fetching the real time data about tfl condition from cloud
        real_time_data = "\n".join(rqs.get("http://cloud.tfl.gov.uk/TrackerNet/LineStatus").text.split("\n")[1:])
        lines_information = xmldic.parse(real_time_data)["ArrayOfLineStatus"]["LineStatus"]

        # running loop in the file,
        for line in lines_information:
            if line["BranchDisruptions"]:
                data = line["BranchDisruptions"]["BranchDisruption"]
                if isinstance(data, list):
                    for disruption in data:
                        disruption_data = [disruption["StationFrom"]["@Name"], disruption["StationTo"]["@Name"], ]
                        if disruption.get("StationVia"):
                            disruption_data.append(disruption["StationVia"]["@Name"])
                        if disruption_data not in self.disrupt:
                            self.disrupt.append(disruption_data)
                else:
                    disruption = data
                    disruption_data = [disruption["StationFrom"]["@Name"], disruption["StationTo"]["@Name"], ]
                    if disruption.get("StationVia"):
                        disruption_data.append(disruption["StationVia"]["@Name"])
                    if disruption_data not in self.disrupt:
                        self.disrupt.append(disruption_data)

            # storing the data in dictionary named self.lines,
            self.lines[line["Line"]["@Name"]] = {
                "Conditions": line["Status"]["@Description"],
                "Description": line["@StatusDetails"].replace("GOOD SERVICE", "Good service"),
                "Disruption": self.disrupt
            }

    # function to print data after loading all the daTA
    def print_realtime_data(self):
        now = datetime.datetime.now()
        today = now.strftime("%H:%M" + " - " + "%d/%m/%Y")
        print(
            f" \n Time: {today} \n Information for London Underground, "
            f"Overground ,DLR and Trams \n ")
        for line, value in self.lines.items():
            print(f" >>>> {line} \n {'Line' if line not in ['TfL Rail'] else ''}")
            if value["Conditions"] == "Good Service":
                print(" ✓ No disruptions, Enjoy your journey")
                print("")

            elif value["Description"]:
                print(f" -✘-✘- {value['Conditions']} ----> {value['Description']}")
                if value["Disruption"]:
                    print(" *** Influenced area !: " + " | ".join(
                        f"{i[0]} to {i[1]}{' via ' + i[2] if len(i) == 3 else ''}" for i in value["Disruption"]),
                          "\n !** Please !, Consider alternating routes")
                    print("")


London_underground_info()
