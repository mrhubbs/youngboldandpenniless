module Jekyll
    module CustomFilters
        $date_suffixes = {
            '1' => 'st', '2' => 'nd', '3' => 'rd', '4' => 'th', '5' => 'th',
            '6' => 'th', '7' => 'th', '8' => 'th', '9' => 'nth', '10' => 'th',
            '11' => 'th', '12' => 'th', '13' => 'th', '14' => 'th', '15' => 'th',
            '16' => 'th', '17' => 'th', '18' => 'th', '19' => 'th', '20' => 'th',
            '21' => 'st', '22' => 'nd', '23' => 'rd', '24' => 'th', '25' => 'th',
            '26' => 'th', '27' => 'th', '28' => 'th', '29' => 'nth', '30' => 'th',
            '31' => 'st'
        }

        # "pretty formats" a date like this:
        # Tuesday, March 1st, 2018
        def pretty_date(date)
            if (date == nil)
                return date
            end

            # format the date into: Tuesday, March 1, 2018
            formatted_date = date.strftime("%A, %B %-d, %Y")
            # split into weekday, month and date, and year
            weekday, month_date, year = formatted_date.split(',')

            # split month and date into month and date
            month, date = month_date.split(' ')
            # append the suffix onto the date
            date += $date_suffixes[date]

            # join everything back together
            [weekday, [month, date].join(' '), year].join(', ')
        end
    end
end

Liquid::Template.register_filter(Jekyll::CustomFilters)
