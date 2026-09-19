-- Migration 0011: generic external/network participation claims beyond voyage-specific relations.
-- This keeps participation in enslavement/trade networks separate from territorial practice intensity.

BEGIN;

INSERT INTO atlas.claim_kind(code, label, definition)
VALUES ('external_participation', 'External / network participation',
        'Participation in enslavement, slave trading, captive movement, finance, markets or related networks that must remain analytically separate from territorial practice')
ON CONFLICT (code) DO NOTHING;

CREATE TABLE atlas.participation_type (
    code text PRIMARY KEY,
    label text NOT NULL,
    definition text,
    active boolean NOT NULL DEFAULT true
);

INSERT INTO atlas.participation_type(code,label,definition) VALUES
('slave_trade_network','Slave-trade network participation','Participation in a slave-trading or enslavement network without automatically implying territorial prevalence'),
('captive_export','Captive / enslaved-person export','Export or outward movement of captives/enslaved persons'),
('captive_import','Captive / enslaved-person import','Import or inward movement of captives/enslaved persons'),
('trade_route','Trade / transport route participation','Participation as a route or corridor in movement/trade'),
('market','Market participation','Participation through a documented market or exchange point'),
('commercial_finance','Commercial / finance participation','Participation through finance, insurance, credit or investment outside a specific voyage relation'),
('state_institutional_participation','State / institutional participation','Participation by a state or institution in an external enslavement/trade network'),
('other','Other external participation','Other evidenced external/network participation requiring explicit description');

CREATE TABLE atlas.external_participation_claim (
    claim_id uuid PRIMARY KEY REFERENCES atlas.claim(claim_id) ON DELETE CASCADE,
    spatial_entity_id uuid REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    actor_id uuid REFERENCES atlas.actor(actor_id) ON DELETE RESTRICT,
    participation_type_code text NOT NULL REFERENCES atlas.participation_type(code),
    role_text text,
    notes text,
    CONSTRAINT external_participation_has_subject CHECK (
        spatial_entity_id IS NOT NULL OR actor_id IS NOT NULL
    )
);

CREATE INDEX external_participation_spatial_idx
    ON atlas.external_participation_claim(spatial_entity_id);
CREATE INDEX external_participation_actor_idx
    ON atlas.external_participation_claim(actor_id);
CREATE INDEX external_participation_type_idx
    ON atlas.external_participation_claim(participation_type_code);

CREATE OR REPLACE VIEW publish.external_participation_claim AS
SELECT c.*, e.spatial_entity_id, e.actor_id, e.participation_type_code,
       e.role_text, e.notes AS subtype_notes
FROM publish.claim c
JOIN atlas.external_participation_claim e USING (claim_id);

COMMIT;
