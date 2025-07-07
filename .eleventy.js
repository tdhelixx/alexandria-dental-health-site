const { EleventyI18nPlugin } = require("@11ty/eleventy");

module.exports = function(eleventyConfig) {
  // Copy static assets
  eleventyConfig.addPassthroughCopy("src/images");
  eleventyConfig.addPassthroughCopy("src/js");
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/_data");
  
  // Copy WordPress content directories for compatibility
  eleventyConfig.addPassthroughCopy("wp-content");
  eleventyConfig.addPassthroughCopy("images");
  
  // Watch CSS files for changes
  eleventyConfig.addWatchTarget("./src/css/");
  eleventyConfig.addWatchTarget("./alexandria-dental-enhanced-styles.css");
  
  // Enable quiet mode
  eleventyConfig.setQuietMode(true);
  
  // Configure markdown
  let markdownIt = require("markdown-it");
  let markdownItAttrs = require("markdown-it-attrs");
  
  let markdownLibrary = markdownIt({
    html: true,
    breaks: true,
    linkify: true
  }).use(markdownItAttrs);
  
  eleventyConfig.setLibrary("md", markdownLibrary);
  
  // Collections
  eleventyConfig.addCollection("blog", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/blog/**/*.md").sort((a, b) => {
      return b.date - a.date; // Sort by date, newest first
    });
  });
  
  eleventyConfig.addCollection("services", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/services/**/*.md");
  });
  
  eleventyConfig.addCollection("pages", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/pages/**/*.md");
  });
  
  // Set default permalinks for collections
  eleventyConfig.addGlobalData("permalink", function() {
    return function(data) {
      // Default permalink structure
      if (data.page.inputPath.includes("/blog/")) {
        return `/blog/${data.page.fileSlug}/`;
      }
      if (data.page.inputPath.includes("/services/")) {
        return `/${data.page.fileSlug}/`;
      }
      return false; // Use 11ty default
    };
  });
  
  // Custom filters
  eleventyConfig.addFilter("dateDisplay", function(dateObj) {
    return new Date(dateObj).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric"
    });
  });
  
  // Head filter - get first N items from array
  eleventyConfig.addFilter("head", function(array, n) {
    if (!Array.isArray(array)) return [];
    return array.slice(0, n);
  });
  
  // Exclude item filter
  eleventyConfig.addFilter("excludeItem", function(array, item) {
    if (!Array.isArray(array)) return [];
    return array.filter(arrayItem => arrayItem.url !== item.url);
  });
  
  // Get previous collection item
  eleventyConfig.addFilter("getPreviousCollectionItem", function(collection, page) {
    if (!Array.isArray(collection)) return null;
    const index = collection.findIndex(item => item.url === page.url);
    return index > 0 ? collection[index - 1] : null;
  });
  
  // Get next collection item
  eleventyConfig.addFilter("getNextCollectionItem", function(collection, page) {
    if (!Array.isArray(collection)) return null;
    const index = collection.findIndex(item => item.url === page.url);
    return index < collection.length - 1 ? collection[index + 1] : null;
  });
  
  // Shortcodes
  eleventyConfig.addShortcode("year", () => `${new Date().getFullYear()}`);
  
  // Layout aliases
  eleventyConfig.addLayoutAlias("base", "layouts/base.njk");
  eleventyConfig.addLayoutAlias("page", "layouts/page.njk");
  eleventyConfig.addLayoutAlias("blog", "layouts/blog.njk");
  eleventyConfig.addLayoutAlias("service", "layouts/service.njk");
  
  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    templateFormats: ["md", "njk", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    dataTemplateEngine: "njk"
  };
}; 