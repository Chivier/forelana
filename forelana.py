"""
Author       : Chivier Humber
Date         : 2021-02-22 15:12:15
LastEditors  : Chivier Humber
LastEditTime : 2021-02-22 16:59:14
Description  : forelana is a fortran relation analysis tool
FilePath     : /forelana/forelana.py
"""

import argparse

gFunctionName = []
gFunctionRelation = {}


def LegalCharacter(character) -> bool:
    """
    description: check if character is legal
    param {*} character
    return {*} bool value
    """
    if character.isalnum() or character == "_":
        return True
    else:
        return False


def FindAll(string, substring):
    """
    description: Find all occurrences of substring in string, this is a generator
    param {*} string
    param {*} substring
    return {*}
    """
    start = 0
    while True:
        start = string.find(substring, start)
        if start == -1:
            return
        yield start
        start += len(substring)  # use start += 1 to find overlapping matches


def ReadFile(filename):
    """
    description: Read program from file
    param {*} filename
    return {*} file
    """
    input_file = open(filename, "r")
    result = []
    while True:
        line = input_file.readline()
        if not line:
            break
        result.append(line)
    for line_index in range(len(result)):
        result[line_index] = result[line_index][:-1]  # delete the '\n' of every line
    input_file.close()
    return result


def CommentCheck(line):
    """
    description: check if line is a comment
    param {*} line
    return {*}
    """
    for index in range(len(line)):
        if line[index] != " ":
            if line[index] == "!":
                return True
            else:
                return False
    return False


def ReadCallName(line, st_index):
    """
    description: Read function name
    param {*} line
    param {*} st_index
    return {*} function names
    """
    name = ""
    index = st_index
    while index < len(line):
        if line[index] == " ":
            index = index + 1
            continue
        else:
            break

    while index < len(line):
        if LegalCharacter(line[index]):
            name += line[index]
        else:
            break
        index = index + 1

    return name.upper()


def SubroutineFinding(line):
    """
    description: find all call in a line
    param {*} line
    return {*}
    """
    global gFunctionName
    global gFunctionRelation
    if not "CALL" in line.upper():
        return []
    position_list = list(FindAll(line.upper(), "CALL"))
    # print(position_list)
    name_list = []
    for call_index in position_list:
        name_list.append(ReadCallName(line, call_index + len("CALL")))
    return name_list


def ReadSubroutineName(line):
    """
    description: read the name of a subroutine
    param {*} line
    return {*}
    """
    index = line.upper().find("SUBROUTINE", 0)
    index += len("SUBROUTINE")
    name = ""
    while index < len(line):
        if line[index] == " ":
            index = index + 1
            continue
        else:
            break

    while index < len(line):
        if LegalCharacter(line[index]):
            name += line[index]
        else:
            break
        index = index + 1

    return name.upper()


def PrintCode(code):
    for line in code:
        print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Forelana is a fortran relation analysis tool."
    )

    parser.add_argument(
        "file_path", help="path to the Fortran program to be analyzed", type=str
    )

    args = parser.parse_args()
    fortran_code = ReadFile(args.file_path)

    in_subroutine_flag = False
    subroutine_name = None
    relations = []
    for line in fortran_code:
        if CommentCheck(line):
            continue
        # Exit subroutine
        if "END SUBROUTINE" in line:
            in_subroutine_flag = False
            print(relations)
            continue
        # Enter subroutine
        if "SUBROUTINE" in line:
            in_subroutine_flag = True
            subroutine_name = ReadSubroutineName(line)
            relations = []
            subroutine_name = subroutine_name.lower()
            print("Subroutine " + subroutine_name + " -> ")
            continue

        if in_subroutine_flag:
            call_list = SubroutineFinding(line)
            if len(call_list) > 0:
                relations = list(set(relations + call_list))
