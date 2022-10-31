def conclusion_of_the_questionnaire(data):
    return data["img_path"], "{0}, {1}, {2}, {3}".format(
        data["name"], 
        data["user_age"],
        data["user_city"],
        data["user_info"])
