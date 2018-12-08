from os import path

def dump(filename, list):
    file = open("bulks/"+filename+".bulk", "w", encoding='utf-8')
    for item in list:
        text = str(item.bulk())
        file.write(text+'\n')

    file.close()
    return path.abspath(file.name)
