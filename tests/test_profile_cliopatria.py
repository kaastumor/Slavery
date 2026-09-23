import io, json, zipfile
from tools.profile_cliopatria import git_blob_sha1, load_features, profile

def fixture_bytes():
    obj={'type':'FeatureCollection','features':[
      {'type':'Feature','properties':{'Name':'A','Type':'POLITY','FromYear':-10,'ToYear':-1,'Extra':'x'},'geometry':{'type':'Polygon','coordinates':[]}},
      {'type':'Feature','properties':{'Name':'B','Type':'RELATION','FromYear':-2,'ToYear':3},'geometry':{'type':'MultiPolygon','coordinates':[]}},
      {'type':'Feature','properties':{'Name':'Composite','Type':'POLITY, RELATION','FromYear':4,'ToYear':2},'geometry':None}]}
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w') as z:
        z.writestr('cliopatria.geojson',json.dumps(obj))
        z.writestr('__MACOSX/._cliopatria.geojson','finder metadata')
    return buf.getvalue()

def test_profile_preserves_source_semantics():
    data=fixture_bytes(); features=load_features(data); p=profile(features)
    assert p['feature_count']==3
    assert p['type_counts']=={'POLITY':1,'POLITY, RELATION':1,'RELATION':1}
    assert p['source_native_years']['minimum']==-10
    assert p['source_native_years']['maximum']==3
    assert p['source_native_years']['rows_crossing_numeric_zero']==1
    assert p['source_native_years']['invalid_from_to_ranges']==1
    assert p['property_presence_counts']['Extra']==1

def test_git_blob_identity_is_content_sensitive():
    a=fixture_bytes(); assert git_blob_sha1(a)!=git_blob_sha1(a+b'x')
