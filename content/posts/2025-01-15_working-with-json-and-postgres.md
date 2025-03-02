---
title: Working with JSON and PostgreSQL
subtitle: Jason and the elephants
authors:
    - tszczurek
categories:
    - article
comments: true
date: 2025-02-27
description: "Store data in json format in PostgreSQL, consult it... and all this using INSEE french census data as an example. "
icon: simple/postgresql
image:
license: default
links:
  - Original version (French): https://geotribu.fr/articles/2025/2025-01-21_travailler-avec-JSON-et-PostgreSQL/
robots: index, follow
tags:
    - PostgreSQL
    - JSON
---

# Working with JSON in PostgreSQL

![logo JSON](https://cdn.geotribu.fr/img/logos-icones/programmation/json.png){: .img-thumbnail-left }

As part of a personal project, I wanted to store a large part of the INSEE's french census data in a PostgreSQL database with multi-millennial tables. The problem is that, within the same dataset, the fields can change over the years, which makes it impossible to create a fixed table structure. The solution? Use semi-structured data, i.e. store this data in JSON in a table field. This article is a summary of that experience.

!!! info "Unscheduled obsolescence"
    This work was carried out before the release of PostgreSQL 17, which adds important features for JSON with [`JSON_TABLE`](https://doc.postgresql.fr/17/functions-json.html#FUNCTIONS-SQLJSON-TABLE), so it won't be mentioned here.

Since we're going to be talking about JSON and semi-structured data, I feel obliged to start this article with a warning.

**The relational model is good, eat it up, and integrity constraints were invented for good reason.**

This article is not intended to be an invitation to go into YOLO mode on data management: “all you have to do is put everything in JSON” (like a vulgar dev who would put everything in MongoDB, as the bad tongues would say).

<!-- more -->
## JSON for beginners

For those of you unfamiliar with [JSON](https://www.json.org/json-fr.html) it's a text-based data representation format from JavaScript that works in part on a `key:value` system that can be seen as a sort of evolution of XML.

```json
{“key_1”: “value”, “key_2”: “value”, “key_3”: “value”}
```

No need for quotation marks for numbers:

```json
{“nb_mushrooms”: 42, “nb_tomatoes”: 31, “first_name”: “roger”}
```

Values can take two forms:

- either a single value, as in the example above,
- or an array, a list, enclosed in `[]`, both of which can be combined in a single JSON object.

```json
{“prenoms”: [“first_name”, “roger”, “fatima”], “nb_mushrooms”: 42}
```

What we call an object is everything between the `{}` used to declare it. To make things even more complex, we can nest objects and give you an example that's a little more meaningful than talking about tomatoes and mushrooms:

```json title="Example with JSON of superheroes" linenums="1"
{
  "squadName": "Super hero squad",
  "homeTown": "Metro City",
  "formed": 2016,
  "secretBase": "Super tower",
  "active": true,
  "members": [
    {
      "name": "Molecule Man",
      "age": 29,
      "secretIdentity": "Dan Jukes",
      "powers": [
        "Radiation resistance",
        "Turning tiny",
        "Radiation blast"
      ]
    },
    {
      "name": "Madame Uppercut",
      "age": 39,
      "secretIdentity": "Jane Wilson",
      "powers": [
        "Million tonne punch",
        "Damage resistance",
        "Superhuman reflexes"
      ]
    },
    {
      "name": "Eternal Flame",
      "age": 1000000,
      "secretIdentity": "Unknown",
      "powers": [
        "Immortality",
        "Heat Immunity",
        "Inferno",
        "Teleportation",
        "Interdimensional travel"
      ]
    }
  ]
}
```

An example from the [Mozilla](https://developer.mozilla.org/fr/docs/Learn/JavaScript/Objects/JSON) site, which will give you a better idea. You can also consult the [wikipedia](https://fr.wikipedia.org/wiki/JavaScript_Object_Notation) article or [the infamous specification site](https://www.json.org/json-en.html).

## PostgreSQL's json types

PostgreSQL is able to store data/objects in json format in fields that are assigned a dedicated type. There are two types, because otherwise it wouldn't be any fun.

- The `json` type is there for historical reasons, to allow databases that used this type in the past to function. It stores information in text form, which is not optimized for a computer. There is, however, an advantage to using it: it allows you to retrieve information on key order. If it's important for you to know that `name` is key 1 and `firstname` is key 2, without having to go through the key name again, then you'll need to use the `json` type.

- the `jsonb` type. The modern type. It stores information in binary form and offers a lott of functions in addition to those of the `json` type.

## Indexes

![icône index](https://cdn.geotribu.fr/img/logos-icones/divers/index_pointeur.webp){: .img-thumbnail-left }

It is possible to index a `json` / `jsonb` field on its **first-level** keys, and this is done with [`GIN`](https://www.postgresql.org/docs/current/gin.html) type indexes:

```sql
CREATE INDEX idx_tb_jsonfield ON tb USING gin (jsonfiled);
```

To index “deeper” values, you'll need to use functional indexes, indexes on functions:

```sql
CREATE INDEX idx_tb_jsonfield ON tb USING gin (jsonfield -> key_to_locate_values_to_be_index);
```

We'll explain this `->` later.

For the adventurous, there's a PostgreSQL extension called `btree_gin` that allows you to create multi-field indexes mixing classic and `json` fields. It's available natively when you install PostgreSQL, and won't require you to become a C/C++ developer⸱se to install it (hello parquet FDW ! How's it going over there?).

## Table creation

I'm not going to spam you with Data Definition Language (<https://en.wikipedia.org/wiki/Data_definition_language>), but you can find the complete database schema [here](https://github.com/thomas-szczurek/base_donnees_insee/tree/main/sql/creation_tables).

However, here's a brief diagram to help you understand the rest of the article:

![Database model diagram](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/postgresql_json/modele.png){: .img-center loading=lazy }

**Don't worry about the stacked tables on the right, they're partitions of the `donnees_communes` table. We won't go into them here, and they're only needed for the example*.

Starting from a schema named `insee`, we'll create two tables:

- the first will contain the list of available *bases*, the various census components ;
- the second will store the data.

To keep the focus on JSON, we'll spare ourselves 95% of the underlying model. So we won't be handling commune codes, etc. :

```sql title="Table creation Script" linenums="1"
BEGIN;
-- table listing the various Insee databases available

CREATE TABLE insee.bases (
pk_id int2 PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
nom text NOT NULL
);

-- table storing data by municipalities

CREATE TABLE insee.donnees_communes (
pk_id int4 PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
code_commune text NOT NULL CHECK length(code_commune) = 5, -- let's not forget the Corsicans who have municipalities codes in 2A and 2B, hence the text type
fk_base int2 NOT NULL,
annee int2 NOT NULL,
donnees jsonb NOT NULL,
UNIQUE (fk_base, annee, code_commune)
CONSTRAINT fk_donnees_bases FOREIGN KEY fk_base ON insee.bases(pk_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Index creation
-- A multi-field index is already automatically created on (fk_base, annee, code_commune) thanks to the UNIQUE clause in the table declaration.
CREATE INDEX idx_donnees_com_donnees ON insee.donnees_communes USING gin (donnees);
END;
```

The most fussy of you DBAs will have noticed this `CHECK`. “Why doesn't he use varchar(5)? It really doesn't make sense!” Quite simply, because this form allows you to use a text type with **really** arbitrary numbers of characters (the `text` type) unlike varchar(255), while being able to control the minimum and maximum number with the `CHECK` predicate (unlike varchar which only controls the maximum) as explained on the [Postgres wiki].(<https://wiki.postgresql.org/wiki/Don%27t_Do_This#Don.27t_use_varchar.28n.29_by_default>).

And we insert a few rows in our insee.bases table :

```sql title="SQL script for data insertion" linenums="1"
INSERT INTO insee.bases (nom) VALUES
('rp_population'),
('rp_menages'),
('rp_logement'),
('rp_diplomes'),
('rp_activite'),
('rp_emploi')
```

## Insertion de données et récupération

To pass text/SQL data to JSON-encoded data in the appropriate dedicated field, PostgreSQL has [*some* functions](https://www.postgresql.org/docs/current/functions-json.html). We're going to use the `jsonb_object()` function, which transforms a sql `array` in the form `key1, value1, key2, value2 ....` into a `jsonb` object with only one nesting level. Other functions are available for more complex objects (such as `jsonb_build_object()`).

### Simple example

We'll create a text string containing the contents of our json, whose values will be separated by commas `key1, value1, key2, value2`. This string will be passed to a `string_to_array()` function, transforming it into an `array` with `,` as separator to separate the elements of the text string into list elements, a character passed as the function's second parameter. This `array` will then be sent to the `jsonb_object()` function.

```sql
INSERT INTO insee.donnees_communes (code_commune, annee, fk_base, donnees) VALUES
(
  '99999',
  2024,
  1,
  jsonb_object(
    string_to_array('tomatoes,42,melons,12',',')
    )
)
```

This request will encode this json object in the `data` field:

```json
{
  "tomatoes": 42,
  "melons": 12
}
```

Now how do we get our number of melons for the municipalitie code 99999 in 2024? This is done using special operators:

- `jsonb_field -> 'key'` retrieves the value of a key while preserving its json type
- `jsonb_field ->> 'key'` does the same, transforming the value into a “classic” sql type

```sql
SELECT
  (donnees ->> 'melons')::int4 AS nb_melons
FROM insee.donnees_communes
WHERE
  donnees ? 'melons'
  AND code_commune = '99999'
  AND annee = 2024
```

You can see that I'm using the `?` operator, which is only valid for `jsonb` fields and not for simple `json` fields. This is because, when a json/jsonb field is queried, all the records in the table are returned, even those that don't contain the key. So if your table contains 100,000 records, but only 100 contain the key “melons”, not specifying this WHERE clause would return 100,000 rows, 99,900 of which would be `NULL`.`?` is a json operator used to ask the question “Is the key present at the first level of the json field for this record?”, and we'd only get our 100 records containing the key “melons”.

If you're still here, I assume you already know this. However, the form `(something)::(type)` is a PostgreSQL shortcut for making a `cast`, i.e. converting a value into another type. With `->>` the value is returned to us as text and we convert it into an integer.

### With nested JSON

Well, he's a nice guy, but his JSON is still JSON where everything is on the first level. Well, for my needs, that was enough. But I'm not going to run away from my responsibilities and we'll see how it goes with more complex JSON.  
I'll use the example from the previous section to make things more complex after this aside.

To inject complex json into a field, we have two solutions: nesting dedicated functions, or castering a text string. Let's imagine a “test” table, in a “test” schema, with a `jsonb` field named “donnees”.

```sql
INSERT INTO test.test (donnees) VALUES
(jsonb_object(
 'key1', 'value1',
 'key2', jsonb_array(
  'foo', 'bar', 'baz')
  )
 )
```

Cette insertion pourrait tout aussi bien s'écrire avec un cast d'une chaine de texte vers du jsonb. Attention, la syntaxe json doit être ici respectée :

```sql
INSERT INTO test.test (donnees) VALUES
('{"key1": "value1", "key2": ["foo", "bar", "baz"]}'::jsonb)
```

#### Data recovery

To retrieve a value, we use the `jsonb_path_query()` function, which has two parameters: `the name of the field` containing the json data, and the `json_path` to the value to be retrieved. Let's imagine we want to retrieve the second value in the list contained in “key2” :

```sql
SELECT
 jsonb_path_query(donnees, '$.cle2[1]')
FROM test.test
```

The `$` indicates the start of the returned json path. We follow this first symbol with a dot to move on to the next object. Then, by the next key name and so on up to the searched key, to which we paste a `[1]` for the 2ᵉ value in the list (values start at 0).
For more information on `json_path`, please refer to the [documentation](https://www.postgresql.org/docs/current/functions-json.html#FUNCTIONS-SQLJSON-PATH).

## Let's tackle the census

![logo INSEE](https://cdn.geotribu.fr/img/logos-icones/entreprises_association/INSEE.svg){: .img-thumbnail-left }

Well, now that we've tried to explain the concepts as best we can with simple examples, because we've got to start somewhere, let's try something a little more voluminous.

Let's retrieve the latest population data from the municipal census [in csv format from the Insee website](https://www.insee.fr/fr/information/8183122) (you'll want the bases for the main indicators, sorry page not available in english). For this example, we'll use the “Evolution et structure de la population” file. First, clean up the field names. Insee systematically indicates the year in its field names, which means that they change every year for the same indicator.

All field names begin with P or C, indicating *main survey* (raw answers to census questions) or *complementary survey* (cross-referencing of answers to establish an indicator). Fields from the main survey and those from the complementary survey must not be cross-referenced. This information should obviously be kept, but for personal reasons, I prefer to put it at the end of the name rather than at the beginning. In this way, we move from normalized fields such as `P18_POP` to a normalization of this type `POP_P`.

You'll find [here](https://github.com/thomas-szczurek/base_donnees_insee/blob/main/sql/import/correction_champs_insee.xlsx) a spreadsheet to take care of all this.

Before inserting the data into our table, we'll go through a temporary table to make the data accessible in Postgres. Using Postgresql's `COPY` would be tedious, as you'd have to specify the hundred or so fields contained in the census population section of the command. And I'm not ashamed to say that I've got a baobab in my hand at the thought. So we pull out this wonderful software called QGIS. We activate the Explorer and Explorer2 panels. We create a connection to the database with creation rights, and with a graceful flick of the wrist, we drag the file from the Explorer panel to the Postgres database in Explorer2. Let the magic happen.

Now, get ready for perhaps one of the weirdest INSERTs of your life (at least, it was for me!). Ugh. I realize that if I wanted to do this right, I'd also have to explain [CTE](https://www.postgresql.org/docs/current/queries-with.html). But I'll let you click on the link so as not to make it too long.

We're going to use the CTE to concatenate the name we want to give to our keys with the values contained in our temporary table in a string separated by `,`. We'll send it to a `string_to_array()` function and then to a `jsonb_object()` function. We'll also take the opportunity to clean up any tabs or carriage returns that might remain with a regular expression, using the `regex_replace()` function. (These characters are called ``t`,``n`and ``r`). The latter function takes 3 arguments: the source string, the searched-for `pattern` and the replacement text. The optional `g` flag* is added to replace all occurrences found.

Note that if your temporary table has a name other than “rp_population_import”, you'll need to modify the FROM clause in the CTE.

```sql title="The weirdest INSERT of your life (with a CTE)" linenums="1"
-- cte cte concatenating data with keys and cleaning up special characters.
WITH d AS (
  SELECT
 CODGEO,
 regexp_replace('pop_p,' || POP_P || ',
   pop_0_14_ans_p,' || POP0014_P || ',
   pop_15_29_ans_p,' || POP1529_P || ',
   pop_30_44_ans_p,' || POP3044_P || ',
   pop_45_59_ans_p,' || POP4559_P || ',
   pop_60_74_ans_p,' || POP6074_P || ',
   pop_75_89_ans_p,' || POP7589_P || ',
   pop_90_ans_plus_p,' || POP90P_P || ',
   hommes_p,' || POPH_P || ',
   hommes_0_14_ans_p,' || H0014_P || ',
   hommes_15_29_ans_p,' || H1529_P || ',
   hommes_30_44_ans_p,' || H3044_P || ',
   hommes_45_59_ans_p,' || H4559_P || ',
   hommes_60_74_ans_p,' || H6074_P || ',
   hommes_75_89_ans_p,' || H7589_P || ',
   hommes_90_ans_plus_p,' || H90P_P || ',
   hommes_0_19_ans_p,' || H0019_P || ',
   hommes_20_64_ans_p,' || H2064_P || ',
   hommes_65_ans_plus_p,' || H65P_P || ',
   femmes_p,' || POPF_P || ',
   femmes_0_14_ans_p,' || F0014_P || ',
   femmes_15_29_ans_p,' || F1529_P || ',
   femmes_30_44_ans_p,' || F3044_P || ',
   femmes_45_59_ans_p,' || F4559_P || ',
   femmes_60_74_ans_p,' || F6074_P || ',
   femmes_75_89_ans_p,' || F7589_P || ',
   femmes_90_ans_plus_p,' || F90P_P || ',
   femmes_0_19_ans_p,' || F0019_P || ',
   femmes_20_64_ans_p,' || F2064_P || ',
   femmes_65_ans_plus_p,' || F65P_P || ',
   pop_1an_ou_plus_localisee_1an_auparavant_p,' || POP01P_P || ',
   pop_1an_ou_plus_meme_logement_1an_auparavant_p,' || POP01P_IRAN1_P || ',
   pop_1an_ou_plus_meme_commune_1an_auparavant_p,' || POP01P_IRAN2_P || ',
   pop_1an_ou_plus_meme_departement_1an_auparavant_p,' || POP01P_IRAN3_P || ',
   pop_1an_ou_plus_meme_region_1an_auparavant_p,' || POP01P_IRAN4_P || ',
   pop_1an_ou_plus_autre_region_1an_auparavant_p,' || POP01P_IRAN5_P || ',
   pop_1an_ou_plus_un_dom_1an_auparavant_p,' || POP01P_IRAN6_P || ',
   pop_1an_ou_plus_hors_metropole_ou_dom_1an_auparavant_p,' || POP01P_IRAN7_P || ',
   pop_1_14ans_autre_logement_1an_auparavant_p,' || POP0114_IRAN2P_P || ',
   pop_1_14ans_meme_commune_1an_auparavant_p,' || POP0114_IRAN2_P || ',
   pop_1_14ans_autre_commune_1an_auparavant_p,' || POP0114_IRAN3P_P || ',
   pop_15_24ans_autre_logement_1an_auparavant_p,' || POP1524_IRAN2P_P || ',
   pop_15_24ans_meme_commune_1an_auparavant_p,' || POP1524_IRAN2_P || ',
   pop_15_24ans_autre_commune_1an_auparavant_p,' || POP1524_IRAN3P_P || ',
   pop_25_54ans_autre_logement_1an_auparavant_p,' || POP2554_IRAN2P_P || ',
   pop_25_54ans_meme_commune_1an_auparavant_p,' || POP2554_IRAN2_P || ',
   pop_25_54ans_autre_commune_1an_auparavant_p,' || POP2554_IRAN3P_P || ',
   pop_55_ou_plus_autre_logement_1an_auparavant_p,' || POP55P_IRAN2P_P || ',
   pop_55_ou_plus_meme_commune_1an_auparavant_p,' || POP55P_IRAN2_P || ',
   pop_55_ou_plus_autre_commune_1an_auparavant_p,' || POP55P_IRAN3P_P || ',
   pop_15_ans_plus_c,' || POP15P_C || ',
   agriculteurs_15_ans_plus_c,' || POP15P_CS1_C || ',
   artisants_commercants_chefs_entreprise_15_ans_plus_c,' || POP15P_CS2_C || ',
   cadres_prof_intel_sup_15_ans_plus_c,' || POP15P_CS3_C || ',
   professions_intermediaires_15_ans_plus_c,' || POP15P_CS4_C || ',
   employes_15_ans_plus_c,' || POP15P_CS5_C || ',
   ouvriers_15_ans_plus_c,' || POP15P_CS6_C || ',
   retraites_15_ans_plus_c,' || POP15P_CS7_C || ',
   autres_15_ans_plus_c,' || POP15P_CS8_C || ',
   hommes_15_ans_plus_c,' || H15P_C || ',
   h_agriculteurs_15_ans_plus_c,' || H15P_CS1_C || ',
   h_artisants_commercants_chefs_entreprise_15_ans_plus_c,' || H15P_CS2_C || ',
   h_cadres_prof_intel_sup_15_ans_plus_c,' || H15P_CS3_C || ',
   h_professions_intermediaires_15_ans_plus_c,' || H15P_CS4_C || ',
   h_employes_15_ans_plus_c,' || H15P_CS5_C || ',
   h_ouvriers_15_ans_plus_c,' || H15P_CS6_C || ',
   h_retraites_15_ans_plus_c,' || H15P_CS7_C || ',
   h_autres_15_ans_plus_c,' || H15P_CS8_C || ',
   femmes_15_ans_plus_c,' || F15P_C || ',
   f_agricultrices_15_ans_plus_c,' || F15P_CS1_C || ',
   f_artisanes_commercantes_cheffes_entreprise_15_ans_plus_c,' || F15P_CS2_C || ',
   f_cadres_prof_intel_sup_15_ans_plus_c,' || F15P_CS3_C || ',
   f_professions_intermediaires_15_ans_plus_c,' || F15P_CS4_C || ',
   f_employees_15_ans_plus_c,' || F15P_CS5_C || ',
   f_ouvrieres_15_ans_plus_c,' || F15P_CS6_C || ',
   f_retraitees_15_ans_plus_c,' || F15P_CS7_C || ',
   f_autres_15_ans_plus_c,' || F15P_CS8_C || ',
   population_15_24_ans_c,' || POP1524_C || ',
   pop_15_24_ans_agriculteurs_c,' || POP1524_CS1_C || ',
   pop_15_24_ans_artisants_commercants_chefs_entreprise_c,' || POP1524_CS2_C || ',
   pop_15_24_ans_cadres_prof_intel_sup_c,' || POP1524_CS3_C || ',
   pop_15_24_ans_professions_intermediaires_c,' || POP1524_CS4_C || ',
   pop_15_24_ans_employes_c,' || POP1524_CS5_C || ',
   pop_15_24_ans_ouvriers_c,' || POP1524_CS6_C || ',
   pop_15_24_ans_retraites_c,' || POP1524_CS7_C || ',
   pop_15_24_ans_autres_c,' || POP1524_CS8_C || ',
   population_25_54_ans_c,' || POP2554_C || ',
   pop_25_54_ans_agriculteurs_c,' || POP2554_CS1_C || ',
   pop_25_54_ans_artisants_commercants_chefs_entreprise_c,' || POP2554_CS2_C || ',
   pop_25_54_ans_cadres_prof_intel_sup_c,' || POP2554_CS3_C || ',
   pop_25_54_ans_professions_intermediaires_c,' || POP2554_CS4_C || ',
   pop_25_54_ans_employes_c,' || POP2554_CS5_C || ',
   pop_25_54_ans_ouvriers_c,' || POP2554_CS6_C || ',
   pop_25_54_ans_retraites_c,' || POP2554_CS7_C || ',
   pop_25_54_ans_autres_c,' || POP554_CS8_C || ',
   population_55_ans_et_plus_c,' || POP55P_C || ',
   pop_55_ans_et_plus_ans_agriculteurs_c,' || POP55P_CS1_C || ',
   pop_55_ans_et_plus_ans_artisants_commercants_chefs_entreprise_c,' || POP55P_CS2_C || ',
   pop_55_ans_et_plus_ans_cadres_prof_intel_sup_c,' || POP55P_CS3_C || ',
   pop_55_ans_et_plus_ans_professions_intermediaires_c,' || POP55P_CS4_C || ',
   pop_55_ans_et_plus_ans_employes_c,' || POP55P_CS5_C || ',
   pop_55_ans_et_plus_ans_ouvriers_c,' || POP55P_CS6_C || ',
   pop_55_ans_et_plus_ans_retraites_c,' || POP55P_CS7_C || ',
   pop_55_ans_et_plus_ans_autres_c,' || POP55P_CS8_C,
  E'[\t\n\r]','','g') AS data
  FROM insee.rp_population_import
 )

-- Conversion of text strings to json and insertion into the table.
INSERT INTO insee.donnees_communes("code_commune","annee","fk_base","donnees")
SELECT
    CODGEO,
    2021,
    1,
    jsonb_object(string_to_array(data::text,','))
FROM d
ORDER BY "CODGEO";
```

*Ouf.*

![Overview of the donnees_communes table after data insertion](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/postgresql_json/donnees_communes.png){: .img-center loading=lazy }

Be sure to group the inserts in this order: year/base/commune_code, to make it easier for PostgreSQL to read the data.

Now, imagine that, like the author of these lines, your fat, pudgy fingers stumble and slip on your keyboard while writing this query, that a typo slips in, and then it's drama. How do you change the name of a key already encoded in the table? Here's how:

```sql
CREATE TABLE example(id int PRIMARY KEY, champ jsonb);
INSERT INTO example VALUES
    (1, '{"nme": "test"}'),
    (2, '{"nme": "second test"}');

UPDATE example
SET champ = champ - 'nme' || jsonb_build_object('name', champ -> 'nme')
WHERE champ ? 'nme'
returning *;
```

`-` is an operator used to remove a key from a json object. For our UPDATE, we therefore remove our typo from the entire object. In addition, we concatenate everything else with the construction of a new object in which we correct the key name. We also assign the value of the key being deleted, which is still usable at UPDATE time, to the fields that originally contained it with `?`.

## Now what ? What do we do with this ?

So far, we've only worked with the population component for its latest version. Let's now imagine that we repeat the exercise for all 6 sections and over several years, bearing in mind that over time, certain fields may appear or disappear; changes in the levels of diplomas observed, for example. It would be interesting to retrieve a table showing the first and last year of presence of each key. Let's just say that during this work, we took the opportunity to update a “correspondance_clefs_champs” table listing each key present and its original INSEE name (at least, the one we had standardized).

```sql
CREATE MATERIALIZED VIEW insee.presence_clefs_annees AS
SELECT
 c.pk_id AS pk_id,
 c.clef_json AS clef_json,
 c.fk_base AS fk_base,
 a.premiere AS premiere_annee_presence,
 a.derniere AS derniere_annee_presence
FROM insee.correspondance_clefs_champs AS c,
 LATERAL (SELECT
     min(annee) AS premiere,
     max(annee) AS derniere
     FROM insee.donnees_communes WHERE fk_base = c.fk_base AND donnees ? c.clef_json) AS a
ORDER BY fk_base, clef_json;
```

![Overview of vm with the first and last year of key presence](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/postgresql_json/vm_presence_cles_annees.png){: .img-center loading=lazy }

The only difficulty here is the presence of [LATERAL](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-FROM). This “word” allows you to use a field from the main query in a subquery placed in a FROM clause. The elements of the subquery will then be evaluated atomically before being joined to the original table. Yes, it's not very easy to explain. Here, the WHERE of the subquery will query the `donnees` field of the “donnees_communes” table to see if it sees the clef_json (json key) being evaluated in the “correspondance_clefs_champs” table with alias “c”. If so, we take the minimum/maximum value of the year field and attach it to this line and this line only. Then evaluate the following clef_json ... (*evaluated atomically*)

Now we'd like to offer a product that's a little easier to use with all this. Excuse me in advance, I'll copy a 50-line query a second time.
The only table used here that we haven't created is a `zonages_administratifs` table containing municipalities codes in a `code_admin` field and a `fk_type` field containing the type of administrative zoning (1 for communes).

```sql title="Creation of the embellished materialized view" linenums="1"
CREATE MATERIALIZED VIEW insee.donnees_communes_olap AS
WITH
-- Municipalities codes selection
 codes_com AS (
  SELECT
   code_admin
  FROM insee.zonages_administratifs
  WHERE fk_type = 1
 ),
-- Key selections and unnest by year
 clefs AS (
  SELECT
   pk_id,
   generate_series(premiere_annee_presence, derniere_annee_presence,1) AS annee
  FROM insee.presence_clefs_annees
 ),
-- cross join keys + single year and communal codes
 tc AS (
 SELECT
  cc.code_admin AS code_com,
  cl.annee AS annee,
  cl.pk_id AS pk_id
 FROM codes_com AS cc
 CROSS JOIN clefs AS cl
 ),
-- Final selection with data recovery
 final AS (
 SELECT
  tc.code_com,
  tc.annee,
  co.fk_base,
  co.clef_json,
  CASE
   WHEN (d.donnees ->> clef_json) IN ('','null','s','nd') THEN NULL
   ELSE ((d.donnees ->> clef_json)::real)
  END AS valeur
 FROM tc
 JOIN
  insee.donnees_communes AS d ON (tc.code_com = d.code_commune AND tc.annee = d.annee)
 LEFT JOIN
  insee.presence_clefs_annees AS co ON tc.pk_id = co.pk_id
 ORDER BY tc.annee, co.fk_base, co.clef_json, tc.code_com
 )
SELECT * FROM final WHERE valeur IS NOT NULL;
```

![mv overview with “olap” organized data](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/postgresql_json/vm_donnees_olap.png){: .img-center loading=lazy }

Please note that creating or refreshing this materialized view may take some time if you've stored a lot of data (1 hour in my case for the 6 sections from 2015 to 2021).

Finally, in the spirit of living with the times and not like an old cave bear, we're going to convert this materialized view into a [parquet file](<https://parquet.apache.org/>).
And for that, we're going to use GDAL, which is truly incredible.

```sh title="View export in parquet format"
ogr2ogr -of parquet donnees_insee.parquet PG:"dbname='insee' schema='insee' tables='donnees_communes_olap' user='user_name' password='your_password'"
```

And then you can put the file on a cloud space, like [here](https://donnees-insee.s3.fr-par.scw.cloud/donnees_insee_olap.parquet)! You can then get out your best Linkedin publication generator, which will put lots of cute emojis, and show off on social networks (imagine that 90% of Linkedin content has to be made with these things, which are able to generate publications explaining that one of the few advantages of shape over geopackage is that it's a multi-file format, all in a very confident tone).

<!-- geotribu:authors-block -->

{% include "licenses/cc4_by-nc-sa.md" %}
