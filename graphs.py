import matplotlib.pyplot as plt

class Graph:
    """
    The class responsablile for generating the required graphs
    The structure will be graph.{graph_type_name}(data) -> will return a fig
    """
    def __init__(self):
        self.fig, self.ax = plt.subplots()


    def line_plot(self, dates, values):
        """Generates a line graph based on the dates and the values"""
        self.ax.plot(dates, values)
        self.ax.set_title("Value Over Time")
        self.ax.set_xlabel("Label")
        self.ax.set_ylabel("Value")
        return self.fig


    def scatter_plot(self, dates, values):
        """Generates a scatter graph based on the dates and the values"""
        self.ax.scatter(dates, values)
        self.ax.set_title("Value Over Time")
        self.ax.set_xlabel("Label")
        self.ax.set_ylabel("Value")
        return self.fig
    

    def bar_plot(self, categories, expenses):
        """Generates a bar graph based on a list of categories and expenses"""
        self.ax.bar(categories, expenses)
        self.ax.set_title("Monthly Expenses")
        self.ax.set_xlabel("Label")
        self.ax.set_ylabel("Value")
        return self.fig


    def pie_chart(self, categories, values):
        """Generates a pie chart based on a list of categories and values"""
        self.ax.pie(values, labels=categories, autopct='%1.1f%%')
        self.ax.set_title("Finance Allocation")
        return self.fig



    def stack_plot(self, dates, savings, expenses, income):
        """
        Generates a stack graph based on the dates, savings, expenses and income.
        It will show the relation between the 3.
        """
        self.ax.fill_between(dates, savings, label='Savings')
        self.ax.fill_between(dates, expenses, label='Expenses', alpha=0.6)
        self.ax.fill_between(dates, income, label='Income', alpha=0.3)
        self.ax.set_title("Financial Growth Over Time")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Value")
        self.ax.legend(loc="upper left")
        return self.fig