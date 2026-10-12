
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

from src.logger import Logger

class TranscriptFetcher:
    def __init__(self, video_id: str = None):
        self.logger = Logger(__name__, log_file="transcript_fetcher.log", level="DEBUG").logger
        self.youtube_transcript_api = YouTubeTranscriptApi()
        self.video_id = video_id

    def fetch_transcript(self):

        """"
        Fetches the transcript for a given YouTube video ID using the YouTubeTranscriptApi.
        Arguments:
            video_id (str): The YouTube video ID for which to fetch the transcript.
        Returns:
            str: The fetched transcript as a single string, or None if transcripts are disabled or
            an error occurs.
        """
        try:
            transcript_list = self.youtube_transcript_api.fetch(self.video_id,languages=['en']) 
            transcript = " ".join(segment.text for segment in transcript_list)
            if not transcript.strip():
                self.logger.warning(
                    "Transcript is empty for video ID: %s",
                    self.video_id
                )
                return None
            self.logger.info(f"Successfully fetched transcript for video ID: {self.video_id}") 
            return transcript
        except TranscriptsDisabled:
            self.logger.warning(f"Transcripts are disabled for video ID: {self.video_id}")
            self.logger.error(f"Failed to fetch transcript for video ID: {self.video_id}")
            return None
        except Exception as e:
            self.logger.error(f"An error occurred while fetching the transcript: {e}")
            return None