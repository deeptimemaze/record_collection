# Record collection

A small installable web app for keeping track of where your records and CDs are stored. Import your collection from Discogs, place each record in a storage location, and search by artist or title to find out where it sits.

## Features

- Import a Discogs CSV export. Choose which formats to keep: LP/12"/10", 7", shellac, CD, cassette.
- Place each record in a storage location by section and position, counting from 1.
- See each location as a diagram, with the number of records in every section.
- Give each record a genre, a free-text comment and a favourite star. Favourites have their own tab.
- Search by artist, title or comment. Accents are ignored, so "sigur ros" finds Sigur Rós and "einsturzende" finds Einstürzende.
- Filter by format and genre, or show only records that are not placed yet.
- Back up and restore with a CSV export that includes every record's location, genre, comment and favourite star.
- Dark look inspired by the Discogs app, with a light version that follows your phone's setting.
- Works offline and can be installed on a phone's home screen.

## Storage locations

Three locations are set up by default and can be edited in the **Data** tab:

| Location | Layout | Holds |
| --- | --- | --- |
| Kallax shelf | 3 × 4 sections, numbered along each row from the top left | LP, 12", 10" |
| 7" case | One compartment, capacity 200 | 7" singles |
| String Pocket | 8 wall units with 3 shelves each, shelves numbered 1–24 from the top | CDs |

You can add more locations, either as a grid of sections or as stacked units with shelves, and set a capacity for each section.

When you place a record at a position that is already taken, the records from that position onwards shift one place along, as if you slid it in on the shelf.

## Use it

1. Export your collection from Discogs as a CSV.
2. Open the app, go to **Data**, and choose the CSV file.
3. Tick the formats you want to track and import.
4. In **Records**, tap a record and choose where it goes.
5. Use the search box to find a record later. **Shelf** shows each location and what is in every section.

The import also reads Genre, Comment and Favourite columns if the CSV has them (a Favourite cell of `Yes` marks a favourite). Importing again keeps the locations, genres, comments and stars of records that match by Discogs release ID, so you can add records on Discogs, export, and re-import without losing your work. A value in the CSV wins over the app's; an empty cell keeps what the app has.

## Your data

Everything is stored in your browser's local storage on your own device. Nothing is uploaded, and this repository contains only the app, not your collection. Browser storage can be cleared, so use **Data → Export CSV** now and then to keep a backup. Don't commit your Discogs CSV to a public repository.

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
| `icon-192.png`, `icon-512.png` | App icons |

There is no build step and there are no dependencies. You can also open `index.html` directly in a browser, without installing, though the home screen icon and offline mode need the hosted version.

## Updating

If you change `index.html` on the host, change the cache name in `sw.js` (for example from `vinyl-shelf-v4` to `vinyl-shelf-v5`) so phones pick up the new version.
