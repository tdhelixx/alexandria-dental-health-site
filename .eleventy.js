const { EleventyI18nPlugin } = require("@11ty/eleventy");

module.exports = function(eleventyConfig) {
  // Copy static assets
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/js");
  eleventyConfig.addPassthroughCopy("src/images");
  eleventyConfig.addPassthroughCopy("*.css");
  eleventyConfig.addPassthroughCopy("api");
  eleventyConfig.addPassthroughCopy("s");
  eleventyConfig.addPassthroughCopy("wp-content");
  eleventyConfig.addPassthroughCopy("wp-includes");
  
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
    return collectionApi.getFilteredByGlob("src/blog/**/*.md");
  });
  
  eleventyConfig.addCollection("services", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/services/**/*.md");
  });
  
  eleventyConfig.addCollection("pages", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/pages/**/*.md");
  });
  
  // Custom filters
  eleventyConfig.addFilter("dateDisplay", function(dateObj) {
    return new Date(dateObj).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric"
    });
  });
  
  // Shortcodes
  eleventyConfig.addShortcode("year", () => `${new Date().getFullYear()}`);
  
  // Layout aliases
  eleventyConfig.addLayoutAlias("base", "layouts/base.njk");
  eleventyConfig.addLayoutAlias("page", "layouts/page.njk");
  eleventyConfig.addLayoutAlias("blog", "layouts/blog.njk");
  eleventyConfig.addLayoutAlias("service", "layouts/service.njk");
  
  return {
    templateFormats: ["md", "njk", "html", "liquid"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    dataTemplateEngine: "njk",
    dir: {
      input: "src",
      includes: "_includes",
      data: "_data",
      output: "_site"
    }
  };
}; 