# WCIF to CSV, for color-coded Championship Schedules

This tool enables the user to generate a useful `.csv` or `.xlsx` file, to later generate beautiful badges like these ones, aided by the design program of your choosing. These ones were made using *Affinity Publisher*, which is now available though *Canva*'s non-profit program, but can also be made with *Adobe Illustrator* (WC2023 badges were made using this ifaik).

![](https://www.worldcubeassociation.org/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsiZGF0YSI6NTEyMzUsInB1ciI6ImJsb2JfaWQifX0=--9b20887f26a558ba29601731eb52e383979f87cb/Example_badges.png)

Parameters the user has to modify before running the program:
* `competition_id`: Enter the competition ID as showed in the url of the competition.
* `stage_count`: Number of stages with tasks associated to them. *e.g 4 main stages + 1 side stage = 5*


Other lines that you have to modify are:
* Hardcoding *Multi-Blind* (and other non-standard tasks') group_ids. Run the code several times and manually hardcode the codes for this groups. You can also search the `.wcif` file of the competition and note these down. There probably is a way to code this here, but it's not yet done.

* If you want to generate a `.csv` file with only or without *staff* members, uncomment either line `51` or `52`.

* You can add custom letter codes for different tasks in line `71`.

* `get_color` function has to be adapted to your specific scenario, adding the specific stage names, as well as a route to a `.png` image of the stage's colour in a rectangle.

The `.afdesign` files for the Euro 2024 badges can be found in 'Euro2024-usecase', but in essence, here's what you have to do for this to work properly:
* Create a schedule table with all of the *groups/waves* the competition is going to have. Each wave may contain several subgroups in different stages. *e.g. 3x3x3 G1, 3x3x3 G2, etc*. A column on the left is suggested to include the scheduled start times. Leave a column on the right, so the task letter code can be written by our design program.
* Measure the size of the cell that will contain our letter code, so we can make `.png` files of that size with all of the different colours.
* Create empty image items (as many as groups you have) and situate them *below* the table, so the text is above the coloured block.
* Don't forget to account for Side Room groups, these should also be included in the schedule.
* I recommend adding the *WCAID* and *CompetitorID* in the back page as well, so there is no need to look at the front to identify the competitor (this is more useful that you could think).

Some other nice touches for the front page:
* Create a flag rectangle so the competitor's flag can be included.
* Include the WCAID and ID of the competitor.
* Create a centered text block with at least 3 lines for competitor's names. Add some margins with the page border for a better look.
* You can also add a text block for the roles (Staff/Delegate, etc) of the competitors.
