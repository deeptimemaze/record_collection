#!/usr/bin/env python3
"""Export the concerts you have marked as attended on setlist.fm to a CSV that Crate can import.

Usage:
    python3 tools/setlistfm_export.py YOUR_SETLISTFM_USERNAME [output.csv]

The setlist.fm API needs a free API key (setlist.fm → your account → Settings → API).
The script reads it from the SETLISTFM_API_KEY environment variable, or asks for it
without showing what you type. The key is never written to disk.

Then in Crate: Data → Concerts → Choose concerts CSV.
"""
import csv, getpass, json, os, subprocess, sys, time, urllib.parse

API = 'https://api.setlist.fm/rest/1.0'
COLUMNS = ['Date', 'Artist', 'Artist MBID', 'Venue', 'City', 'Country', 'Tour', 'Songs', 'Setlist ID', 'URL']


def fetch(path, key):
    """GET one API page with curl (it uses the system's certificates), with simple rate-limit handling."""
    for attempt in range(5):
        p = subprocess.run(['curl', '-sS', '--max-time', '30', '-w', '\n%{http_code}',
                            '-H', 'Accept: application/json', '-H', '@-',  # key header from stdin, not the process list
                            '-H', 'User-Agent: CrateSetlistExport/1.0', API + path],
                           input='x-api-key: ' + key + '\n', capture_output=True, text=True)
        body, _, code = p.stdout.rpartition('\n')
        if p.returncode != 0:
            sys.exit('Could not reach setlist.fm: ' + p.stderr.strip())
        if code == '200':
            return json.loads(body)
        if code == '404':
            return None
        if code == '429':
            time.sleep(2 + 3 * attempt)
            continue
        if code in ('401', '403'):
            sys.exit('setlist.fm refused the API key (HTTP %s). Check the key in your setlist.fm API settings.' % code)
        sys.exit('setlist.fm answered HTTP %s: %s' % (code, body[:200]))
    sys.exit('setlist.fm kept asking to slow down. Try again in a minute.')


def iso(d):
    """setlist.fm dates are dd-MM-yyyy."""
    try:
        dd, mm, yyyy = d.split('-')
        return f'{yyyy}-{mm}-{dd}'
    except ValueError:
        return d


def row(s):
    artist, venue = s.get('artist') or {}, s.get('venue') or {}
    city = venue.get('city') or {}
    songs = [song.get('name', '') for part in (s.get('sets') or {}).get('set', []) for song in part.get('song', [])]
    return {
        'Date': iso(s.get('eventDate', '')),
        'Artist': artist.get('name', ''),
        'Artist MBID': artist.get('mbid', ''),
        'Venue': venue.get('name', ''),
        'City': city.get('name', ''),
        'Country': (city.get('country') or {}).get('name', ''),
        'Tour': (s.get('tour') or {}).get('name', ''),
        'Songs': '; '.join(x for x in songs if x),
        'Setlist ID': s.get('id', ''),
        'URL': s.get('url', ''),
    }


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        sys.exit(__doc__)
    user = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else 'setlistfm-concerts.csv'
    key = os.environ.get('SETLISTFM_API_KEY') or getpass.getpass('setlist.fm API key (not shown): ').strip()
    if not key:
        sys.exit('An API key is needed.')

    rows, page, total = [], 1, None
    while True:
        j = fetch(f'/user/{urllib.parse.quote(user)}/attended?p={page}', key)
        if j is None:
            if page == 1:
                sys.exit(f'No setlist.fm user called "{user}", or they have not marked any concerts as attended.')
            break
        total = j.get('total', 0)
        batch = j.get('setlist', [])
        rows += [row(s) for s in batch]
        print(f'\rFetched {len(rows)} of {total} concerts', end='', flush=True)
        if not batch or len(rows) >= total:
            break
        page += 1
        time.sleep(0.6)  # setlist.fm allows about 2 requests a second
    print()

    rows.sort(key=lambda r: r['Date'], reverse=True)
    with open(out, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f'Wrote {len(rows)} concerts to {out}. Import it in Crate: Data → Concerts → Choose concerts CSV.')


if __name__ == '__main__':
    main()
