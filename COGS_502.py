
import PySimpleGUI as sg
import random
import time
import pandas as pd #save responses to .CSV file
import pyminizip #create encrypted .Zip file
import os
import pandas._libs.tslibs.base #necessary to generate working .exe file

response_dict = {}
recall_dict = {}
acceptance = []

def intro():
    sg.theme("DarkAmber")

    layout = [[sg.Text("Welcome!")],
              [sg.Text("My name is Eren Irmak. I am student in Cognitive Sciences, MA, Yeditepe University.")],
              [sg.Text("This program is created for free recall experiment.\nWhen you click the button, a window with Demographic questions will appear.\nPlease respond to all questions.")],
              [sg.Text("Then, trials will begin. There will be 3 sets, and at the end of the each set,\nyou will be required to type as many words as you can without any time limit.")],
              [sg.Text("When the trials are completed, there will be a ZIP file created with your name.\nIt is necessary to send it:\neren.irmak@std.yeditepe.edu.tr")],
              [sg.Text("Your data will be protected and will not be used in any other way.\nThis experiment is conducted under the supervision of Assoc. Prof. Funda Yıldırım Cengiz.\nIf you have any questions, you can reach out to me via my e-mail.")],
              [sg.Text("If you accept participating in the study, please type YES into the box.")],
              [sg.InputText()],
              [sg.Button("OK")]]

    window = sg.Window("Introduction", layout, finalize = True)

    while True:
        event, value = window.read()

        if value != None:
            acceptance.append(value[0])
        if event in (sg.WIN_CLOSED, "OK"):
            break
                
    window.close()

def demographics():
    sg.theme("DarkAmber")

    layout = [
                [sg.Column([
                    [sg.Text("First Name:")],
                    [sg.Text("Last Name: ")],
                    [sg.Text("Age:")]]),
                sg.Column([
                    [sg.InputText(size = 18)],
                    [sg.InputText(size = 18)],
                    [sg.InputText(size = 18)]])],
                [sg.Text("Gender:")],
                [sg.Radio("Male", "gender"), sg.Radio("Female", "gender"), sg.Radio("Non-Binary", "gender")],
                [sg.Text("Which hand do you use more often?")],
                [sg.Radio("Right", "handedness"), sg.Radio("Left", "handedness")],
                [sg.Text("How many languages do you know?")],
                [sg.Radio("1", "languages"), sg.Radio("2", "languages"), sg.Radio("3+", "languages")],
                [sg.Text("Degree of education")],
                [sg.Radio("High school", "education"), sg.Radio("Bachelor's Degree", "education"), sg.Radio("Master's Degree", "education"), sg.Radio("PhD", "education")],
                [sg.Text("Did you have classes in English?")],
                [sg.Radio("Yes", "eng_class"), sg.Radio("No", "eng_class")],
                [sg.Text("How many hours a day do you use the computer?")],
                [sg.InputText(size = 10)], #sg.Radio("1-3", "comp_usage"), sg.Radio("4-6", "comp_usage"), sg.Radio("7+", "comp_usage")
                [sg.Text("Do you have any eye-related health issues? (e.g. color blindness)")],
                [sg.Radio("Yes", "eye_problem"), sg.Radio("No", "eye_problem")],
                [sg.Submit()]
             ]

    window = sg.Window("Demographics", layout, finalize = True)
    while True:
        event, values = window.read()

        if event == "Submit":
            if values[0] == "" or values[1] == "" or values[2] == "" or True not in (values[3], values[4], values[5]) or True not in (values[6], values[7]) or True not in (values[8], values[9], values[10]) or True not in (values[11], values[12], values[13], values[14]) or True not in (values[15], values[16]) or values[17] == "" or True not in (values[18], values[19]):
                sg.Popup("Please answer all questions.", title = "Warning")
            else:
                get_values(values)
                break

        if event == sg.WIN_CLOSED:
            sg.Popup("Your answers are not saved. Thank you for your time.", title = "Good Bye")
            break

    window.close()

