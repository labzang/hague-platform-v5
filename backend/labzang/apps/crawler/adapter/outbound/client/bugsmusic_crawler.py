"""
벅스 차트 크롤링 아웃바운드 어댑터 (CrawlerPort 구현).
- 외부 HTTP 호출만 수행. DB/영속성 없음.
"""

import re
from typing import List
from urllib.parse import urljoin

import requests  # type: ignore[import-untyped]
from bs4 import BeautifulSoup  # type: ignore[import-untyped]

from labzang.apps.crawler.application.ports.output import CrawlerPort


class BugsmusicCrawler(CrawlerPort):
    """벅스뮤직 실시간 차트 크롤링 구현."""

    _url = "https://music.bugs.co.kr/chart/track/realtime/total?wl_ref=M_contents_03_01"
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    def fetch_chart(self) -> List[dict]:
        response = requests.get(self._url, headers=self._headers, timeout=10)
        response.raise_for_status()
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        chart_table = soup.find("table", class_="list trackList byChart")
        if not chart_table:
            return []

        songs: List[dict] = []
        tbody = chart_table.find("tbody")
        rows = tbody.find_all("tr") if tbody else chart_table.find_all("tr")[1:]

        for idx, row in enumerate(rows, 1):
            song_data = self._parse_row(row, idx)
            if not song_data:
                continue
            if song_data.get("title") and song_data["title"] != "제목 없음":
                songs.append(song_data)
        return songs

    def _parse_row(self, row, idx: int) -> dict | None:
        """한 행 파싱. 파싱 불가 시 None 반환(방어적 처리)."""
        if row is None:
            return None
        song_data: dict = {}

        rank_cell = row.find("td", class_="ranking")
        if rank_cell:
            rank_text = rank_cell.get_text(strip=True) or ""
            rank_match = re.search(r"\d+", rank_text)
            song_data["rank"] = int(rank_match.group()) if rank_match else idx
        else:
            song_data["rank"] = idx

        title_cell = row.find("p", class_="title")
        if title_cell:
            title_link = title_cell.find("a")
            song_data["title"] = (
                (title_link.get_text(strip=True) if title_link else "")
                or title_cell.get_text(strip=True)
                or "제목 없음"
            )
        else:
            title_td = row.find("td", class_="left")
            if title_td:
                title_link = title_td.find("a")
                song_data["title"] = (
                    title_link.get_text(strip=True) if title_link else "제목 없음"
                )
            else:
                song_data["title"] = "제목 없음"

        artist_cell = row.find("p", class_="artist")
        if artist_cell:
            artist_links = artist_cell.find_all("a")
            if artist_links:
                artists = [
                    (link.get_text(strip=True) or "").strip() for link in artist_links
                ]
                song_data["artist"] = ", ".join(artists) or "아티스트 없음"
            else:
                song_data["artist"] = (
                    artist_cell.get_text(strip=True) or "아티스트 없음"
                )
        else:
            song_data["artist"] = "아티스트 없음"

        album_cell = row.find("p", class_="album")
        if album_cell:
            album_link = album_cell.find("a")
            song_data["album"] = (
                (album_link.get_text(strip=True) if album_link else "")
                or album_cell.get_text(strip=True)
                or "앨범 없음"
            )
        else:
            song_data["album"] = "앨범 없음"

        img_cell = row.find("td", class_="albumImg")
        if img_cell:
            img_tag = img_cell.find("img")
            if img_tag and img_tag.get("src"):
                song_data["image_url"] = urljoin(self._url, img_tag["src"])

        return song_data
