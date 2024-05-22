"""
Simple Indavideo.hu embed token grabber
"""

# Required Libraries
import urllib.parse
import requests
import re
import time

# Function to get token from indavideo URL
def get_indavideo_token(url: str):
    """
    Get token from indavideo.hu embed URL
    :param url: indavideo.hu embed URL
    :return: Dictionary of urls to video files with token {height <int>: url <str>}
    """
    # Extract video ID from URL
    video_id = re.search(r'https?://(?:(?:embed\.)?indavideo\.hu/player/video/|assets\.indavideo\.hu/swf/player\.swf\?.*\b(\?:v(?:ID|id))=)(?P<id>[\da-f]+)', url).group('id')
    # Get video data
    response = requests.get(
        f'https://amfphp.indavideo.hu/SYm0json.php/player.playerHandler.getVideoData/{video_id}/',
        params={'_': int(time.time())}
    )
    # Extract video data
    video = response.json()['data']
    # Extract video files
    video_files = video.get('video_files', [])
    # Check if video files is a dictionary
    if isinstance(video_files, dict):
        # Convert dictionary to list
        video_files = list(video_files.values())
    # Extract tokens from video data
    filesh = video.get('filesh', {})
    # Initialize tokens dictionary
    tokens = {}
    # Iterate over video files
    for video_url in video_files:
        # Extract height from video URL
        height = re.search(r'.(\d{3,4}).mp4(?:\?|$)', video_url)
        # Check if height is found
        if height:
            height = height.group(1)
        token = filesh.get(str(height))
        if token:
            url_parts = list(urllib.parse.urlparse(video_url))
            query = dict(urllib.parse.parse_qsl(url_parts[4]))
            query.update({'token': token})
            url_parts[4] = urllib.parse.urlencode(query)
            tokens[height] = urllib.parse.urlunparse(url_parts)

    return tokens

print(get_indavideo_token('https://embed.indavideo.hu/player/video/eac6d340e3?autostart=1&hide=titleshare&hq=1'))
