# https://www.tutorialspoint.com/python/string_split.htm


def splitSections(fileContent: str) -> list:
    """Splits the skin.ini file into the different sections, returns an object with following structure

    Numbers aren't parsed, they're kept as strings.
    Lists however are converted into a list of strings:

        {
            "General": {
                "Name": str,
                "Autor: str
                # ...
            },

            "Colours": {
                "Combo1": list(str),
                "Combo2": list(str)
                # ...
            },

            "Fonts": {
                "ScoreOverlap": str,
                "ComboOverlap": str
                # ...
            },

            "Mania1k": {
                "Keys": str,
                "ColumnWidth": list(str),
                "HitPosition": str
                # ...
            }
        }
    """

    # Filters empty lines and comments (comments start with ";" or "//")
    # and joins them to a single string again
    fileContent = "\n".join([line for line in fileContent.split("\n") if line and not line.startswith(
        "//") and not line.startswith(";")])

    # Final object we will be returning
    parsedObject = {}

    # Every section starts with a word in square brackets
    # (Example: "[General]") so if we split everything at the beginning
    # of a square brackets we will get an array of each section as an string array element

    # Example:

    #     [
    #         "",
    #         "General]\nName: Skin Example\nAuthor: IceDynamix ...",
    #         "Colours]\nCombo1: 0,0,0,0\nCombo2\n0,0,0,0",
    #         "Fonts]\nScoreOverlap: 10\nComboOverlap: 10..."
    #     ]

    # Note: The closing square bracket is still there in the element,
    # because when splitting at a string, it's removed from the element

    # Note: There's an empty element at the beginning, because we split at
    # a string which is at the very beginning of the file. The file starts with
    # "[General]", after all

    sections = fileContent.split("[")

    for section in sections:
        # Remember the closing square bracket? We just crab rave it
        # by replacing it with an empty string. Then we split the
        # section into the lines by splitting at each newline character.

        # Example for [General] section:

        #     [
        #         "General,"  # closing square bracket is gone now!
        #         "Name: Skin Example",
        #         "Author: IceDynamix",
        #         "Version: 2.5",
        #     ]

        lines = section.replace("]", "").split("\n")

        # Just a simple check, not sure if this is even necessary
        # but better be safe than sorry
        if len(lines) == 0:
            continue

        # Looking at our example, it should be clear that the section title
        # is the very first element. Therefore, the section content is
        # everything after that.
        sectionTitle = lines[0]
        sectionTextContent = lines[1:]

        # Our section object is going to look like this for the [General] section:

        #     {
        #         "Name": "Skin Example",
        #         "Author": "IceDynamix",
        #         "Version": "2.5",
        #     }

        # Note: This is a proper python object now, you can call the
        # properties with something like `section["Name"]`.
        # `print(section["Name"])` for the General section would
        # print "IceDynamix" in the console.

        sectionObject = {}

        for attribute in sectionTextContent:

            if attribute == "":  # Another simple null check
                continue

            # Since each attribute is saved as something like
            # "{key}: {value}" (Example: "Name: Skin Example"
            # where Name would be the key and Skin Example would be the
            # value) and both elements are seperated by a colon and a space.
            # Splitting the line at "; " gives us an array of [key,value],
            # so we assign the key from [0] and the value from [1].

            keyValuePair = attribute.split(": ")
            key = keyValuePair[0]
            value = keyValuePair[1]

            # Detects if the value is an array by checking for a comma
            if "," in value:
                value = value.split(",")

            # Adds the key value pair to the object
            sectionObject[key] = value

        # Sections in .ini files have to be unique. Our skin.ini contains
        # multiple [Mania] sections for each keymode though, that's why your
        # configloader failed. Objects also have to have unique identifiers,
        # otherwise we'd be overwriting the same object attribute over and over
        # again, until everything is finished. That's why the attribute is edited
        # to be "Mania4k", "Mania5k" etc.

        if sectionTitle == "Mania":
            sectionTitle = "Mania" + sectionObject["Keys"] + "k"

        # Adding each section to the final object
        parsedObject[sectionTitle] = sectionObject

    return parsedObject


# This code should be trivial
def main():
    iniPath = "skin.ini"
    with open(iniPath, "r") as ini:
        fileContent = ini.read()
    sections = splitSections(fileContent)
    print(sections)


# This is just to protect ourselves. It will only jump into the if
# if this is the executed file. If this file were to be imported via
# `import skinini`, it would run everything at base layer. We don't want
# that to happen. Of course it's irrelevant right now as this is a single file
# project, but it's just good practice in general
if __name__ == "__main__":
    main()
