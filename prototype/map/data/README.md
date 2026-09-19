# Prototype map data

These files exist only for the thin map proof.

## world-land.geojson

Source repository: `nvkelso/natural-earth-vector`  
Path: `geojson/ne_110m_land.geojson`  
Git blob SHA: `04811d72fff2701ec67587e30ad8942675b511e3`

Used only as the neutral land outline/background.

## brazil-modern-proxy.geojson

Extracted from:

`geojson/ne_110m_admin_0_countries.geojson`

Source repository: `nvkelso/natural-earth-vector`  
Git blob SHA: `1e6ab74c7042f97013be69ceec798be8e1aff27d`

The feature with `ADM0_A3 = BRA` was retained and properties reduced for the prototype.

The geometry is explicitly classified as `modern_proxy`.

## slice.json

Historical assertion derived from the canonical v0.6.1 Brazil evidence row. P-level remains null/unassigned. The source URL is preserved exactly.
