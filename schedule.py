# schedule.py
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCHEDULE_FILE = Path(__file__).with_name("schedule.json")
JST = timezone(timedelta(hours=9))


def load_schedule(path):
    """schedule.json を読み込んで予定のリストを返す。"""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def filter_by_date(events, date_str):
    """指定した日(YYYY-MM-DD)の予定だけを、開始時刻順で返す。"""
    day_events = [e for e in events if e["start"].startswith(date_str)]
    return sorted(day_events, key=lambda e: e["start"])


def format_event(event):
    """予定1件を「09:00-18:00 タイトル @場所」の形の文字列にする。"""
    start = event["start"][11:16]
    end = event["end"][11:16]
    location = event.get("location") or "（場所なし）"
    return f"{start}-{end} {event['title']} @{location}"


def main():
    if len(sys.argv) >= 2:
        date_str = sys.argv[1]
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("日付は 2026-10-02 のような形式で指定してください。")
            return
    else:
        date_str = datetime.now(JST).strftime("%Y-%m-%d")

    try:
        events = load_schedule(SCHEDULE_FILE)
    except FileNotFoundError:
        print(f"schedule.json が見つかりません。schedule.py と同じフォルダに置いてください。({SCHEDULE_FILE})")
        return
    except json.JSONDecodeError as e:
        print(f"schedule.json の形式が正しくありません: {e}")
        return

    day_events = filter_by_date(events, date_str)
    print(f"{date_str} の予定 {len(day_events)} 件")
    for event in day_events:
        print(format_event(event))


if __name__ == "__main__":
 main()