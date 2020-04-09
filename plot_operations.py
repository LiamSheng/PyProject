"""
Create a plot_operations.py module with a PlotOperations class inside.
• Use the Python matplotlib to create a basic boxplot:
◦ https://matplotlib.org/examples/pylab_examples/boxplot_demo.html
"""
import matplotlib.pyplot as plt


class PlotOperations:
    """
    Be creative. One way is a dictionary of lists. For example:
    • weather_data = {1: [1.1, 5.5, 6.2, 7.1], 2: [8.1, 5.4, 9.6, 4.7]}
    • The dictionary key is the month: January = 1, February = 2 etc...
    • The data is all the mean temperatures for each day of that month.
    """

    def diplay_box_plot(self, my_list, from_year, to_year):
        """
        A boxplot displaying one box per month, so it shows all
        12 months of the year on one plot.
        """
        title = 'Monthly Temperature Distribution for: ' + str(from_year) + ' to ' + str(to_year)
        loc = 'center'
        font_dict = {'fontsize': 14, 'fontweight': 8.2, 'verticalalignment': 'baseline', 'horizontalalignment': loc}
        plt.title(title, fontdict=font_dict, loc=loc)
        plt.ylabel('Temperature (Celsius)')
        plt.xlabel('Month')
        mean_value = []
        try:
            for key, values in my_list.items():
                try:
                    mean_value.append(values)
                    plt.boxplot(mean_value)
                except Exception as e:
                    print("Error in reading key & values in my_list.items():", e)
            try:
                plt.show()
            except Exception as e:
                print("An exception occurred while parsing the key-value pair", e)
        except Exception as e:
            print("An exception occurred while parsing my_list.items()", e)

