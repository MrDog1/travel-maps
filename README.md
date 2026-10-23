# travel-maps
旅行・日帰りの候補地マップ（公開用）。GitHub Pages: https://mrdog1.github.io/travel-maps/

- `build_public.py` でプロジェクトの座標JSONから作る（自宅・家の近所は含めない。基準点は駅など）
- 地図は2種類
  - Leaflet 版（国土地理院タイル、APIキーなし）：`python -I build_public.py <座標.json> <名前> "<基準>"`
  - Google Maps 版：`--google` を付ける。HTMLにはキーの代わりに `__GOOGLE_MAPS_API_KEY__` が入る
- デプロイは GitHub Actions（`.github/workflows/deploy.yml`）。main に push すると、Secrets の `GOOGLE_MAPS_API_KEY` をプレースホルダーに差し込んで Pages に出す。**リポジトリにはキーを入れない**
