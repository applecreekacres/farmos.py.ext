"""Formats Johnny's growing information in to a Defintion List for FarmOS."""

with open('in') as form:
    with open('out', 'w') as out:
        out.write("<dl>")
        for line in form.readlines():
            out.write("<dt>{}".format(line.replace("\n\n", "\n").replace(
                ":", ":</dt><dd>").replace("\n", "</dd>\n")))
        out.write("</dd>")
        out.write("</dl>")
