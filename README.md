## Drunken Bishop Algorithm CLI

The [Drunken Bishop Algorithm](https://codegolf.stackexchange.com/questions/59670/the-drunken-bishop) was developed by Alexander von Gernler to create an ASCII representation given a string of hexidecimal digits known as a fingerprint. Most notably, OpenSSH uses this method to make differentiating fingerprints visually easier.

### Examples

Use `python3 drunk.py -h` to display the help menu.

#### Using a Provided Key

Ensure the key is a 16 octet string of hex values.

``

```
python3 drunk.py -k 37:e4:6a:2d:48:38:1a:0a:f3:72:6d:d9:17:6b:bd:5e

Fingerprint:
37:e4:6a:2d:48:38:1a:0a:f3:72:6d:d9:17:6b:bd:5e
+-----------------+
|                 |
|                 |
|          .      |
|     .   o       |
|o . o . S +      |
|.+ + = . B .     |
|o + + o B o E    |
| o .   + . o     |
|         .o      |
+-----------------+
```

#### Using a Random Key

```
python3 drunk.py -r

Fingerprint:
b4:bb:ed:62:0a:75:d1:a6:eb:09:bf:9d:8b:b7:ee:c3
+-----------------+
|                 |
|         .       |
|        o o      |
|       . =       |
|      . S        |
|     . . o       |
|    . . o.       |
|     . +o*E.     |
|      .oBBX+     |
+-----------------+
```

#### Demo

Repl demo link coming soon.
