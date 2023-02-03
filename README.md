# Assembly-Description-Generator
Simple Python program to automatically create pretty descriptions for:

## Stack State
_Example Input_:
```asm
push offset array
push arraySize
push offset sum
push x
call SumArrayPositive
```
_Example Output_:
```asm
; --------------------------------------------------
; Stack State:
; | bp + 4 |   bp + 6   |   bp + 8  |   bp + 10    |
; |   x    | offset sum | arraySize | offset array |
; --------------------------------------------------
```

## Procedure
_Example Input_:
- sums positive values in pushed array into a variable 
- sum in [Sum] at DSEG
```asm
push offset array
push arraySize
push offset sum
push x
call SumArrayPositive
```
_Example Output_:
```asm
; ===========================================================================
; Descrpt: Sums positive values in pushed array into a variable.
; Input  : (By order) [1] x, [2] offset sum, [3] arraySize, [4] offset array.
; Output : Sum in [sum] at dseg.
; ===========================================================================
```

# Usage
The few features mentioned above are supported as functions:
## Stack
```py
>>> CODE = """
  push offset array
  push arraySize
  push offset sum
  push x
  call SumArrayPositive
  """
>>> ss = stack_state(code)
>>> ss
; --------------------------------------------------
; Stack State:
; | bp + 4 |   bp + 6   |   bp + 8  |   bp + 10    |
; |   x    | offset sum | arraySize | offset array |
; --------------------------------------------------
```

## Procedure
```py
>>> CODE = """
  push offset array
  push arraySize
  push offset sum
  push x
  call SumArrayPositive
  """
>>> pd = procedure_description(
      description="sums positive values in pushed array into a variable",
      output="sum in [Sum] at DSEG",
      code=CODE
    )
>>> pd
; ===========================================================================
; Descrpt: Sums positive values in pushed array into a variable.
; Input  : (By order) [1] x, [2] offset sum, [3] arraySize, [4] offset array.
; Output : Sum in [sum] at dseg.
; ===========================================================================
```



Enjoy! 😎
