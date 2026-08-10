import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "shopify-wine-list-import.csv"

products = []


def add(ptype, title, region, bottle_price):
    products.append(
        {
            "type": ptype,
            "title": title.strip(),
            "region": (region or "").strip(),
            "price": float(bottle_price),
        }
    )


# SPARKLING — bottle only
add("Sparkling", "NV Vouvray la Dilettante Brut", "Loire, FR", 51)
add("Sparkling", "NV Champagne Bertrand Delespierre Extra Brut", "FR", 79)

# ROSÉ
add("Rosé", "2023 Domaine Sainte Philomène Cuvée Philippine", "Provence, FR", 40)
add("Rosé", "2022 Domaine Ott Clos Mireille", "Provence, FR", 65)

# SWEET — menu lists 100ml only; use that as product price (no bottle shown)
add("Sweet", "2014 Castelnau de Suduiraut", "Sauternes, FR", 11.00)
add("Sweet", "2017 Gaillac Vendanges Tardives Domaine Rotier", "FR", 11.00)
add("Sweet", "2013 Tokaji Aszú 5 Puttonyos Dorgó", "Tokaji, HUNG", 15.00)

# FORTIFIED — 100ml only on menu
add("Fortified", "2021 Vinmouth Gros Manseng Vermouth", "", 9.50)
add("Fortified", "2023 Banyuls Domaine de Valcros", "FR", 8.00)
add("Fortified", "20 YO Graham's Tawny", "POR", 11.00)
add("Fortified", "1992 Rivesaltes Ambré Domaine de Rancy", "FR", 15.00)
add("Fortified", "2000 Dow's Vintage", "POR", 20.00)

# ARMAGNAC / COGNAC / EAU-DE-VIE — 50ml pour prices on menu (no bottle)
add("Armagnac", "NV Domaine d'Aurensan Carré des Fantômes", "", 13.50)
add("Armagnac", "1970 Dartigalongue Armagnac", "", 30)
add("Cognac", "Ragnaud Sabourin N 20 Reserve Speciale", "", 16.50)
add("Eau-de-Vie", "Goutte de Poire Williams Distillerie Cazottes", "", 14.00)

whites = [
    ("2022 Le Petit Fantet d'Hippolyte Ollieux Romanis", "Languedoc, FR", 32),
    ("2021 Baglio Antico Catarratto (Orange)", "Sicily, IT", 35),
    ("2023 Ebner-Ebenauer Poysdorf Grüner Veltliner", "Niederösterreich, AUSTRIA", 42),
    ("2021 Nosiola Vigneti delle Dolomiti Cesconi", "Trentino, IT", 44),
    ("2020 Trinity Hill 'Gimblett' Marsanne Viognier", "Hawke's Bay, NZ", 45),
    ("2021 Domaine Gauby Calcinaires", "Côtes Catalanes, FR", 45),
    ("2019 Dobogó Tokaji Furmint", "Tokaji, HUNG", 45),
    ("2022 Sancerre Roger Champault Clos du Roy", "Loire, FR", 46),
    ("2022 Albariño O Casal", "Galicia, SP", 46),
    ("2021 Trinity Hill 'Gimblett' Chardonnay", "Hawke's Bay, NZ", 48),
    ("2020 Savagnin Ouillé Chevassu", "Jura, FR", 49),
    ("2022 Tue Boeuf Brin de Chèvre Menu Pineau", "Loire, FR", 50),
    ("2023 Saumur l'Insolite Thierry Germain", "Loire, FR", 52),
    ("2021 Riesling Kientzheim Trapet", "Alsace, FR", 52),
    ("2022 Riesling 'Julius' Henschke", "Eden Valley, AUST", 56),
    ("2022 Chablis 1er Cru Vaillons Domaine du Chardonnay", "Burgundy, FR", 56),
    ("2022 Assyrtiko Vassaltis", "Santorini, GR", 59),
    ("2022 Saint Joseph François Merlin", "Rhône, FR", 61),
    ("2021 Katherine's Vineyard Chardonnay Cambria Estate", "Santa Barbara County, USA", 63),
    ("2022 Pouilly-Fuissé 1er Cru Les Crays Domaine Guerrin", "Burgundy, FR", 65),
    ("2022 Condrieu Stéphane Montez", "Rhône, FR", 72),
    ("2021 Meursault Bzikot", "Burgundy, FR", 97),
]
for title, region, price in whites:
    add("White Wine", title, region, price)

