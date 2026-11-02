# travel-maps
旅行・日帰りの候補地マップ（公開用）。GitHub Pages: https://mrdog1.github.io/travel-maps/

- 地図は国土地理院タイル＋Leaflet（APIキーなし）
- `build_public.py` でプロジェクトの座標JSONから作る（自宅・家の近所は含めない。基準点は駅など）
- デプロイは GitHub Actions（`.github/workflows/deploy.yml`）。main に push すると Pages に出る

## 地図を足す手順
1. `python -I 公開/build_public.py <座標.json> <英字名> "<基準の駅・門>"` → `公開/maps/` にキーなし・自宅なしの地図ができる
2. `公開/index.html` に1行足す
3. APIキーと自宅の住所・座標が入っていないか grep する（検索する文字列は ../CLAUDE.md）
4. commit・push
