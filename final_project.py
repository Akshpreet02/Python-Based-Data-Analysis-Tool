# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                     #
# Course: ENDG 233                                                    #
# Name: AKSHPREET SINGH                                               #
# Group: L04-20                                                       #
# Description: Terminal-Based Data Analysis Tool                      #
# Requirements: pandas      - in `DataClass` for importing data       #
#               numpy       - in `get_insights` for data analysis     #
#               matplotlib  - in `plot_insights` for plotting charts  #
#                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""A class to import data using the pandas module containing instance functions
to convert the requested data to numpy arrays and return it
Instance Variables:
    df1 [pandas dataframe]: containing the data in the first csv
    df2 [pandas dataframe]: containing the data in the second csv
    df3 [pandas dataframe]: containing the data in the thrid csv
    common [string]: the name of the column common in the three data files
Instance Functions:
    get_selection: to get the selected data based on the primary keys provided
    get_all: to get the entire column containing all the primary keys
    get_extremes: to get the two extreme points in data based on the sizes
    get_pop_data: to get the data for plotting the population chart
    get_species_data: to get the data for plotting the species chart
"""
class DataClass:
    def __init__(self, f1, f2, f3):
        self.df1 = pd.read_csv(f1)
        self.df2 = pd.read_csv(f2)
        self.df3 = pd.read_csv(f3)
        # to identify the primary key column
        self.common = np.intersect1d(self.df3.columns, self.df2.columns)
        self.common = np.intersect1d(self.common, self.df1.columns)[0]

    """This function returns the column 'name' along with the primary key column if found in the data
    Returns:
        [tuple] : A boolean to check if the requested column was found along with the data
    """
    def get_selection(self, name):
        if name in self.df1:
            return True, np.array([self.df1[self.common], self.df1[name]])
        elif name in self.df2:
            return True, np.array([self.df2[self.common], self.df2[name]])
        elif name in self.df3:
            return True, np.array([self.df3[self.common], self.df3[name]])
        return False, []

    """Returns the entire primary key column
    """
    def get_all(self):
        return np.array(self.df1[self.common])

    def get_extremes(self, selection):
        df1_sizes = np.array([self.df1[self.common], self.df1[list(self.df1)[-1]]])
        selected_sizes = np.isin(df1_sizes[0], selection)
        max_idx = np.argmax(df1_sizes[1][selected_sizes])
        max_value = df1_sizes[0][selected_sizes][max_idx]
        min_idx = np.argmin(df1_sizes[1][selected_sizes])
        min_value = df1_sizes[0][selected_sizes][min_idx]
        if max_value != min_value:
            return [min_value, max_value]
        else:
            return [min_value]

    def get_pop_data(self, selection):
        extremes = self.get_extremes(selection)
        labels = list(self.df2)
        labels.remove(self.common)

        if len(extremes) == 1:
            values = np.array(self.df2.loc[self.df2[self.common] == extremes[0]])[0]
            temp_idx = np.argwhere(values == extremes[0])
            values = np.delete(values, temp_idx)
            return {
                "data_pointers": extremes,
                "data_values": [np.array(labels), values]
            }
        else:
            min_values = np.array(self.df2.loc[self.df2[self.common] == extremes[0]])[0]
            temp_idx = np.argwhere(min_values == extremes[0])
            min_values = np.delete(min_values, temp_idx)

            max_values = np.array(self.df2.loc[self.df2[self.common] == extremes[1]])[0]
            temp_idx = np.argwhere(max_values == extremes[1])
            max_values = np.delete(max_values, temp_idx)

            return {
                "data_pointers": extremes,
                "data_values": [np.array(labels), min_values, max_values]
            }

    def get_species_data(self, selection):
        extremes = self.get_extremes(selection)
        labels = list(self.df3)
        labels.remove(self.common)
        labels.append("Total")

        if len(extremes) == 1:
            values = np.array(self.df3.loc[self.df3[self.common] == extremes[0]])[0]
            temp_idx = np.argwhere(values == extremes[0])
            values = np.delete(values, temp_idx)
            values = np.append(values, np.sum(values))
            return {
                "data_pointers": extremes,
                "data_values": [np.array(labels), values]
            }
        else:
            min_values = np.array(self.df3.loc[self.df3[self.common] == extremes[0]])[0]
            temp_idx = np.argwhere(min_values == extremes[0])
            min_values = np.delete(min_values, temp_idx)
            min_values = np.append(min_values, np.sum(min_values))

            max_values = np.array(self.df3.loc[self.df3[self.common] == extremes[1]])[0]
            temp_idx = np.argwhere(max_values == extremes[1])
            max_values = np.delete(max_values, temp_idx)
            max_values = np.append(max_values, np.sum(max_values))

            return {
                "data_pointers": extremes,
                "data_values": [np.array(labels), min_values, max_values]
            }

"""Function to generate the two plots based on the data passed as parameters
Args:
    pop_data [dict]: Dictionary containing labels and data as numpy array
