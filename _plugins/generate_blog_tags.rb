
# for String::replace_diacritics
require 'nuggets/i18n'

# Adapted from code here: https://github.com/pattex/jekyll-tagging

module Jekyll
  class TagPageGenerator < Generator
    safe true

    # Substitutes any diacritics in _str_ with their ASCII equivalents,
    # whitespaces with dashes and converts _str_ to downcase.
    def jekyll_tagging_slug(str)
      str.to_s.replace_diacritics.downcase.gsub(/\s/, '-')
    end

    def generate(site)
      @site = site

      generate_tag_pages
    end

    def generate_tag_pages
      active_tags.each { |tag, posts| new_tag(tag, posts) }
    end

    def new_tag(tag, posts)
      data = {
        'layout' => 'tag_page',
        'posts' => posts.sort.reverse!,
        'tag' => tag,
        # TODO: this is the easy way to get the data in, instead of reading the
        # layout front-matter
        'site_section' => 'blog'
      }

      name = yield data if block_given?
      name ||= tag
      name = jekyll_tagging_slug(name)

      tag_dir = @site.config['tag_page_dir']

      name = Utils.slugify(name)
      page_name = "#{name}#{@site.layouts[data['layout']].ext}"
      @site.pages << TagPage.new(
        @site, @site.source, tag_dir, page_name, data
      )
    end

    def active_tags
      return @site.tags
    end
  end

  class TagPage < Page
    def initialize(site, base, dir, name, data)
      @content = data.delete('content') || ''
      @data = data

      super(site, base, dir[-1, 1] == '/' ? dir : '/' + dir, name)
    end

    # Usually this reads the front matter for the page we're creating.
    # In this case we don't have any.
    def read_yaml(*)
      # Do nothing
    end
  end
end
