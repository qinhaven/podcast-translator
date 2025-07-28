import requests
import os
import logging
from typing import List, Dict, Optional, Union
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class ListenNotesAPIError(Exception):
    """Custom exception for Listen Notes API errors."""
    pass

class PodcastSearchError(Exception):
    """Custom exception for podcast search errors."""
    pass

class DownloadError(Exception):
    """Custom exception for download errors."""
    pass

class PodcastSearcher:
    """A class to handle podcast search and download operations."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the PodcastSearcher.
        
        Args:
            api_key: Listen Notes API key. If None, loads from environment.
        """
        self.api_key = api_key or os.getenv("LISTEN_NOTES_API_KEY")
        if not self.api_key:
            raise ValueError("Listen Notes API key is required. Set LISTEN_NOTES_API_KEY environment variable.")
        
        self.base_url = "https://listen-api.listennotes.com/api/v2"
        self.headers = {"X-ListenAPI-Key": self.api_key}
        
        # Validate API key by making a test request
        self._validate_api_key()
    
    def _validate_api_key(self) -> None:
        """Validate the API key by making a test request."""
        try:
            test_url = f"{self.base_url}/search"
            params = {"q": "test", "type": "episode", "len_min": 1}
            response = requests.get(test_url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 401:
                raise ListenNotesAPIError("Invalid API key")
            elif response.status_code != 200:
                raise ListenNotesAPIError(f"API validation failed with status {response.status_code}")
                
            logger.info("API key validated successfully")
        except requests.RequestException as e:
            raise ListenNotesAPIError(f"Failed to validate API key: {e}")
    
    def search_podcast(
        self, 
        query: str, 
        max_results: int = 5,
        min_length: int = 5,
        sort_by_date: bool = False,
        language: Optional[str] = None,
        region: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for podcast episodes.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            min_length: Minimum episode length in minutes
            sort_by_date: Sort results by date (0=relevance, 1=date)
            language: Language code (e.g., 'en', 'es')
            region: Region code (e.g., 'us', 'gb')
            
        Returns:
            List of podcast episode dictionaries
            
        Raises:
            PodcastSearchError: If search fails
        """
        if not query.strip():
            raise ValueError("Search query cannot be empty")
        
        if max_results <= 0 or max_results > 20:
            raise ValueError("max_results must be between 1 and 20")
        
        try:
            url = f"{self.base_url}/search"
            params = {
                "q": query.strip(),
                "type": "episode",
                "len_min": min_length,
                "sort_by_date": 1 if sort_by_date else 0
            }
            
            if language:
                params["language"] = language
            if region:
                params["region"] = region
            
            logger.info(f"Searching for podcasts with query: '{query}'")
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            results = data.get("results", [])[:max_results]
            
            logger.info(f"Found {len(results)} podcast episodes")
            return results
            
        except requests.RequestException as e:
            error_msg = f"Failed to search podcasts: {e}"
            logger.error(error_msg)
            raise PodcastSearchError(error_msg)
        except (KeyError, ValueError) as e:
            error_msg = f"Invalid response format: {e}"
            logger.error(error_msg)
            raise PodcastSearchError(error_msg)
    
    def download_episode_mp3(
        self, 
        audio_url: str, 
        output_path: Union[str, Path] = "downloaded_episode.mp3",
        chunk_size: int = 8192,
        timeout: int = 300
    ) -> Path:
        """
        Download an MP3 file from a URL.
        
        Args:
            audio_url: URL of the MP3 file to download
            output_path: Path where to save the file
            chunk_size: Size of chunks to download at once
            timeout: Request timeout in seconds
            
        Returns:
            Path object of the downloaded file
            
        Raises:
            DownloadError: If download fails
        """
        if not audio_url:
            raise ValueError("Audio URL cannot be empty")
        
        # Convert to Path object
        output_path = Path(output_path)
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            logger.info(f"Starting download from: {audio_url}")
            logger.info(f"Saving to: {output_path}")
            
            response = requests.get(audio_url, stream=True, timeout=timeout)
            response.raise_for_status()
            
            # Get file size for progress tracking
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:  # Filter out keep-alive chunks
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Log progress for large files
                        if total_size > 0 and downloaded_size % (chunk_size * 100) == 0:
                            progress = (downloaded_size / total_size) * 100
                            logger.info(f"Download progress: {progress:.1f}%")
            
            file_size = output_path.stat().st_size
            logger.info(f"Download completed. File size: {file_size:,} bytes")
            
            return output_path
            
        except requests.RequestException as e:
            error_msg = f"Failed to download file: {e}"
            logger.error(error_msg)
            # Clean up partial download
            if output_path.exists():
                output_path.unlink()
            raise DownloadError(error_msg)
        except OSError as e:
            error_msg = f"Failed to save file: {e}"
            logger.error(error_msg)
            raise DownloadError(error_msg)
    
    def get_episode_info(self, episode_id: str) -> Dict:
        """
        Get detailed information about a specific episode.
        
        Args:
            episode_id: Listen Notes episode ID
            
        Returns:
            Episode information dictionary
            
        Raises:
            PodcastSearchError: If request fails
        """
        try:
            url = f"{self.base_url}/episodes/{episode_id}"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            error_msg = f"Failed to get episode info: {e}"
            logger.error(error_msg)
            raise PodcastSearchError(error_msg)
    
    def search_podcasts_by_genre(self, genre: str, max_results: int = 5) -> List[Dict]:
        """
        Search for podcasts by genre.
        
        Args:
            genre: Genre name (e.g., 'Technology', 'Business')
            max_results: Maximum number of results
            
        Returns:
            List of podcast dictionaries
        """
        return self.search_podcast(f"genre:{genre}", max_results=max_results)

