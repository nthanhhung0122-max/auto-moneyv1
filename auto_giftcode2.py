name: Auto Giftcode (Acc 2)

on:
  workflow_dispatch:
  schedule:
    - cron: '*/5 * * * *'

concurrency:
  group: giftcode-acc2
  cancel-in-progress: false

jobs:
  farm-giftcodes:
    runs-on: ubuntu-latest
    timeout-minutes: 340

    permissions:
      actions: write
      contents: read

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests telethon colorama beautifulsoup4

      - name: Chay Bot Giftcode Acc 2 (Tu dong chay lai sau 1 phut neu tat)
        env:
          PYTHONUNBUFFERED: "1"
          PYTHONIOENCODING: "utf-8"
        run: |
          while true; do
            python auto_giftcode2.py || true
            echo "--------------------------------------------------------"
            echo "Bot vua dung, cho 60 giay (1 phut) roi tu dong chay lai..."
            echo "--------------------------------------------------------"
            sleep 60
          done

      - name: Tu dong kich hoat lai workflow sau 1 phut neu bi tat
        if: always()
        run: |
          echo "Ca chay ket thuc! Cho 60 giay roi kich hoat ca moi..."
          sleep 60
          curl -X POST \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer ${{ secrets.GITHUB_TOKEN }}" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/${{ github.repository }}/actions/workflows/giftcode_acc2.yml/dispatches \
            -d '{"ref":"main"}' || true
