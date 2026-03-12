---
description: Technical defaults for HTML/CSS output when recreating website designs
---

- Use Tailwind CSS via CDN (`<script src="https://cdn.tailwindcss.com"></script>`)
- Use placeholder images from `https://placehold.co/` when source images aren't provided
- Mobile-first responsive design
- Single `index.html` file unless the user requests otherwise

## Screenshots

Run `npm run screenshot` to capture the page. Optionally pass a target file and output name:

```
node screenshot.js index.html screenshot.png
```

Run `npm install` once before first use to install Puppeteer.
