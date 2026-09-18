from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
DOC=yaml.safe_load((ROOT/'schema/controls.yaml').read_text(encoding='utf-8'))
TESTS=yaml.safe_load((ROOT/'schema/tests.yaml').read_text(encoding='utf-8'))

def test_domain_count(): assert len(DOC['domains']) == 10

def test_control_range(): assert 40 <= len(DOC['controls']) <= 60

def test_unique_control_ids():
    ids=[c['id'] for c in DOC['controls']]; assert len(ids)==len(set(ids))

def test_all_control_tests_exist():
    tids={t['id'] for t in TESTS['tests']}
    assert all(tid in tids for c in DOC['controls'] for tid in c['adversarial_tests'])

def test_critical_controls_target_high_assurance():
    assert all(c['target_assurance']=='YAL-4' for c in DOC['controls'] if c['severity']=='critical')

def test_test_count_v05():
    assert len(TESTS['tests']) >= 58

def test_symmetric_control_test_links():
    cmap={c['id']:set(c['adversarial_tests']) for c in DOC['controls']}
    for t in TESTS['tests']:
        for cid in t['controls']:
            assert t['id'] in cmap[cid]

def test_brand_contact_metadata():
    m=DOC['metadata']
    assert m['website']=='https://yofunesec.com/'
    assert m['contact']=='contact@yofunesec.com'
    assert 'Chengdu Yofune Ariake Technology Co., Ltd.' in m['publisher']
