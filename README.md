# Pycafe
A project that emulates **javap** in python. Reads a compiled java class file's bytecode

Named **Pycafe** after a java class file's first 4 'magic' bytes : [**'ca'**, **'fe**', **'ba'**, **'be'**]

## Goals
### Implement all pool constants
- [x] Utf8
- [x] Integer
- [x] Float
- [x] Long
- [x] Double
- [x] Class reference
- [x] String reference
- [x] Field reference
- [x] Method reference
- [ ] Interface method reference
- [x] Name and type descriptor
- [ ] Method handle
- [ ] Method type
- [ ] Dynamic
- [ ] InvokeDynamic
- [ ] Module 
- [ ] Package

### Implement critical attributes
- [ ] ConstantValue
- [x] Code
- [ ] StackMapTable
- [ ] Exceptions
- [ ] BootstrapMethods

## Demos
### Pycafe (Left) and Javap (Right)
![Demo](https://github.com/chasekov/Pycafe/blob/master/imgs/demo.png)
