#Timber Sales v0.1 beta

Timber Sales is a program to keep track of Timber Sale scheduling and information. 
This beta version is originally built for the Dept of Natural Resources of Washington State, 
and aspects of the program are specific to the Dept's way of doing business and may not be
applicable for general use. If you are insterested in the program for personal or business use,
contact Pipeline Forestry (contact info at the bottom), and we will be happy to adjust the program
to your specific needs.


Timber Sales uses two main classes for information about the timber sale.

	The Unit class is an individual unit within the timber sale, it holds information like the unit name, 
	the harvest type, acres, MBF (1000 board feet), and MBF per acre; and specifically these are split up 
	further into the different public trusts that the Dept manages. 

	The Sale class holds the Unit classes and holds sale-specific information like sale name, value, total acres
	total MBF, overall MBF per acre, and specifically for the Dept, the sale auction date, field work due date and 
	Dept fiscal year the sale will be sold.


Timber Sales uses a SQLite3 database to store, retrieve and update timber sale data. The timber sale Sale class
is stored as a BLOB by using Python's standard Pickle library. 

To test this program, download the app and the database and keep these items in the same working directory.



Getting Started

	Upon opening Timber Sales, you will see listboxes on the left-hand side, selecting one or multiple parameters within each
	lisbox will show the sales that have the corresponding attributes. For example to see all sales that have a total volume 
	between 4000 and 5000 MBF, select 4000 from the 'MBF' listbox.


	Once the sales frame is populated, each sale has buttons to facilitate the editing of the sale. The 'v' button will expand
	the sale and show the units within the sale, conversely the '^' button will contract the sale. The '/' button will allow 
	you to edit the sale attributes. 

	With the sale expanded you will see the units also have specific buttons. On the units header you will see '+' and '/'. 
	'+' will add a new unit to the sale, and '/' will toggle all of the units into edit mode. On the unit rows 
	you will see the buttons 'X' and '/'. 'X' will delete the corresponding unit from the sale, and '/' will toggle the only 
	corresponding unit into edit mode.

	Once you have completed your editing and would like to commit the changes to the database, select the 'COMMIT' button
	above the listboxes on the left side. If there are missing data or value errors, a warning window will open and the errors
	will be highlighted in red; if there are errors, no changes will be made to database.



Sale Menu--
There are two tools in the Sale Menu, these are New Sale and Delete Sale.

	-New Sale will create a new timber sale, the parameters are Sale Name, Sale Auction Date and Number of Units. The sale is
	 populated with Unit classes with default attributes.

	-Delete Sale will remove the sale from the database, this is permanent deletion.


Tools Menu--
There are two tools in the Tools Menu, these are Swap Sales and Unit LRM MBF.

	-Swap Sales will swap two sales by their auction dates.

	-Unit LRM MBF is specific to the Dept, but the premise of it is that it will proportionately scale unit MBFs up or down to 
	 acheieve the user-defined desired sale MBF.


Reports Menu--
There is one tool in the report menu, it is Trust Volume by MBF.

	-This tool is also specific for the Dept, but it will give sale data and totals within a user-defined timeframe specific to the
	 user-chosen trust. It will also allow the user to export this data to an Excel spreadsheet.





Further versions of Timber Sales...
Features to come for Timber Sales
-More Tools and Reports
-Silviculture Activity Scheduler
-Ability to Read Sale and Unit data from Shapefiles


Timber Sales is produced by Pipeline Forestry of Washington State.
To contact Pipeline.

    Email - zachbeebe@pipelineforestry.com
    Phone - 425-931-8214
    Website - pipelineforestry.com


		


