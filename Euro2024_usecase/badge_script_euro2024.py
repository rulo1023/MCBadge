import json
import csv

################################ CARGAR DATOS ###############################

with open('final.json', 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)

#############################################################################
    
event_list = ["222", "333", "444", "555", "666", "777", "333bf","333fm", "333oh", "clock", "minx", "pyram", "skewb", "sq1", "444bf", "555bf", "333mbf"]

group_dict = dict()

staff = {
    "2010GARC02",
    "2018GODI01",
    "2020DWOR01",
    "2012SANT12",
    "2015GOIK01",
    "2020GROD01",
    "2017DIKY01",
    "2019GEAA01",
    "2017NICO01",
    "2022GOME03",
    "2016LAZA03",
    "2015SANC18",
    "2014IRIA01",
    "2016LOPE37",
    "2022BOGA01",
    "2016WALS01",
    } # only including some staff

output = dict()

###################### get table with people and task per group ####################

for room in [0,1,2,3,4,5]:
    for activity in data["schedule"]["venues"][0]["rooms"][room]["activities"]:
        for group in activity["childActivities"]:
            group_dict[group["id"]] = (group["activityCode"], data["schedule"]["venues"][0]["rooms"][room]["name"])

group_dict[6132] = ('333mbf1-1', 'Side Room')
group_dict[6133] = ('333mbf1-2', 'Side Room')
group_dict[6134] = ('333mbf2-1', 'Side Room')
group_dict[6135] = ('333mbf2-2', 'Side Room')
group_dict[5681] = ('333mbf1-submit', 'Side Room')
group_dict[5682] = ('333mbf2-submit', 'Side Room')
group_dict[5684] = ('555bf-submit', 'Side Room')
#   or

for person in data["persons"]:
    tareas = dict()
    for assignment in person["assignments"]:
        group = group_dict[assignment["activityId"]]
        # index = group.find("g") + 1
        if assignment["assignmentCode"] == "staff-judge":
            task = "J" # + group_dict[assignment["activityId"]][index:]
        elif assignment["assignmentCode"] == "competitor":
            task = "C" # + group_dict[assignment["activityId"]][index:]
        elif assignment["assignmentCode"] == "staff-scrambler":
            task = "S" # + group_dict[assignment["activityId"]][index:]
        elif assignment["assignmentCode"] == "staff-runner":
            task = "R" # + group_dict[assignment["activityId"]][index:]
        elif assignment["assignmentCode"] == "staff-Delegate":
            task = "D" # + group_dict[assignment["activityId"]][index:]
        tareas[assignment["activityId"]] = task
    output[(person["wcaId"], person["registrantId"])] = tareas
    

# Obtain all of the unique keys of the internal dictionaries
columnas = sorted(set(key for diccionario in output.values() for key in diccionario.keys())) # headings


group_list = dict() # List with all of the groups and the ids of their stages
for elem in group_dict.keys():
    if group_dict[elem][0] not in group_list:
        group_list[group_dict[elem][0]] = []
    group_list[group_dict[elem][0]].append((elem, group_dict[elem][1]))
        

person_dict = dict()
wcaid_set =set()
for person in data["persons"]:
    person_dict[person["registrantId"]] = (person["name"], person["countryIso2"])
    wcaid_set.add(person["wcaId"])


def get_color(param):
    if param == "Blue Stage":
        return "C:\\colors\\azul.png"
    elif param == "Green Stage":
        return "C:\\colors\\verde.png"
    elif param == "Yellow Stage":
        return "C:\\colors\\amarillo.png"
    elif param == "Side Room":
        return "C:\\colors\\morado.png"
    elif param == "Red Stage":
        return "C:\\colors\\rojo.png"
    elif param == "Orange Stage":
        return "C:\\colors\\naranja.png"
    return ""



with open("todos.csv","w",newline="", encoding="utf32") as archivo_csv:
    writer = csv.writer(archivo_csv)
    
    aux = []
    i = 0
    for categoria in group_list.keys():
        aux.append("e_"+str(i))
        aux.append("c_"+str(i))
        i += 1
    writer.writerow(['wcaId', 'registrantId', 'name', 'country'] + aux)
    
    aux = []
    i = 0
    for categoria in group_list.keys():
        aux.append(categoria)
        aux.append("stage")
        i += 1
    writer.writerow(['', '', '', ''] + aux)
    
    
    for clave, diccionario in output.items(): # ('2016LOPE37', 1): {5725: 'C'}
        fila = []
        for grupo in group_list.keys(): # For each group in the group dict
            marcador = False
            for subgrupo in group_list[grupo]: #For each subgroup in the group
                if subgrupo[0] in diccionario:
                    fila.append(diccionario[subgrupo[0]])
                    color = get_color(subgrupo[1])
                    fila.append(color)
                    marcador = True
                    break
                
            if marcador == False:
                fila.append("")
                fila.append("")
                    
                
        
        writer.writerow([clave[0], clave[1], person_dict[clave[1]][0], "C:/f/" + person_dict[clave[1]][1].lower()+".svg"] + fila)
    

print("CSV created succesfully exitosamente.")