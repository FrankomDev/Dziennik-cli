def format_hour(data) -> str:
    data = str(data).split("T")[1].split(":")[0:2]
    return f"{data[0]}:{data[1]}"

def format_date(data) -> str:
    data = str(data).split("T")[0].split("-")
    return f"{data[2]}.{data[1]}.{data[0]}"

def reformat_date(data) -> str:
    data = str(data).split(".")
    return f"{data[2]}-{data[1]}-{data[0]}"

frekwencja_str = {
    1: "Obecność",
    2: "Nieobecność",
    3: "Nieobecność usprawiedliwiona",
    4: "Spóźnienie",
    5: "Spóźnienie usprawiedliwione",
    6: "Nieobecność z przyczyn szkolnych",
    7: "Zwolnienie"
}

sprawdziany_str = {
    1: "Sprawdzian",
    2: "Kartkówka",
    3: "Praca klasowa",
    4: "Zadanie domowe"
}