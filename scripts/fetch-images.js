#!/usr/bin/env node
/**
 * Fetch images from Unsplash API.
 *
 * Usage: node fetch-images.js --query "nature landscape" --count 5
 *
 * Requires UNSPLASH_ACCESS_KEY environment variable.
 * Output: JSON array of image objects to stdout.
 */
const https = require('https');

function searchUnsplash(query, count = 5) {
  const key = process.env.UNSPLASH_ACCESS_KEY;
  if (!key) {
    console.error('Set UNSPLASH_ACCESS_KEY environment variable');
    process.exit(1);
  }

  return new Promise((resolve, reject) => {
    const url = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(query)}&per_page=${count}&orientation=landscape`;
    const options = { headers: { 'Authorization': `Client-ID ${key}` } };

    https.get(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const parsed = JSON.parse(data);
        resolve(parsed.results.map(r => ({
          id: r.id,
          url: r.urls.regular,
          download: r.links.download_location,
          description: r.description || r.alt_description,
          credit: `${r.user.name} on Unsplash`
        })));
      });
    }).on('error', reject);
  });
}

const args = process.argv.slice(2);
const queryIdx = args.indexOf('--query');
const countIdx = args.indexOf('--count');
const query = queryIdx >= 0 ? args[queryIdx + 1] : args[0];
const count = countIdx >= 0 ? parseInt(args[countIdx + 1]) : 5;

if (!query) {
  console.error('Usage: node fetch-images.js --query "search term" [--count N]');
  process.exit(1);
}

searchUnsplash(query, count).then(results => {
  console.log(JSON.stringify(results, null, 2));
});