reds = [
    ("2022 Domaine Les Yeuses Syrah", "Languedoc, FR", 35),
    ("2020 Barbera Rossore Iuli", "Piemonte, IT", 39),
    ("2019 Chakana Ayni Malbec", "Mendoza, ARG", 46),
    ("2017 Rioja Gran Reserva Coto de Imaz", "Rioja, SP", 48),
    ("2015 Diane de Belgrave Haut-Médoc", "Bordeaux, FR", 49),
    ("2021 Gigondas Domaine Grand Romane", "Rhône, FR", 52),
    ("2022 Chénas Blemonts Domaine Thillardon", "Beaujolais, FR", 55),
    ("2013 Moulin à Vent Château des Jacques Clos du Grand Carquelin", "Beaujolais, FR", 56),
    ("2019 Pinot Noir Résonance Willamette Valley", "Oregon, USA", 59),
    ("2018 Valtellina Superiore Riserva Carteria Sandro Fay", "Lombardy, IT", 60),
    ("2018 Château des Graviers Margaux", "Bordeaux, FR", 62),
    ("2015 Ribeira Sacra Algueira Serradelo", "Galicia, SP", 62),
    ("2019 'GAM' Mitolo Shiraz", "McLaren Vale, AUST", 62),
    ("2011 Saumur-Champigny Les Rogelins Clotilde Legrand", "Loire, FR", 65),
    ("2017 Barolo 460 Cascina Bric", "Piemonte, IT", 66),
    ("2018 Château Le Gabachot Pomerol", "Bordeaux, FR", 69),
    ("2022 Pinot Noir Cuvée Cinéma Crystallum", "Hemel En Aarde, SA", 69),
    ("2012 Pastourelle de Clerc Milon Pauillac", "Bordeaux, FR", 71),
    ("2019 Vilafonte Serie M (Merlot/Malbec blend)", "Paarl, SA", 79),
    ("2019 Marsannay Au Champ Salomon Domaine Bart", "Burgundy, FR", 79),
    ("2017 Brunello di Montalcino Silvio Nardi", "Tuscany, IT", 85),
    ("2020 Côte Rôtie François Merlin", "Rhône, FR", 92),
    ("2021 Cabernet Sauvignon Pine Ridge", "Napa Valley, USA", 99),
]
for title, region, price in reds:
    add("Red Wine", title, region, price)

# Types with no bottle on the printed list — skip for bottle-only import
BOTTLE_TYPES = {"Sparkling", "Rosé", "White Wine", "Red Wine"}
bottle_products = [p for p in products if p["type"] in BOTTLE_TYPES]


def slugify(title):
    s = title.lower().replace("'", "").replace("'", "").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:70]


def country_tag(region):
    mapping = {
        "FR": "France",
        "IT": "Italy",
        "SP": "Spain",
        "POR": "Portugal",
        "HUNG": "Hungary",
        "NZ": "New Zealand",
        "AUST": "Australia",
        "AUSTRIA": "Austria",
        "USA": "USA",
        "GR": "Greece",
        "ARG": "Argentina",
        "SA": "South Africa",
    }
    tags = []
    if not region:
        return tags
    parts = [p.strip() for p in region.split(",")]
    if len(parts) >= 2:
        tags.append(parts[0])
        code = parts[-1].upper()
        tags.append(mapping.get(code, parts[-1]))
    else:
        code = parts[0].upper()
        tags.append(mapping.get(code, parts[0]))
    return tags


headers = [
    "Handle",
    "Title",
    "Body (HTML)",
    "Vendor",
    "Product Category",
    "Type",
    "Tags",
    "Published",
    "Option1 Name",
    "Option1 Value",
    "Variant SKU",
    "Variant Grams",
    "Variant Inventory Tracker",
    "Variant Inventory Qty",
    "Variant Inventory Policy",
    "Variant Fulfillment Service",
    "Variant Price",
    "Variant Compare At Price",
    "Variant Requires Shipping",
    "Variant Taxable",
    "Variant Barcode",
    "Image Src",
    "Image Position",
    "Image Alt Text",
    "Gift Card",
    "SEO Title",
    "SEO Description",
    "Status",
]

rows = []
seen = {}
for p in bottle_products:
    base = slugify(p["title"])
    handle = base
    n = 2
    while handle in seen:
        handle = f"{base}-{n}"
        n += 1
    seen[handle] = True

    tags = [p["type"], "Wine List", "Menu 07.08", "Bottle"]
    tags.extend(country_tag(p["region"]))
    m = re.match(r"^(NV|\d{4})", p["title"])
    if m:
        tags.append(m.group(1))

    body = ""
    if p["region"]:
        body += f"<p><strong>Origin:</strong> {p['region']}</p>"
    body += f"<p><strong>Type:</strong> {p['type']}</p>"
    body += "<p>Sold by the bottle.</p>"

    row = {h: "" for h in headers}
    row["Handle"] = handle
    row["Title"] = p["title"]
    row["Body (HTML)"] = body
    row["Vendor"] = "St Swithins Wine Shippers"
    row["Type"] = p["type"]
    row["Tags"] = ", ".join(tags)
    row["Published"] = "TRUE"
    row["Option1 Name"] = "Title"
    row["Option1 Value"] = "Default Title"
    row["Variant SKU"] = f"{handle}-bt"
    row["Variant Grams"] = "1250"
    row["Variant Inventory Policy"] = "deny"
    row["Variant Fulfillment Service"] = "manual"
    row["Variant Price"] = f"{p['price']:.2f}"
    row["Variant Requires Shipping"] = "TRUE"
    row["Variant Taxable"] = "TRUE"
    row["Gift Card"] = "FALSE"
    row["SEO Title"] = p["title"]
    row["SEO Description"] = f"{p['title']} — {p['region']}".strip(" —")
    row["Status"] = "active"
    rows.append(row)

with OUT.open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} bottle products -> {OUT}")
for key, count in Counter(p["type"] for p in bottle_products).items():
    print(f"  {key}: {count}")
skipped = [p for p in products if p["type"] not in BOTTLE_TYPES]
print(f"Skipped {len(skipped)} pour-only items (Sweet/Fortified/spirits — no bottle price on list)")
