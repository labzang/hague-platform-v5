"""
크롤러 아웃바운드 어댑터 (IChartCrawlPort 구현)
"""
import re
from abc import ABC, abstractmethod
from typing import List
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None  # type: ignore[assignment]


# domain.ports 미로드 시 사용할 스텁 (전역에 한 번만 정의)
class _IChartCrawlPortStub(ABC):
    """도메인 포트 미로드 시 스텁 (실행 시에는 domain.ports 사용)."""
    @abstractmethod
    def fetch_chart(self) -> List[dict]: ...


try:
    from labzang.apps.crawler.domain.ports import IChartCrawlPort
except ImportError:
    IChartCrawlPort = _IChartCrawlPortStub  # type: ignore[misc, assignment]


class BugsCrawlAdapter(IChartCrawlPort):
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
        if requests is None or BeautifulSoup is None:
            raise ImportError(
                "벅스 차트 크롤링에 requests, beautifulsoup4 가 필요합니다. "
                "pip install requests beautifulsoup4"
            )
        try:
            response = requests.get(
                self._url, headers=self._headers, timeout=10
            )
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
                try:
                    song_data = self._parse_row(row, idx)
                    if song_data.get("title") and song_data["title"] != "제목 없음":
                        songs.append(song_data)
                except Exception:
                    continue
            return songs
        except requests.RequestException:
            return []
        except Exception:
            return []

    def _parse_row(self, row, idx: int) -> dict:
        song_data: dict = {}

        rank_cell = row.find("td", class_="ranking")
        if rank_cell:
            rank_text = rank_cell.get_text(strip=True)
            rank_match = re.search(r"\d+", rank_text)
            song_data["rank"] = int(rank_match.group()) if rank_match else idx
        else:
            song_data["rank"] = idx

        title_cell = row.find("p", class_="title")
        if title_cell:
            title_link = title_cell.find("a")
            song_data["title"] = (
                title_link.get_text(strip=True) if title_link else title_cell.get_text(strip=True)
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
                artists = [link.get_text(strip=True) for link in artist_links]
                song_data["artist"] = ", ".join(artists)
            else:
                song_data["artist"] = artist_cell.get_text(strip=True)
        else:
            song_data["artist"] = "아티스트 없음"

        album_cell = row.find("p", class_="album")
        if album_cell:
            album_link = album_cell.find("a")
            song_data["album"] = (
                album_link.get_text(strip=True) if album_link else album_cell.get_text(strip=True)
            )
        else:
            song_data["album"] = "앨범 없음"

        img_cell = row.find("td", class_="albumImg")
        if img_cell:
            img_tag = img_cell.find("img")
            if img_tag and img_tag.get("src"):
                song_data["image_url"] = urljoin(self._url, img_tag["src"])

        return song_data
