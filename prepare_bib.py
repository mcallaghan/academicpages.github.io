import bibtexparser
from bibtexparser.bparser import BibTexParser
import os
import glob
import jinja2
import numpy as np
import re
from datetime import datetime as dt
from pylatexenc.latex2text import LatexNodes2Text


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
with open('bibliography/callaghan-publications.bib') as file:
    bib_db = bibtexparser.load(file, parser)

#os.remove("_cv/nocite.tex")

bib_db.entries = [x for x in bib_db.entries if re.match("\w",x["title"])]

dates = np.array([dt.strptime(f'{e["year"]}-{e["month"]}',"%Y-%B") for e in bib_db.entries])

print(dates)

n = 0
for i in np.argsort(dates)[::-1]:
    n+=1
    e = bib_db.entries[i]
    print(e)
    e["title"] = e["title"].replace("{","").replace("}","")
    fname = f"_publications/{n:03d}.md"
    authors = e["author"].split(" and ")
    authors = ["<b>"+x+"</b>" if "Callaghan" in x else x for x in authors]
    e["author"] = ", ".join(authors)
    e["journal"] = e["journal"].replace("\\","")
    e["author"] = LatexNodes2Text().latex_to_text(e["author"])
    with open("_cv/nocite.tex", "a") as f:
        f.write(r"\nocite{" + e["ID"] + "}")
        f.write("\n")
    with open(fname, "w") as f:
        f.write(template.render({"e":e, "i": n}))