def get_values(values):
    
    response_dict["Name"] = values[0]
    response_dict["Last Name"] = values[1]
    response_dict["Age"] = values[2]
    
    if values[3] == True:
        response_dict["Gender"] = "Male"
    elif values[4] == True:
        response_dict["Gender"] = "Female"
    elif values[5] == True:
        response_dict["Gender"] = "Non-Binary"

    if values[6] == True:
        response_dict["Hand"] = "Right"
    elif values[7] == True:
        response_dict["Hand"] = "Left"

    if values[8] == True:
        response_dict["Languages"] = 1
    elif values[9] == True:
        response_dict["Languages"] = 2
    elif values[10] == True:
        response_dict["Languages"] = 3

    if values[11] == True:
        response_dict["Education"] = "High School"
    elif values[12] == True:
        response_dict["Education"] = "Bachelor's Degree"
    elif values[13] == True:
        response_dict["Education"] = "Master's Degree"
    elif values[14] == True:
        response_dict["Education"] = "PhD"

    if values[15] == True:
        response_dict["English Classes"] = "Yes"
    elif values[16] == True:
        response_dict["English Classes"] = "No"

    response_dict["Computer (hour/day)"] = values[17]

    if values[18] == True:
        response_dict["Eye Problem"] = "Yes"
    elif values[19] == True:
        response_dict["Eye Problem"] = "No"

def experiment_set(color = "default"):
    word_list = ["love", "woman", "girl", "time", "life", "letter", "body", "corner", "blood", "knowledge",
                 "rock", "death", "position", "village", "journal", "direction", "soul", "money", "health", "cost"]
    
    if color == "default":
        color = "black"

    width, height = sg.Window.get_screen_size()
    
    layout = [[sg.Text("", text_color=color, font = ("default", 24), pad = ((0, 0), (height / 2 -24, 0)), background_color = "white", key="text")]]
    window = sg.Window("", layout, no_titlebar = True, background_color="white", location = (0, 0), element_justification = "center", force_toplevel = True, modal = True, keep_on_top = True, finalize = True) 
    window.Maximize()
    
    turns = 20
    used_index = []
    for turn in range(turns):
    
        rand_index = random.randint(0, 19)
        if rand_index not in used_index:   #to check whether randomed earlier      
            used_index.append(rand_index) 
        else:
            while rand_index in used_index:
                rand_index = random.randint(0, 19)
            used_index.append(rand_index)
    
        
        for i, w in enumerate(word_list):
            if used_index[-1] == i:
                random_text = w
                window["text"].update(f"{random_text}") #send randomly selected word to gui
        
        window.read(timeout = 5)
    
        time.sleep(5)

    window.close()

def recall_responses(color = "default"):
    if color == "default":
        color = "black"

    layout = [
                [sg.Text("Enter the words you remember:")],
                [sg.InputText()],
                [sg.Button("Save Answers")]
             ]

    window = sg.Window("Answers", layout, finalize = True)
    while True:
        event, values = window.read()

        if values[0] == "":
            sg.Popup("You haven't type any words.", title = "Info")        
        elif event == "Save Answers":
            sg.Popup("Your answers are saved.", title = "Info")
            recall_values(color, values)
            break
        
        if event == sg.WIN_CLOSED:
            break

    window.close()

def recall_values(color, values):
    recall_dict[f"{color}"] = values[0] # color : response pair

def write_to_file(): # may be modified for encryption
    df = pd.DataFrame([response_dict])
    df2 = pd.concat([df, pd.DataFrame([recall_dict])], axis = 1)
    df2.to_csv("{name}.csv".format(name = response_dict["Name"]), encoding = "utf-8", index=False)


def reminder():
    layout = [[sg.Text("You have completed the experiment.")],
              [sg.Text("There is a file created with your name.")],
              [sg.Text("Please send the file to:\neren.irmak@std.yeditepe.edu.tr")],
              [sg.Text("For further questions, you can contact me via this e-mail.")],
              [sg.Text("Thank you for your participation.")],
              [sg.Button("OK")]]
    window = sg.Window("Reminder", layout, finalize = True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "OK"):
            break

    window.close()

def security_measurements():
    #Compress and Encrypt
    file = "./{name}.csv".format(name = response_dict["Name"])
    pre = None
    output = "./{name}.zip".format(name = response_dict["Name"])
    password = "do not touch!"
    com_lvl = 5
    pyminizip.compress(file, None, output, password, com_lvl)

    os.remove("{name}.csv".format(name = response_dict["Name"]))



intro()
acceptance.append(0)
if acceptance[0] == "YES":
    demographics()

#if demographics not completed, don't start the experiment
if response_dict != {} and os.path.exists("{name}.zip".format(name = response_dict["Name"])) == False:
    experiment_set()
    recall_responses()
    
    experiment_set("green")
    recall_responses("green")

    experiment_set("red")
    recall_responses("red")
    
    write_to_file()
    security_measurements()

    reminder()
