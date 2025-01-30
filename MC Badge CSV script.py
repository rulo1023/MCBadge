import json, requests # type: ignore
import csv
import pandas as pd

################################ LOAD DATA ###############################

# Replace this with your competition ID
competition_id = "ExampleChampionship2025"

# URL of the wcif file with all the competition details
url = 'https://worldcubeassociation.org/api/v0/competitions/'+ competition_id +'/wcif/public'
file_name = competition_id + 'json'
response = requests.get(url)
if response.status_code == 200:
    # Saving the json file locally
    with open(file_name, 'w', encoding="utf-8") as json_file:
        json.dump(response.json(), json_file, ensure_ascii=False, indent=4)

    # Opening the json file from local storage
    with open(file_name, 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)

    json.dumps(data, indent=4)
else:
    print(f"Error accesing URL: {response.status_code}")

######################## Events and groups ##############################
    
event_list = ["222", "333", "444", "555", "666", "777", "333bf","333fm", "333oh", 
              "clock", "minx", "pyram", "skewb", "sq1", "444bf", "555bf", "333mbf"]
group_dict, output = dict(), dict()

###################### Extract table with people and tasks per group ####################
stage_count = 4 # Number of stages in the competition (counting side room)
for room in range(stage_count): # You can manually add the codes of your stages as well
    for activity in data["schedule"]["venues"][0]["rooms"][room]["activities"]:
        for group in activity["childActivities"]:
            group_dict[group["id"]] = (group["activityCode"], data["schedule"]["venues"][0]["rooms"][room]["name"])


# Adding the group_ids of the MultiBLD groups (they don't have any subgroups, so they are not added above).
# Just run the code and note the KeyErrors and hardcode them, like group_dict[key] = (custom code, room)
group_dict[123] = ('333mbf-r1-a1', 'Side room') # This is the group_id of the first stage of MultiBLD and the name of the room
group_dict[456] = ('333mbf-r1-a2', 'Side room')
group_dict[789] = ('333mbf-r1-a3', 'Side room')
# ...

# Now we go through everybody's assignments and create a dictionary with the tasks of each person
for person in data["persons"]:
    # Uncoment the following line if you want to filter in or out the staff from the CSV file
    #if (person["registration"]["status"]=="accepted" and person["wcaId"] not in staff): 
    #if  person["wcaUserId"] in staff:
    tasks = dict()
    for assignment in person["assignments"]:
        group = group_dict[assignment["activityId"]]
        # index = group.find("g") + 1
        if assignment["assignmentCode"] == "staff-judge":
            task = "J" 
        elif assignment["assignmentCode"] == "competitor":
            task = "C" 
        elif assignment["assignmentCode"] == "staff-scrambler":
            task = "S" 
        elif assignment["assignmentCode"] == "staff-runner":
            task = "R" 
        elif assignment["assignmentCode"] == "staff-delegate":
            task = "D" 
        elif assignment["assignmentCode"] == "staff-dataentry":
            task = "E"
        elif assignment["assignmentCode"] == "staff-stagelead":
            task = "L"
        # ADD MORE ROLES HERE, AND ASSIGN A DIFFERENT LETTER TO EACH ONE
        tasks[assignment["activityId"]] = task
    output[(person["wcaId"], person["registrantId"])] = tasks
    

# We obtain all the unique keys from the internal dictionaries
columnas = sorted(set(key for diccionario in output.values() for key in diccionario.keys())) # headings for the CSV file

# We create the CSV file
group_list = dict() # List of all groups and the ids of their stages
for elem in group_dict.keys():
    if group_dict[elem][0] not in group_list:
        group_list[group_dict[elem][0]] = []
    group_list[group_dict[elem][0]].append((elem, group_dict[elem][1]))

# Dictionary of the form {1: ('Raúl Cuevas Castillo', 'ES'), 2: ('Gladys Garcés', 'ES'),...
person_dict = dict()
wcaid_set =set()
for person in data["persons"]:
    person_dict[person["registrantId"]] = (person["name"], person["countryIso2"])
    wcaid_set.add(person["wcaId"])

file_path = "" # Set your current path here

# Returns the route to the image of the color of the group (adjust with your own paths and coloured stages)
# This is writing the path to an image of the same colour as the stage, so it can be used in the design program
def get_color(param):
    if param == "Green area":
        return "C:\\green.png" 
    elif param == "Red area":
        return "C:\\red.png"
    elif param == "Yellow area":
        return "C:\\yellow.png"
    elif param == "Orange area":
        return "C:\\orange.png"
    return ""

def get_role(comp_id): # Function to create the "role" column, personalize it with your own roles
    for person in data["persons"]:
        if person["registrantId"] == comp_id:
            if 'staff-dataentry' in person["roles"]:
                return 'Data entry'
            elif 'organizer' in person["roles"]:
                return 'Organizer'
            elif 'delegate' in person["roles"]:
                return 'Delegato'
            elif 'staff-other' in person["roles"]:
                return 'Staff'
            elif 'staff-judge' in person["roles"]:
                return 'Staff'
            elif 'staff-runner' in person["roles"]:
                return 'Staff'
            elif 'staff-scrambler' in person["roles"]:
                return 'Staff'
            return 'Competitor' # Else, just write competitor

# Write the CSV file

staff_ids = [] # Add the staff's WCAID's here so you can filter them in or out of the CSV file


with open(file_path + "output.csv","w",newline="", encoding="utf32") as archivo_csv:
    writer = csv.writer(archivo_csv)
    
    # Variable names are short so they don't take much space in the tables of the design program
    aux = []
    i = 0
    for categoria in group_list.keys():
        aux.append(str(i)) # Task code
        aux.append("c"+str(i)) # Color code
        i += 1
    writer.writerow(['wcaId', 'registrantId', 'name', 'country', 'role'] + aux)
    
    # Events and groups so we know what each column code means
    aux, i = [], 0
    
    for categoria in group_list.keys():
        aux.append(categoria)
        aux.append("stage")
        i += 1
    writer.writerow(['', '', '', '', ''] + aux)
    
    for clave, dictionary in output.items(): # Dict of the form ('2016LOPE37', 1): {5725: 'C'}
        row = []
        for grupo in group_list.keys(): # For each group in the group dictionary
            marker = False
            for subgroup in group_list[grupo]: # For each subgroup inside of the group
                if subgroup[0] in dictionary: # If the person has a task in that subgroup
                    row.append(dictionary[subgroup[0]])
                    # This is an exception if you want data entry to have another color (not in any stage).
                    # Remove the condition if you don't want it, and leave the else statement
                    if dictionary[subgroup[0]] == "E": # This adds a special color for data entry, as they are not in any stage
                        color = "C:\\blue.png"
                    else:
                        color = get_color(subgroup[1])
                    row.append(color)
                    marker = True
                    break
                
            if marker == False: # If the person is not in any subgroup of the group
                row.append("")
                row.append("")
                    
        # This writes (in order) wcaId, registrantId, name, country (flag in .svg), role, tasks in each group, 
        # and the color of the group (rectangular image in .png)
        writer.writerow([clave[0], clave[1], person_dict[clave[1]][0], 'C:\\f\\'+ 
                         person_dict[clave[1]][1].lower()+'.svg', get_role(clave[1])] + row)
        
print("CSV File created successfully.")

# We save it as an excel file if you want, so it can be easily viewed afterwards (if necessary). Publisher also accepts .xlsx files :)

df = pd.read_csv(file_path + "output.csv", encoding="utf32")
df.to_excel(file_path + competition_id + "_output.xlsx", index=False)
print("Excel file created succesfully")