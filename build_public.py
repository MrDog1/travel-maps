"""プロジェクトの地図（座標JSON）から、公開用の地図を作る。
自宅と家の近所（中村南）を外し、基準点を駅などにする。使い方:
  python -I build_public.py <座標.json> <出力名> [基準の名前] [緯度,経度] [--google]

- 基準の名前が spec の points に無いときは「緯度,経度」を付ける（例：光が丘駅 35.7585,139.62889）
- --google：Google Maps 版を作る。キーは入れず、プレースホルダー __GOOGLE_MAPS_API_KEY__ を埋める。
  本物のキーは GitHub Actions（.github/workflows/deploy.yml）がデプロイ時に Secrets から差し込む。
- --google なし：これまでどおりキーなしの Leaflet 版。
"""
import json, os, subprocess, sys, tempfile
sys.stdout.reconfigure(encoding='utf-8')
SKILL = os.path.expanduser('~/.claude/skills/place-map/place_map.py')
PLACEHOLDER = '__GOOGLE_MAPS_API_KEY__'
args = [a for a in sys.argv[1:] if a != '--google']
google = '--google' in sys.argv
src, name = args[0], args[1]
base = args[2] if len(args) > 2 else '鷺ノ宮駅'
here = os.path.dirname(os.path.abspath(__file__))
spec = json.load(open(src, encoding='utf-8'))
pts = [p for p in spec['points'] if '自宅' not in p['name'] and '中村南' not in p.get('addr', '')]  # 家の近所の店も出さない
if len(args) > 3:
    lat, lon = (float(v) for v in args[3].split(','))
else:
    b = next(p for p in pts if p['name'] == base)
    lat, lon = b['lat'], b['lon']
spec['home'] = {'name': base, 'lat': lat, 'lon': lon}
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
env = dict(os.environ)
if google:
    env['GOOGLE_MAPS_API_KEY'] = PLACEHOLDER  # 本物のキーを読ませない
subprocess.run([sys.executable, '-I', SKILL, tmp, '--out-dir', out, '--data-dir', out,
                '--name', name, '--engine', 'google' if google else 'leaflet'], check=True, env=env)
os.remove(os.path.join(out, name + '_座標.json'))
