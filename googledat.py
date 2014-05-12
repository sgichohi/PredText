from google_ngram_downloader import readline_google_store


fname, url, records = next(readline_google_store(ngram_len=5))
count = 0

for record in records:
    count += 1
    if count > 1000000:
        print record
        break
