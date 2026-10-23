# travel-maps
旅行・日帰りの候補地マップ（公開用）。GitHub Pages: https://mrdog1.github.io/travel-maps/

- 地図は国土地理院タイル＋Leaflet（APIキーなし）
- `build_public.py` でプロジェクトの座標JSONから作る（自宅・家の近所は含めない。基準点は駅など）
- デプロイは GitHub Actions（`.github/workflows/deploy.yml`）。main に push すると Pages に出る
