# Convolutional encoder/decoder class

The ConvolutionalCode class is defined by a list of bitstrings that indicate the tap points for the convolutional code. The number of elements in the list defines the number of output bits. For example, 
```Python
ConvolutionalCode(['1001', '1010', '1100', '1011', '1101', '1110', '1111'])
``` 
would define a rate 1/7 code, where the first output bit is tapping the input bit and the last delay, the second output bit is tapping the input bit and the 2nd delay, etc.

## Example Use

```Python
>>> from conv_enc import ConvolutionalCode as CC
>>> cc = CC(['1001', '1010', '1100', '1011', '1101', '1110', '1111'])
>>> cc.encode('10010110')
'11111110010111010101101100100010111101010001001010111100'
>>> cc.decode('11111110010111010101101100100010111101010001001010111100')
'10010110'
>>> cc.decode('00001110010111010101101100100010111101010001001010111100') # with first 4 bits flipped 
'10010110'
```


## Author
* **Steve Bremer**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