Returns:
    None
"""
def plot_insights(pop_data, species_data):
    print("\nThe program will now generate the 2 plots based on your selection...")
    
    # coolean to check if there as two data series to plot
    double_graphs = len(species_data['data_pointers']) > 1

    # Begin Plot 1 - threatened species plot
    fig, ax = plt.subplots()
    x = np.arange(len(species_data['data_values'][0]))
    width = 0.34
    ax.set_ylabel('Number of threatened species')
    if double_graphs:
        rects1 = ax.bar(x - width/2, species_data['data_values'][1], width, label=species_data['data_pointers'][0])
        rects2 = ax.bar(x + width/2, species_data['data_values'][2], width, label=species_data['data_pointers'][1])
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        ax.set_title('Threatened Species in the largest and the smallest countries', pad=20)
    else:
        rects1 = ax.bar(x, species_data['data_values'][1], width, label=species_data['data_pointers'][0])
        ax.bar_label(rects1, padding=3)
        ax.set_title('Threatened Species in the country', pad=20)
    
    ax.set_xticks(x, species_data['data_values'][0])
    ax.legend()
    fig.tight_layout()
    plt.show()

    # Begin plot 2 - Population plot
    fig = plt.figure()
    plt.plot(pop_data['data_values'][0], pop_data['data_values'][1], label=pop_data['data_pointers'][0], marker='o')
    if double_graphs:
        plt.plot(pop_data['data_values'][0], pop_data['data_values'][2], label=pop_data['data_pointers'][1], marker='o')
        plt.title("Population over the years for the largest and the smallest countries", pad=25)
    else:
        plt.title("Population over the years for the country", pad=20)
    plt.legend()
    plt.xlabel("Year")
    plt.ylabel("Population (in scientific notation)")
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    plt.show()

    print("\nData Analysis Complete! You will now return to the main menu.")

"""Function to calculate the mean, median, max, min and standard deviation
Args:
    data [array]: numpy array containing the data to calculate the insights from
    line_format [str]: string to specify the format to print table edges
    row_format [str]: string to specify the format to row data in the table
Returns:
    None
"""
def calculate_insights(data, line_format, row_format):
    print(line_format, sep='')
    print(line_format, sep='')

    # Calculate and display the minimum value
    row_data = []
    for arr in data:
        # Check if the value is not of type number
        if isinstance(arr[1][0], str):
            row_data.append("-")
        else:
            row_data.append(np.min(arr[1]))
    print(" ", row_format.format("Minimum", *row_data))

    # Calculate and display the median value
    row_data = []
    for arr in data:
        # Check if the value is not of type number
        if isinstance(arr[1][0], str):
            row_data.append("-")
        else:
            row_data.append(round(np.median(arr[1]), 5))
    print(" ", row_format.format("Median", *row_data))

    # Calculate and display the maximum value
    row_data = []
    for arr in data:
        # Check if the value is not of type number
        if isinstance(arr[1][0], str):
            row_data.append("-")
        else:
            row_data.append(np.max(arr[1]))
    print(" ", row_format.format("Maximum", *row_data))

    # Calculate and display the mean value
    row_data = []
    for arr in data:
        # Check if the value is not of type number
        if isinstance(arr[1][0], str):
            row_data.append("-")
        else:
            row_data.append(round(np.mean(arr[1]), 5))
    print(" ", row_format.format("Mean", *row_data))

    # Calculate and display the standard deviation
    row_data = []
    for arr in data:
        # Check if the value is not of type number
        if isinstance(arr[1][0], str):
            row_data.append("-")
        else:
            row_data.append(round(np.std(arr[1]), 5))
    print(" ", row_format.format("σ (S.D.)", *row_data))

    print(line_format, sep='')

"""Function to select the data based on the columns requested by the user, display it and
invoke the functions to calculate and plot the insights.
Args:
    col_name [str]: The column from which the data will be selected
    comp_type [int]: To check the type of selection (based on user input or all data)
    comp_val [str|int]: The value matching which the data will be selected
    operands [list]: List containing the columns containing the data to be fetched
Returns:
    None
