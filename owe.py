import pandas

df = pandas.read_excel("files\OWE_Nov_21.xlsx", sheet_name="PU Wise OWE", header=2, skiprows=lambda x: x in [14, 26])
print (df.shape)