import bibtexparser
from bibtexparser.bparser import BibTexParser
import os
import glob
import jinja2
import numpy as np

files = glob.glob('_publications/*')
for f in files:
    os.remove(f)

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader="bibliography/",
    autoescape=select_autoescape()
)

templateLoader = jinja2.FileSystemLoader( searchpath="bibliography" )
templateEnv = jinja2.Environment( loader=templateLoader )

template = templateEnv.get_template( "bib_template.md" )

parser = BibTexParser(common_strings=True)
with open('bibliography/publications.bib') as file:
    bib_db = bibtexparser.load(file, parser)

#os.remove("_cv/nocite.tex")


dates = np.array([int(e["year"]) for e in bib_db.entries])

print(dates)

for i in np.argsort(-dates):
    e = bib_db.entries[i]
    e["title"] = e["title"].replace("{","").replace("}","")
    fname = f"_publications/{i:03d}.md"
    authors = e["author"].split(" and ")
    authors = ["<b>"+x+"</b>" if "Callaghan" in x else x for x in authors]
    e["author"] = ", ".join(authors)
    e["journal"] = e["journal"].replace("\\","")
    with open("_cv/nocite.tex", "a") as f:
        f.write(r"\nocite{" + e["ID"] + "}")
        f.write("\n")
    with open(fname, "w") as f:
        f.write(template.render({"e":e, "i": i}))
