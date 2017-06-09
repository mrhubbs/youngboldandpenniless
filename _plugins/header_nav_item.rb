# example plugin - not used

module Jekyll
    class HeaderNavItemTag < Liquid::Tag

        def initialize(tag_name, text, tokens)
            super
            @args = eval(text)
        end

        def render(context)
            classes = "nav-item #{@args[:classes]}"

            if @args[:site]
                classes += ' site-nav-heading'
            end

            # TODO: get page name
            if @args[:page_name] == @args[:url] or @args[:active]
                classes += ' nav-item-active'
            end

            "<li>
                <a href='#{@args[:url]}' class='nav-item #{@args[:classes]}'>#{@args[:code]}#{@args[:title]}</a>
            </li>"
        end
    end
end

Liquid::Template.register_tag('header_nav_item', Jekyll::HeaderNavItemTag)
