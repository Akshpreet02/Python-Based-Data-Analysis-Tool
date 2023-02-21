# Python-Based-Data-Analysis-Tool
This project comprises a terminal-based data analysis tool that leverages the numpy python module to perform basic data manipulation operations. It has the following features:

• Data selection (i.e., filtering and searching)

• Statistical Calculations (Minimum, Median, Maximum, Mean & Standard Deviation)

• Plotting charts based on selected data The working of the application is as follows:

- Data Selection
❖ We first import the data stored in csv files into pandas data frames.

❖ The user is then prompted to either select all the data rows or provide a value and a column name to search for the matching entries. This search is performed using the ‘where’ method of the numpy library.

❖ The user is then asked to input the column names they would like to fetch and analyze as a comma separated list which we iterate through and store the required data into numpy arrays. These arrays are then matched with the selection in the previous step using the ‘isin’ method of the numpy library.

❖ Once we have the filtered data, it is displayed on screen using ‘print’ statements.

- Statistical Calculation

❖ The selected data is now subjected to calculations through the built-in ‘mean’, ‘max’, ‘min’, ‘med’, and ‘std’ functions of the numpy library.

❖ The columns that have strings as values are left out in this calculation and the result is displayed directly beneath each column.

- Generating Plots

❖ To generate plots, the matplotlib library is used.

❖ We first find out the smallest and the largest countries in the selection based on the ‘Sq Km’ column in the data.

Note: This column name is not hard-coded, but the last column in the Country_Data.csv file is picked by the program.

❖ These two extreme points are then taken as pivot points to fetch the population for each year as well as the number of threatened species, i.e., the row corresponding to these entries in each of the other two csv files is picked and stored as numpy arrays.

❖ Finally, this data is plotted using matplotlib and show to the user as output one by one.

