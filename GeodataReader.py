#field: call it with LINENAME.FIELDNAME eg SENDER.SCOMPNAME
def get_values(filename,field):
    try:
        fieldname = field.split(".")
    except Exception as error:
        raise
    # reading csv file
    if filename.find('GEODATA')==-1:
        return False
    with open(filename, 'r', encoding="utf8") as data:
        Lines = data.readlines()
        file_dict = {}
        header = {}
        field_values=[]
        # Strips the newline character
        for line in Lines:
            chunks = line.split(";")
            #find the position of the field in the given line
            if chunks[0] == "#DEF" and chunks[1] == "GEODATA:"+fieldname[0]:
                field_pos=chunks.index(fieldname[1])
            if chunks[0] == fieldname[0]:

                field_values.append(chunks[field_pos-1])

    return tuple(field_values)