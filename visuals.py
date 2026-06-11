#This file contains the python code for file validation and chart generation  
import pandas as pd
import os
import time # used to rename the charts being downloaded to avoid overwriting 
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
class visuals:
    def analysis(self, file):  #function to check the correct file format
        try:
            if file.filename.endswith((".xlsx", ".xls")):
                df = pd.read_excel(file)
                return df
            else:
                return None
        except:
            return None
    def line_chart(self, df, x_col, y_col, title=""): # function to generate line chart
        plt.close()
        plt.figure()
        plt.plot(df[x_col], df[y_col])
        plt.title(title)
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.grid(True)
        filename = f"chart_{int(time.time())}.png" # timestamp is used to avoid overwriting
        filepath = os.path.join("static", filename)
        plt.savefig(filepath)
        plt.close()
        return filename
    def bar_chart(self, df, x_col, y_col, title=""): # function to generate bar chart
        plt.close()
        plt.figure()
        plt.bar(df[x_col], df[y_col])
        plt.title(title)
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        filename = f"chart_{int(time.time())}.png"# timestamp is used to avoid overwriting
        filepath = os.path.join("static", filename)
        plt.savefig(filepath)
        plt.close()
        return filename
    def histogram(self, df, x_col, title=""): # function to generate histogram
        plt.close()
        plt.figure()
        plt.hist(df[x_col])
        plt.title(title)
        plt.xlabel(x_col)
        filename = f"chart_{int(time.time())}.png"# timestamp is used to avoid overwriting
        filepath = os.path.join("static", filename)
        plt.savefig(filepath)
        plt.close()
        return filename
    def pie_chart(self, df, x_col, y_col, title=""): # function to generate pie chart
        try:
            plt.close()
            plt.figure(figsize=(6,6))
            values = pd.to_numeric(df[y_col], errors="coerce")
            labels = df[x_col]
            data = pd.DataFrame({
                "labels": labels,
                "values": values
            }).dropna()
            # remove invalid labels
            data = data[data["labels"] != ""]
            # prevent crash
            if data.empty or data["values"].sum() == 0:
                return None
            # limit for better display
            data = data.head(6)
            plt.pie(
                data["values"],
                labels=data["labels"],
                autopct='%1.1f%%',
                startangle=90
            )
            plt.axis("equal")
            plt.title(title)
            filename = f"chart_{int(time.time())}.png"# timestamp is used to avoid overwriting
            filepath = os.path.join("static", filename)
            plt.savefig(filepath)
            plt.close()
            return filename
        except Exception as e:
            print("Error:", e)
            return None
    def scatter_chart(self, df, x_col, y_col, title=""): #function to generate scatter plot
        plt.close()
        plt.figure()
        plt.scatter(df[x_col], df[y_col])
        plt.title(title)
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.grid(True)
        filename = f"chart_{int(time.time())}.png"# timestamp is used to avoid overwriting
        filepath = os.path.join("static", filename)
        plt.savefig(filepath)
        plt.close()
        return filename


    