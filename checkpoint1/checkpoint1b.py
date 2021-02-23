import pandas as pd
import re


def remove_percents(df, col):
    column = list(df[col]) 
    new_col = []
    for element in column:
        if type(element)== float:
            new_col.append(element)
            continue
        new_col.append(float(element.split("%")[0]))
        
    new_series = pd.Series(new_col)
    df[col] = new_series
    return df


def fill_zero_iron(df):
    df['Iron (% DV)'] = df['Iron (% DV)'].fillna(0)
    return df
    

def fix_caffeine(df):
    
    coffee = list(df["Caffeine (mg)"])
    add = 0
    count = 0
    for element in coffee:
        if type(element) == float : continue
        if element == 'Varies' or element == 'varies': continue
        add = int(element)+add
        count = count+1
        
    average = add/count
    for i in range(len(coffee)):
        if type(coffee[i]) == float : coffee[i] = average
        if coffee[i] == 'Varies' or coffee[i] == 'varies': coffee[i] = average
    
    coff_series = pd.Series(coffee)
    df["Caffeine (mg)"] = coff_series
    return df


def standardize_names(df):
    col_names = list(df.columns)
    for i in range (len(col_names)):
        col_names[i] = col_names[i].lower()
        col_names[i] = col_names[i].split("(")[0]
    df.columns = pd.Series(col_names)
    return df



def fix_strings(df, col):
    string_list = list(df[col])
    new_col = []
    for string in string_list:
        string = string.lower()
        for char in string:
            if (re.search("[a-z ]", char)) : continue
            string = string.replace(char, "")
        new_col.append(string)
        
    df[col] = pd.Series(new_col)
    
    return df



def main():
    
    # first, read in the raw data
    df = pd.read_csv('../data/starbucks.csv')
    
    # the columns below represent percent daily value and are stored as strings with a percent sign, e.g. '0%'
    # complete the remove_percents function to remove the percent symbol and convert the columns to a numeric type
    pct_DV = ['Vitamin A (% DV)', 'Vitamin C (% DV)', 'Calcium (% DV)', 'Iron (% DV)']
    for col in pct_DV:
        df = remove_percents(df, col)
        
    # the column 'Iron (% DV)' has missing values when the drink has no iron
    # complete the fill_zero_iron function to fix this
    df = fill_zero_iron(df)
        
    # the column 'Caffeine (mg)' has some missing values and some 'varies' values
    # complete the fix_caffeine function to deal with these values
    # note: you may choose to fill in the values with the mean/median, or drop those values, etc.
    df = fix_caffeine(df)
    
    
    # the columns below are string columns... starbucks being starbucks there are some fancy characters and symbols in their names
    # complete the fix_strings function to convert these strings to lowercase and remove non-alphabet characters
    names = ['Beverage_category', 'Beverage']
    for col in names:
        df = fix_strings(df, col)
        
    # the column names in this data are clear but inconsistent
    # complete the standardize_names function to convert all column names to lower case and remove the units (in parentheses)
    df = standardize_names(df)
    
    # now that the data is all clean, save your output to the `data` folder as 'starbucks_clean.csv'
    # you will use this file in checkpoint 2
    
    df.to_csv(r'../data/starbucks_clean.csv',index = False)
    
if __name__ == "__main__":
    main()