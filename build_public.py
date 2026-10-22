"""プロジェクトの地図（座標JSON）から、公開用のキーなし地図を作る。
自宅を外し、基準点を駅にする。使い方:
  python -I build_public.py <座標.json> <出力名> [基準の駅名]
"""
import json, os, subprocess, sys, tempfile
sys.stdout.reconfigure(encoding='utf-8')
SKILL = os.path.expanduser('~/.claude/skills/place-map/place_map.py')
src, name = sys.argv[1], sys.argv[2]
base = sys.argv[3] if len(sys.argv) > 3 else '鷺ノ宮駅'
here = os.path.dirname(os.path.abspath(__file__))
spec = json.load(open(src, encoding='utf-8'))
pts = [p for p in spec['points'] if '自宅' not in p['name']]
b = next(p for p in pts if p['name'] == base)
spec['home'] = {'name': base, 'lat': b['lat'], 'lon': b['lon']}
spec['points'] = [p for p in pts if p['name'] != base]
for p in spec['points']:
    for k in list(p):
        if isinstance(p[k], str):
            p[k] = p[k].replace('自宅まで直線約1km、歩いて帰る', '終点').replace('自宅', '家')
        if k in ('km', 'match', 'addr_hit'):
            p.pop(k)
spec['subtitle'] = spec.get('subtitle', '').split('。', 1)[-1].strip() or spec.get('subtitle', '')
tmp = os.path.join(tempfile.mkdtemp(), name + '.json')
json.dump(spec, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
out = os.path.join(here, 'maps')
subprocess.run([sys.executable, '-I', SKILL, tmp, '--out-dir', out, '--data-dir', out,
                '--name', name, '--engine', 'leaflet'], check=True)
os.remove(os.path.join(out, name + '_座標.json'))
