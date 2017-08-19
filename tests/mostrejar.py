from Core.Sampling import sampling
"""
Contingut de les imatges amb cieLAB:

Valors python
8-bit images: L <-- L∗255/100,a <-- a+128,b <-- b+128

Valors reals
L --> 0 - 100
a --> -127 a 127
b --> -127 a 127
estudiar si donaria informacio convertirlos als valors reals
"""


if __name__ == "__main__":

    file_metadata = 'results/values/metadata.xml'
    file_data = 'results/Data/data.xml'
    datasets = ["datasets/mostreig"]

    sampling(datasets, file_metadata, file_data)