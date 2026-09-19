-- Migration 0002: controlled vocabularies that are expected to evolve.
-- These are tables rather than PostgreSQL enums so historical ontology can grow without type replacement.

BEGIN;

CREATE TABLE atlas.actor_type (
    code text PRIMARY KEY,
    label text NOT NULL,
    definition text,
    active boolean NOT NULL DEFAULT true
);

CREATE TABLE atlas.spatial_entity_type (
    code text PRIMARY KEY,
    label text NOT NULL,
    definition text,
    active boolean NOT NULL DEFAULT true
);

CREATE TABLE atlas.claim_kind (
    code text PRIMARY KEY,
    label text NOT NULL,
    definition text,
    active boolean NOT NULL DEFAULT true
);

CREATE TABLE atlas.coverage_state (
    code text PRIMARY KEY,
    label text NOT NULL,
    definition text,
    active boolean NOT NULL DEFAULT true
);

CREATE TABLE atlas.practice_type (
    code text PRIMARY KEY,
    label text NOT NULL,
    definition text NOT NULL,
    parent_code text REFERENCES atlas.practice_type(code),
    active boolean NOT NULL DEFAULT true
);

CREATE TABLE atlas.actor_attribute_type (
    code text PRIMARY KEY,
    label text NOT NULL,
    definition text,
    active boolean NOT NULL DEFAULT true
);

CREATE TABLE atlas.spatial_relation_type (
    code text PRIMARY KEY,
    label text NOT NULL,
    definition text,
    active boolean NOT NULL DEFAULT true
);

CREATE TABLE atlas.voyage_stop_role (
    code text PRIMARY KEY,
    label text NOT NULL,
    definition text,
    active boolean NOT NULL DEFAULT true
);

CREATE TABLE atlas.finance_role (
    code text PRIMARY KEY,
    label text NOT NULL,
    definition text,
    active boolean NOT NULL DEFAULT true
);

INSERT INTO atlas.actor_type(code,label,definition) VALUES
('person','Person','Individual human actor'),
('organization','Organization','Organization not better described by another active subtype'),
('partnership','Partnership / firm','Partnership or merchant firm'),
('company','Company','Company or chartered corporate entity'),
('state_institution','State institution','Governmental or state-linked institution'),
('other','Other','Other evidenced actor type');

INSERT INTO atlas.spatial_entity_type(code,label,definition) VALUES
('polity','Polity','Historical political or social unit'),
('province','Province / subnational unit','Historical subnational unit'),
('region','Region','Named historical or analytical region'),
('city','City / settlement','City, town or settlement'),
('port','Port','Port or port-place'),
('site','Site','Archaeological or other bounded site'),
('estate','Estate / plantation','Estate, plantation or comparable bounded property'),
('other','Other','Other named or bounded spatial unit');

INSERT INTO atlas.claim_kind(code,label,definition) VALUES
('territorial_practice','Territorial practice','Practice physically evidenced in a spatial entity'),
('legal_event','Legal event','Legal or state event/regime claim'),
('actor_attribute','Actor attribute','Time-bounded attribute or identity claim about an actor'),
('voyage_owner','Voyage ownership','Ownership/co-ownership or documented missing-owner status for a voyage'),
('voyage_finance','Voyage finance','Finance, insurance, credit or investment relation for a voyage'),
('voyage_stop','Voyage stop','Origin, embarkation, landing, call or other voyage-place relation'),
('spatial_relation','Spatial relation','Time-bounded relationship between spatial entities'),
('other','Other','Other claim type not yet specialized');

INSERT INTO atlas.coverage_state(code,label,definition) VALUES
('not_researched','Not researched','Not yet adequately researched'),
('source_identified','Source identified','Relevant sources identified but not yet fully reviewed'),
('reviewed','Reviewed','Evidence reviewed'),
('classified','Classified','Evidence reviewed and classified'),
('disputed','Disputed','Evidence exists but interpretation/classification remains disputed'),
('researched_inconclusive','Researched inconclusive','Target was actively reviewed but evidence does not justify a defensible classification');

INSERT INTO atlas.practice_type(code,label,definition) VALUES
('slavery_enslavement','Slavery / enslavement','Slavery or enslavement where supported by the evidence'),
('chattel_property_slavery','Chattel / property slavery','Property/chattel status where specifically evidenced'),
('hereditary_slavery','Hereditary slavery','Status transmitted hereditarily where evidenced'),
('debt_bondage','Debt bondage / debt servitude','Coercive dependency tied to debt'),
('forced_labour','Forced labour','Forced or compulsory labour not automatically classified as slavery'),
('state_forced_labour','State forced labour','Forced labour imposed or administered by state institutions'),
('penal_labour','Penal labour','Coerced labour tied to penal institutions or sentences'),
('corvee_compulsory_public_labour','Corvée / compulsory public labour','Compulsory public labour'),
('serfdom_tied_dependency','Serfdom / tied dependency','Tied dependency or serfdom'),
('domestic_servitude','Domestic servitude','Domestic servitude or household unfreedom'),
('military_slavery','Military slavery','Military slavery or slave-soldier institution'),
('sexual_slavery','Sexual slavery','Sexual slavery where specifically evidenced'),
('captive_taking_incorporation','Captive-taking / captive incorporation','Captivity or incorporation that must not automatically be equated with slavery'),
('slave_trade_sale_purchase','Slave trading / sale / purchase','Trading, sale or purchase of enslaved persons'),
('trafficking','Trafficking','Trafficking where historically and analytically appropriate'),
('other_servile_dependency','Other slavery-like / servile dependency','Other coerced or servile dependency requiring explicit definition');

INSERT INTO atlas.actor_attribute_type(code,label,definition) VALUES
('identity','Identity','Identity or normalization claim'),
('nationality_political_identity','Nationality / political identity','Independently evidenced nationality or political identity'),
('residence','Residence','Place of residence for a bounded period'),
('business_base','Business base','Commercial operating base'),
('corporate_jurisdiction','Corporate jurisdiction','Jurisdiction or political context of an organization'),
('political_legal_affiliation','Political / legal affiliation','Time-bounded political or legal affiliation'),
('commercial_role','Commercial role','General commercial role not represented by a more specific relationship'),
('other','Other','Other actor attribute');

INSERT INTO atlas.spatial_relation_type(code,label,definition) VALUES
('within','Within','Subject is geographically within object'),
('controlled_by','Controlled by','Subject is controlled by object for the stated interval'),
('jurisdiction_of','Jurisdiction of','Subject lies within the jurisdiction of object'),
('part_of','Part of','Subject is part of object'),
('other','Other','Other explicit spatial relationship');

INSERT INTO atlas.voyage_stop_role(code,label,definition) VALUES
('origin','Origin','Voyage origin / home port'),
('embarkation','Embarkation','Embarkation/purchase location'),
('landing','Landing','Disembarkation/landing location'),
('call','Call','Intermediate call'),
('registration','Registration','Vessel registration place'),
('construction','Construction','Vessel construction place'),
('other','Other','Other voyage-place relation');

INSERT INTO atlas.finance_role(code,label,definition) VALUES
('financier','Financier','Provides finance'),
('insurer','Insurer','Provides insurance'),
('lender','Lender','Provides credit or loan'),
('investor','Investor','Provides investment'),
('shareholder','Shareholder','Shareholding relationship where evidenced'),
('other','Other','Other finance relationship');

COMMIT;
