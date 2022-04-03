========
LogTools
========

Goal
----

Log viewer application that displays separate runs from a log file
in separate tabs and enable fast searching pre-defined patterns.

Concept
-------

There are many great log viewer out. But I wanted to write mine.
The main difference that I don't really know in advance what I'm
looking for in the logs. I know some patterns, and then I just
want jump back and forth through them and looking for anomalies.
When I find something else to search then I record a new pattern.

I also want to see some blocks of log at once. So one run of
the logger application or one processing block or so. All these
will go to their own tab, quickly showing me how many blocks do
the log have.

Finally I would like to see some statistics about my logs and
patterns.

Status
------

All the above things are done at a very basic level. It is already
usable, but really limited. Also design is a bit raw, need some
refactor iteration.
I would like to continue and enhance since I
need it and I have much more idea, how to go on.

Ideas / Todo
------------

* background / foreground text colors to give more possibility
* color selector dialog
* style preview in the pattern edit dialog
* simple text search in addition to regexp, since many pattern has "."
* regexp compile check and check not to match the empty string
* text visible / hidden option is present but make it work
* visible / hidden option for all the other not matched lines
* define block sections to show user operation start / stops
* show where we are in the process like: init > section 1 > section 2
* fold / unfold sections
* search field under log display with options to create pattern from it
* right click menu to create pattern from selected text
* change patterns order (arrow buttons, I don't think I can do drag and drop)
* better tab management for lot of tabs, dropdown or tab list panel
* display props as hint when mouse over a tab
* display elapsed time info in properties
* handle more log types with different log content order
* remove DEBUG/INFO/... text and display as icons
* remove timestamp and display as tooltip for the line number
* timestamp reduction to hh:mm:ss
* display time as time from start or delta from prev row
* add pattern search for time or timedelta things

:-)

BigBirdCode
