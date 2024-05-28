CREATE EXTENSION IF NOT EXISTS postgis;

CREATE SCHEMA IF NOT EXISTS app;

CREATE TABLE IF NOT EXISTS app.countries (
    "country_id" SERIAL PRIMARY KEY,
    "country_name" VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS app.grapes (
    "grape_code" SERIAL PRIMARY KEY,
    "grape" VARCHAR(100),
    "sinonimi" TEXT
);

CREATE TABLE IF NOT EXISTS app.grapes_descriptions (
    "grape_code" SERIAL PRIMARY KEY,
    "description" VARCHAR(100),
    FOREIGN KEY ("grape_code") REFERENCES app.grapes ("grape_code") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS app.clones (
    "clone_code" SERIAL PRIMARY KEY,
    "clone_name" VARCHAR(100),
    "approvation_date" DATE,
    "costitutore" VARCHAR(100),
    "annotazioni" TEXT,
    "gazzetta_ufficiale" VARCHAR(100),
    "data_gu" DATE,
    "grape_code" INT REFERENCES app.grapes("grape_code")
);

CREATE TABLE IF NOT EXISTS app.regions (
    "region_id" SERIAL PRIMARY KEY,
    "region_name" VARCHAR(100),
    "description" Text,
    "geometry" GEOMETRY(Geometry,4326),
    "country_id" SERIAL,
    FOREIGN KEY ("country_id") REFERENCES app.countries ("country_id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS app.wine_regions (
    "wine_region_id" SERIAL PRIMARY KEY,
    "wine_region_name" VARCHAR(100),
    "wine_region_type" VARCHAR(100),
    "description" TEXT,
    "geometry" GEOMETRY(Geometry,4326),
    "region_id" SERIAL,
    FOREIGN KEY ("region_id") REFERENCES app.regions ("region_id") ON DELETE CASCADE
);

COPY app.grapes ("grape_code","grape","sinonimi") FROM '/setup_data/grapes.csv' WITH (FORMAT csv, HEADER true);
COPY app.clones ("clone_code","clone_name","approvation_date","costitutore","annotazioni","gazzetta_ufficiale","data_gu","grape_code") FROM '/setup_data/clones.csv' WITH (FORMAT csv, HEADER true);
COPY app.countries FROM '/setup_data/countries.csv' WITH (FORMAT csv, HEADER true);
COPY app.regions FROM '/setup_data/contours.csv' WITH (FORMAT csv, HEADER true);


CREATE TABLE IF NOT EXISTS app.wines (
    "wine_id" SERIAL PRIMARY KEY,
    "nome" VARCHAR(100),
    "produttore" VARCHAR(100),
    "annata" INTEGER,
    "alchol" NUMERIC(5,2),
    "v_colore" VARCHAR(50),
    "v_riflesso" VARCHAR(50),
    "v_densita" VARCHAR(50),
    "v_limpidezza" VARCHAR(50),
    "v_vivacità" VARCHAR(50),
    "v_perlage" VARCHAR(50),
    "o_fruttato" BOOLEAN,
    "o_floreale" BOOLEAN,
    "o_vegetale" BOOLEAN,
    "o_minerale" BOOLEAN,
    "o_erbe_aromatiche" BOOLEAN,
    "o_speziato" BOOLEAN,
    "o_tostato" BOOLEAN,
    "o_balsamico" BOOLEAN,
    "o_etereo" BOOLEAN,
    "o_note" TEXT,
    "o_complessita" INTEGER,
    "o_qualita" INTEGER,
    "g_zucchero" VARCHAR(50),
    "g_alcol" VARCHAR(50),
    "g_acido" VARCHAR(50),
    "g_tannino" VARCHAR(50),
    "g_equilibrio" INTEGER,
    "g_persistenza" INTEGER,
    "g_sapido" VARCHAR(50),
    "g_chiusura" VARCHAR(50),
    "g_qualita" INTEGER,
    "g_dimensione" INTEGER,
    "prospettive_di_consumo" VARCHAR(50),
    "punteggio" INTEGER,
    "region_id" SERIAL,
    "wine_region_id" INTEGER NULL,
    FOREIGN KEY ("region_id") REFERENCES app.regions ("region_id") ON DELETE NO ACTION,
    FOREIGN KEY ("wine_region_id") REFERENCES app.wine_regions ("wine_region_id") ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS app.grapes_wines (
    "grape_code" SERIAL,
    "wine_id" SERIAL,
    FOREIGN KEY ("grape_code") REFERENCES app.grapes ("grape_code") ON DELETE CASCADE,
    FOREIGN KEY ("wine_id") REFERENCES app.wines ("wine_id") ON DELETE CASCADE
);

CREATE OR REPLACE VIEW app.wine_region_summary AS
SELECT 
    wr.wine_region_id,
    wr.wine_region_name,
    COUNT(w.wine_id) AS wine_count,
    bst.best_wine,
    bst.best_produttore,
    bst.best_punteggio,
    ROUND(AVG(w.punteggio), 1) AS avg_punteggio 
FROM 
    app.wine_regions wr
LEFT JOIN 
    app.wines w ON wr.wine_region_id = w.wine_region_id
LEFT JOIN 
    app.grapes_wines gw ON w.wine_id = gw.wine_id
LEFT JOIN 
    (
        SELECT 
            w.wine_region_id,
            w.nome AS best_wine,
            w.produttore AS best_produttore,
            w.punteggio AS best_punteggio
        FROM 
            app.wines w 
        JOIN 
            (
                SELECT 
                    wine_region_id,
                    MAX(punteggio) AS max_punteggio
                FROM 
                    app.wines
                GROUP BY 
                    wine_region_id
            ) subquery ON w.wine_region_id = subquery.wine_region_id AND w.punteggio = subquery.max_punteggio
    )  bst ON wr.wine_region_id = bst.wine_region_id   
GROUP BY 
    wr.wine_region_id, wr.wine_region_name, bst.best_wine, bst.best_produttore, bst.best_punteggio
ORDER BY 
    wr.wine_region_id;


CREATE OR REPLACE VIEW app.grape_wine_region_summary AS
SELECT 
    gw.grape_code,
    gr.grape,
    wr.wine_region_name AS wine_region,
    r.region_name AS region,
    w.nome,
    w.produttore,
    w.annata,
    w.punteggio
FROM 
    app.grapes_wines gw
JOIN 
    app.grapes gr ON gw.grape_code = gr.grape_code
JOIN 
    app.wines w ON gw.wine_id = w.wine_id
JOIN 
    app.wine_regions wr ON w.wine_region_id = wr.wine_region_id
JOIN 
    app.regions r ON wr.region_id = r.region_id;