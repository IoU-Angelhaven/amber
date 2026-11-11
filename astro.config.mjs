// @ts-check
import { defineConfig } from 'astro/config';
import { readdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

// Where the site is published. The GitHub workflow fills these in automatically
// (from the GitHub Pages settings), so the same code works both at
// https://iou-angelhaven.github.io/ehealth-implementation/ and later at https://ehealth-implementation.eu/.
const site = process.env.SITE_URL || 'https://iou-angelhaven.github.io';
const base = process.env.BASE_PATH ?? '/ehealth-implementation';

/**
 * After the build, add the sub-folder to any link or image that still points to the
 * site root – for example a link or image written inside Markdown text (/media/file.pdf).
 * Templates already use url() from src/lib/url.ts.
 * The same step also writes sitemap.xml and robots.txt.
 * @returns {import('astro').AstroIntegration}
 */
function prefixRootLinks() {
  const prefix = base.replace(/\/$/, '');
  return {
    name: 'prefix-root-links',
    hooks: {
      'astro:build:done': async ({ dir }) => {
        const root = fileURLToPath(dir);
        const files = (await readdir(root, { recursive: true })).filter((f) => f.endsWith('.html'));

        // sitemap.xml and robots.txt for search engines (every published page except the 404 page)
        const origin = site.replace(/\/$/, '') + prefix;
        const pages = files
          .filter((f) => f.endsWith('index.html'))
          .map((f) => '/' + f.split(/[\\/]/).slice(0, -1).join('/'))
          .map((p) => (p === '/' ? '/' : p + '/'))
          .sort();
        const sitemap =
          '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          pages.map((p) => `  <url><loc>${origin}${p}</loc></url>`).join('\n') +
          '\n</urlset>\n';
        await writeFile(join(root, 'sitemap.xml'), sitemap);
        await writeFile(join(root, 'robots.txt'), `User-agent: *\nAllow: /\n\nSitemap: ${origin}/sitemap.xml\n`);

        if (!prefix) return;
        const re = new RegExp(`\\b(href|src)="/(?!/)(?!${prefix.slice(1)}(?:/|"))`, 'g');
        for (const f of files) {
          const path = join(root, f);
          const html = await readFile(path, 'utf8');
          const fixed = html.replace(re, `$1="${prefix}/`);
          if (fixed !== html) await writeFile(path, fixed);
        }
      },
    },
  };
}

export default defineConfig({
  site,
  base,
  trailingSlash: 'ignore',
  integrations: [prefixRootLinks()],
});
