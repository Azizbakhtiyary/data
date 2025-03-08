name: Update Pools Data

on:
  schedule:
    - cron: '*/30 * * * *'  # Запуск каждые 30 минут
  workflow_dispatch:  # Возможность запускать вручную

jobs:
  update_data:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Fetch latest pools data
        run: curl -s "https://yields.llama.fi/pools" -o pools.json

      - name: Run filtering script
        run: python filter_pools.py

      - name: Log filtered pools count
        run: cat filter_log.txt

      - name: Commit and push changes
        run: |
          git config --global user.name "github-actions"
          git config --global user.email "actions@github.com"
          git add pools.json filtered_pools.json filter_log.txt
          git commit -m "Auto-update pools and filtered pools" || exit 0
          git push

      - name: Send Telegram Notification
        if: always()
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id=${{ secrets.TELEGRAM_CHAT_ID }} \
            -d text="🚀 Обновление пулов завершено!%0A%0A✅ Фильтр: APY ≥ 100%, TVL ≥ $50K%0A📊 Количество пулов: $(cat filter_log.txt)" \
            -d parse_mode="Markdown"
