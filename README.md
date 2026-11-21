# Crate

A small installable web app for keeping track of where your records and CDs are stored. Import your collection from Discogs, place each record in a storage location, and search by artist or title to find out where it sits.

## Features

- Import a Discogs CSV export. Choose which formats to keep: LP/12"/10", 7", shellac, CD, cassette.
- Place each record in a storage location by section and position, counting from 1.
- See each location as a wireframe 3D drawing, with the number of records in every section, shelf or drawer. Tap a drawer to pull it out and see its records standing front to back.
- Give each record a genre, a free-text comment and a star. Starred records have their own tab.
- Search by artist, title, comment, Discogs notes, label, catalogue number, folder or Discogs style. Accents are ignored, so "sigur ros" finds Sigur Rós and "einsturzende" finds Einstürzende.
- Filter by format and genre, or show only records that are not placed yet.
- **Explore** tab: pick a random record (filter by format and genre, starred only, only placed, favour unplayed), keep a play-next list, and see which records have gone longest without being played. Mark a record as played from the pick or from its sheet.
- Speed: vinyl cards show 33⅓, 45 or 78 rpm. Discogs leaves the speed out of its CSV export, so the app fills it in where the format makes it clear (LP, 7", shellac). **Data → Fetch details from Discogs** looks up each release on the public Discogs API for the exact speed, genres, styles and country, starting with records whose speed is unclear. It runs at about 24 records a minute and keeps going where it left off. Records without a genre get the first Discogs genre. The Format filters have a Speed group.
- Tempo (BPM) for 12" singles and EPs: **Data → Fetch tempos** looks up a suggested BPM for each track, from AcousticBrainz (measured from audio, through MusicBrainz) and from Deezer (by artist and title). About half of the 12"s are found, and a suggestion can be half or double the real tempo or belong to another mix, so the record sheet shows each track's values with **×½**, **×2**, **Confirm** and **Use** buttons. A big **TAP** button measures the tempo as you tap along to the record; it saves itself a moment after you stop. Cards show the BPM (with a ~ while it's only a suggestion), the Format filters have a Tempo group (90–100, 120–125 and so on), and Stats shows the spread. Deezer is called with JSONP, its only way to work from a web page.
- Discogs details: the record sheet shows the speed, format tags (reissue, limited, mono, gatefold, coloured vinyl and so on), label and catalogue number, country, genres and styles, your rating, condition, where and when you bought it and the price, your Discogs folder and notes, and a link to the release on Discogs.
\1: the Released year from Discogs is the year of your pressing. **Data → Fetch original years** looks up when each album first came out on MusicBrainz (the release group's first release date). Where it is known, the card shows that year in **bold**, instead of the pressing year, and the Timeline and the decade stats use it. It is saved with each record and included in the CSV export as the `Original release` column.
- Timeline: a vertical timeline by release year with this year on top. Each record hangs off its year, and you can filter by format and genre.
- Stats: counts by format, speed, genre and decade, records added per year, how full each storage location is, and, when the Discogs export has them, your ratings, top labels, where you bought your records and what you spent.
- Album covers from MusicBrainz and the Cover Art Archive replace the disc icon on the cards when one is found. They are fetched as you scroll, saved on the phone, and can be switched off in the Data tab.
- Back up and restore with a CSV export that includes every record's location, genre, comment and star.
- Cyberpunk brutalist look: near-black with a faint grid, monospace type, square 2px outlines, one acid-lime accent and magenta for warnings and hard shadows. It follows your phone's light or dark setting; the light version is off-white and black.
- Works offline and can be installed on a phone's home screen.

## Storage locations

Three locations are set up by default and can be edited in the **Data** tab:

| Location | Layout | Holds |
| --- | --- | --- |
| Kallax shelf | 3 × 4 sections, numbered along each row from the top left | LP, 12", 10" |
| 7" case | One compartment, capacity 200 | 7" singles |
| String Pocket | Shelves layout: 8 units with 3 shelves each, 78 × 20 × 15 cm per shelf, numbered 1–24 from the top | CDs |

You can add more locations with one of three layouts:

- **Grid section**: columns and rows of square sections, drawn as cubes (like a Kallax). Sections are numbered along each row from the top left.
- **Shelves**: units side by side and stacked, each with a number of shelves. Enter the width, height and depth of each shelf in centimetres; the drawing uses those proportions. Shelves are numbered from the top, unit by unit.
- **Drawers**: a cabinet of drawers side by side and stacked. Enter the width, height and depth of each drawer in centimetres. Drawers are numbered along each row from the top left, and inside a drawer records are numbered from the front to the back.

The drawings are wireframe 3D, with depth going up and to the right. A location can't be made smaller than the highest section, shelf or drawer that holds records, so your placements are never lost by an edit.

When you place a record at a position that is already taken, the records from that position onwards shift one place along, as if you slid it in on the shelf (in a drawer: one place further back).

## Use it

1. Export your collection from Discogs as a CSV.
2. Open the app, go to **Data**, and choose the CSV file.
3. Tick the formats you want to track and import.
4. In **Records**, tap a record and choose where it goes.
5. Use the search box to find a record later. **Storage** shows each location and what is in every section.

The import reads the Discogs columns Label, Catalog#, Rating, CollectionFolder, Collection Bought at, Collection Date, Collection Media and Sleeve Condition, Collection Price and Collection Notes. A record without a genre gets one from its collection folder when the folder names a genre ("Electronic (Vinyl)" gives Electronic; artist folders such as "*Kraftwerk" are skipped). It also reads Genre, Comment and Starred columns if the CSV has them (a Starred cell of `Yes` marks a starred record; a column named Favourite from an older export is read too). Importing again keeps the locations, genres, comments and stars of records that match by Discogs release ID, so you can add records on Discogs, export, and re-import without losing your work. A value in the CSV wins over the app's; an empty cell keeps what the app has. If you own several copies of the same release, they are told apart by the Date Added column, so reordered rows in a Discogs export don't swap their placements. The export also carries Date Added, Last played, Play next and Original release.

## Concerts from setlist.fm

Crate can show which of your records are by artists you've seen live, using the concerts you've marked as **I was there** on [setlist.fm](https://www.setlist.fm). Records by those artists get a **LIVE ×n** tag, the record sheet lists each concert with date and venue (and the song, if a record's title was played that night), and **Explore → Live** shows your concerts by year with the most-seen artists, venues and concerts per year. Tap a concert to find that artist's records.

setlist.fm doesn't allow web apps to call its API, so the concerts come in as a CSV made on a computer:

1. Get a free API key: on setlist.fm, open your account settings and choose **API**. It's for non-commercial use.
2. On a Mac (or any computer with Python 3 and curl), from this folder run:

   ```bash
   python3 tools/setlistfm_export.py YOUR_SETLISTFM_USERNAME
   ```

   It asks for the API key without showing it (or reads it from the `SETLISTFM_API_KEY` environment variable), and writes `setlistfm-concerts.csv`. The key is never saved.
3. Move the file to your phone and import it in **Data → Concerts → Choose concerts CSV**. Importing again replaces the list, so re-run the script when you've been to more concerts.

Concerts are matched to records by artist name. Accents and a leading "The" are ignored, and a record by "A / B", "A & B" or "A feat. B" matches concerts by either artist. Concerts are stored apart from your collection and aren't in the collection CSV export; keep the setlist.fm CSV as their backup.

## Your data

Everything is stored in your browser's local storage on your own device. Nothing of your collection is uploaded, apart from the lookups: for album covers and original years a record's Discogs number, and sometimes its artist and title, are sent to MusicBrainz (covers can be switched off), and **Fetch details from Discogs** sends each Discogs number to Discogs, and this repository contains only the app, not your collection. Browser storage can be cleared, so use **Data → Export CSV** now and then to keep a backup. Don't commit your Discogs CSV to a public repository.

Storage is separate for each web address. If you move from a local file to the hosted version, export a CSV first and import it in the new place.

## Install it on a phone

The app needs to be served over https to be installable. GitHub Pages does this for free:

1. In the repository, go to **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**, select the `main` branch and the `/ (root)` folder, and save.
3. Open the address GitHub gives you in Chrome on your phone.
4. Open the menu and choose **Add to Home screen** or **Install app**.

It then opens full screen like an app and works offline.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole app: layout, styles and logic in one file |
| `manifest.webmanifest` | Name, colours and icons for installing on a home screen |
| `sw.js` | Caches the app so it opens offline |
| `icon-cyber-192.png`, `icon-cyber-512.png` | App icons |
| `icon-cyber.svg` | Source drawing for the app icons |
| `tools/setlistfm_export.py` | Exports your attended concerts from setlist.fm to a CSV for **Data → Concerts** |

There is no build step and there are no dependencies. You can also open `index.html` directly in a browser, without installing, though the home screen icon and offline mode need the hosted version.

## Updating

The app checks for a newer version when it opens, a few seconds after it starts, and whenever you switch back to it. If the version on GitHub is newer, it clears its saved app files and reloads by itself. Your records, locations and album covers are not touched. The **Data** tab shows the running version at the bottom, with a **Check for updates** button.

When you make a new release, raise `APP_VERSION` (and the date) near the top of the script in `index.html`, and change the cache name in `sw.js` to match.
