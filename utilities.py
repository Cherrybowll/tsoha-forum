def sql_like_escape(input:str):
    input = input.replace("`", "``")
    input = input.replace("%", "`%")
    input = input.replace("[", "`[")
    input = input.replace("]", "`]")
    input = input.replace("_", "`_")
    return input