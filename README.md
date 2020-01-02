# Convolutional encoder/decoder class

The ConvolutionalCode class is defined by a list of bitstrings that indicate the tap points for the convolutional code. The number of elements in the list defines the number of output bits. For example, 
```Python
ConvolutionalCode(['1001', '1010', '1100', '1011', '1101', '1110', '1111'])
``` 
would define a rate 1/7 code, where the first output bit is tapping the input bit and the last delay, the second output bit is tapping the input bit and the 2nd delay, etc.

## Author
* **Steve Bremer**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
