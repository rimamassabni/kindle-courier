from datetime import datetime, time, timedelta
import tempfile

opml_file_path = "sample-feeds.opml"
output_directory = tempfile.gettempdir()
published_after = datetime.combine(datetime.today(), time.min) - timedelta(days=30)
