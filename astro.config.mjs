import { defineConfig } from 'astro/config';
import tailwind from "@astrojs/tailwind";

import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  site: 'https://voorste-eng.nl',
  integrations: [tailwind(), sitemap()],
  i18n: {
    defaultLocale: "nl",
    locales: ["nl", "en", "de"],
    routing: {
      prefixDefaultLocale: true
    }
  }
});