from datetime import datetime, time, timedelta

opml_file_path = "sample-feeds.opml"
output_directory = "output"
published_after = datetime.combine(datetime.today(), time.min) - timedelta(days=1)