"""
def get_insights(col_name, comp_type, comp_val, operands):
    data = DataClass('Country_Data.csv', 'Population_Data.csv', 'Threatened_Species.csv')
    selected_rows = []
    fetched_data = []
    valid_operands = []

    # If the selection is to be made based on a value, fetch those entries
    if comp_type == 1:
        flag, selection = data.get_selection(col_name)
        if flag:
            selected_idx = []
            selected_idx = np.where(selection[1] == comp_val)
            selected_rows = selection[0][selected_idx]
        else:
            print(f"The selected column '{col_name}' was not found. Selecting all data.")
            col_name = data.common
            selected_rows = data.get_all()
    # else fetch all the data entries
    else:
        col_name = data.common
        selected_rows = data.get_all()

    # Loop thorugh the columns requested and fetch the data in each of them
    for operand in operands:
        flag, selection = data.get_selection(operand)
        if flag:
            fetch_idx = np.isin(selection[0], selected_rows)
            fetched_data.append(np.array([selection[0][fetch_idx], selection[1][fetch_idx]]))
            valid_operands.append(operand)
        else:
            print(f"The requested column '{operand}' was not found in the given data.")

    # For each of the columns found in the data, calculate insights and display them
    if len(valid_operands) > 0:
        table_line = " "*14 + " +" + "-" * (20 * len(valid_operands) - 1) + "+"
        table_row = "   {:<10}|" + " {:<17} |" * len(valid_operands)

        print("\n", table_line, sep='')
        print(" ", table_row.format("Data -->", *valid_operands))
        print(table_line, sep='')

        for selected_row in selected_rows:
            row_data = []
            for arr in fetched_data:
                row_data.append(arr[1][np.where(arr[0] == selected_row)][0])
            print(" ", table_row.format(' ', *row_data))

        # exit if no matching rows are found
        if not len(fetched_data[0][1]):
            print("No matching rows found!")
            return

        calculate_insights(fetched_data, table_line, table_row)

        population_data = data.get_pop_data(fetched_data[0][0])
        species_data = data.get_species_data(fetched_data[0][0])
        plot_insights(population_data, species_data)
    else:
        print("All columns requested are Invalid! Please try again.")

# The main function
def main():
    # Print the welcome message
    print("\n", "*" * 58, sep='')
    print("*", ' '*25, "WELCOME", ' '*24, "*", sep='')
    print("*" * 58 ,sep='')
    print("Instructions:\n")
    print("- This is a python based data analysis tool. We have data with respect to the population and the threatened species in countries all around the world.")
    print("- You may search through the data based on any data column, for example you may want to select all countries in Asia, for that user inputs 'Asia' first then he puts the column heading name. In this case, user inputs 'UN Region' .Or you may select all the entries.")
    print("- Once the selection is made, the application will prompt you to enter the columns of which you'd like to fetch the data, you may enter, 'Country, Sq Km' to fetch the Country name and Size in Sq. Kms for the countries matching your search term in the previous step.")
    print("- The application will then fetch the data in the requested columns corresponding to the selection made (in this example, the countries in the region Asia).")
    print("- For all numerical entries, the maximum, median, minimum, mean and standard deviation will be calculated and displayed as output along with the columns requested.")
    print("- Post this, the largest and the smallest countries from your selection will be selected and a plot of the population through the years as well as a plot of the threatened species in the country will be generated and shown as output.")
    header = ""
    selection_value = ""
    insights = ""
    selection_type = -1
    # Loop to display the menu until explicitly exited by the user
    while True:
        print("\nEnter 1 if you want to search for some particular data using a search value.")
        print("Enter 2 if you would like to select all the entries in the data.")
        print("Enter 0 to exit the program.")
        try:
            selection_type = int(input("Your selection: "))
        except:
            print("Invalid Input!")
            continue
        if not 0 <= selection_type <= 2:
            print("Invalid Input!")
            continue
        if selection_type == 0:
            raise SystemExit
        elif selection_type == 1:
            selection_value = input("Enter the search term you want to search for in the data: ")
            header = input("\nEnter the name of the column that you want to select data from: ")
        # If the value is a number, perform the conversion, else pass
        try:
            selection_value = int(selection_value)
        except:
            pass
        insights = input("Enter the data columns you want to fetch for stats calculation (comma-separated): ")
        # Store the column names as a list
        result = [x.strip() for x in insights.split(',') if x != '']
        # Call the function to calculate and display the requested data
        get_insights(header, selection_type, selection_value, result)

if __name__=="__main__":
    main()