# Comarques de Catalunya deck

## Genreating the images of each comarca
It was not possible to use ChatGPT to modify a raster file (png) to highlight each comarca, so I found  SVG file I could manipulate.
- [catalunya.svg](https://commons.wikimedia.org/wiki/File%3AMapa_comarcal_de_Catalunya.svg
  ) — A map of the comarques without text. I modified one `path` to make it `red`.
- [catalunya-comarques.svg](https://upload.wikimedia.org/wikipedia/commons/2/26/Comarcas_de_Catalu%C3%B1a.svg) — A map of the comarques with the comarca names but not the capitals. It includes Moianès.
- [catalunya-toponims-original.svg](https://upload.wikimedia.org/wikipedia/commons/a/af/CatMCVPtoponims.svg) — The map I end up using, including Municipis and more text. Does not include Moianès.
- `catalunya-toponims.svg` — The map I ended up using, with the Municipis removed. 

I have not explored the possibility of using other formats like geojson or topojson, available at [catalonia-cartography](https://github.com/sirisacademic/catalonia-cartography) GitHub repo.

### Manipulating the SVG with Python
I used the libraries `lxml` and `cairosvg`.

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install lxml
$ pip install cairosvg
```

I manually modified `catalunya-toponims.svg` removing municipalities and identifying paths of each comarca in their `path@id`.

- `catalunya-list-comarques-svg.py` — List the comarques in the SVG file.
- `catalunya-convert-svg-to-png.py` — Convert a single SVG file to PNG, 800 pixels wide.
- `catalunya-generate-each-comarca.py` — Generate a PNG file for each comarca, highlighting the border in red.


## Creatting the markdown
Prompt used with ChatGPT.

```markdown
Create a markdown file named catalunya.md. The heading of the file will be:

# Comarques de Catalunya
 
---

Deck: Comarques de Catalunya
Tags: catalunya


The footer of the file will be:

---

Generated by ChatGPT


For each of the comarques of Catalunya I want you to create two entries between the header and the footer. One entry asking for the capital of the comarca and the other entry asking for the comarca que city is capital of. Each entry needs a sequential number and I want the comarques processed in alphabetical order. Each entry will use the images generated previous ly. For both questions use the same image.

Use the following as an example of the entries:

1. Quina és la capital de la comarca del **Berguedà**?
> La capital de la comarca del Berguedà és **Berga**.
>
> ![Berguedà](images/bergueda.png)

2. De quina comarca **Berga** és la capital?
> Berga és la capital del **Berguedà**.
>
> ![Berguedà](images/bergueda.png)
```

## Load the Markdown into Anki
Use [inka2](https://github.com/sysid/inka2).