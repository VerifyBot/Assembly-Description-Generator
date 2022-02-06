def _parse_pushes(code: str) -> list:
  """
  Collect pushes and push them to the "stack"
  :param code: assembly code to parse (lines with push)
  :return: the stack (pushes in reverse order)
  """

  stack = []
  for line in code.splitlines():
    line = line.strip()

    if len(line) == 0:
      continue
    elif line.startswith("call"):
      break
    elif line.startswith("push"):
      val = line.split('push ', 1)[1]
      stack.insert(0, val)

  return stack

def stack_state(code: str):
  """
  Generate the description of the Stack State

  # Example:
  CODE = '''
  push offset array
  push arraySize
  push offset sum
  push x
  call SumArrayPositive
  '''

  stack_state(CODE)

  # Output:
  ; --------------------------------------------------
  ; Stack State:
  ; | bp + 4 |   bp + 6   |   bp + 8  |   bp + 10    |
  ; |   x    | offset sum | arraySize | offset array |
  ; --------------------------------------------------

  :param code: assembly code to parse (lines with push)
  """

  stack = _parse_pushes(code)

  # design inspired by: https://github.com/ben9923/DOS-8086-Space-Invaders/blob/master/Print.asm#L78-L82
  EXTRA_SPACE = 1  # recommended: 1-4
  ss_bps  = "; |"
  ss_vals = "; |"
  bp = 4
  for val in stack:
    lng = max(len(val), len(f'bp + {bp}'))
    ss_bps += f'bp + {bp}'.center(lng + EXTRA_SPACE * 2) + '|'
    ss_vals += val.center(lng + EXTRA_SPACE * 2) + '|'

    bp += 2

  maxlen = max(len(ss_bps), len(ss_vals))

  # print('; ' + '-' * (maxlen - 2))
  # print("; Stack State:")
  # print(ss_bps)
  # print(ss_vals)
  # print('; ' + '-' * (maxlen - 2))

  return "\n".join([
    '; ' + '-' * (maxlen - 2),
    "; Stack State:",
    ss_bps,
    ss_vals,
    '; ' + '-' * (maxlen - 2)
  ])


# noinspection PyShadowingBuiltins
def procedure_description(description: str = None, input: str = None, output: str = None, code: str = None):
  """
  Generate the description of the procedure

  # Example:
  CODE = '''
  push offset array
  push arraySize
  push offset sum
  push x
  call SumArrayPositive
  '''

  procedure_description(
      description="sums positive values in pushed array into a variable",
      output="sum in [Sum] at DSEG",
      code=CODE
  )

  # Output:
  ; ===========================================================================
  ; Descrpt: Sums positive values in pushed array into a variable.
  ; Input  : (By order) [1] x, [2] offset sum, [3] arraySize, [4] offset array.
  ; Output : Sum in [sum] at dseg.
  ; ===========================================================================

  * All params are optional
  :param description: procedure description
  :param input: procedure input
  :param output: procedure output
  :param code: assembly code to parse (lines with push)
               the pushes read will be added to the input
  """
  
  # parse code to find pushes so we can add them to the input
  stack_input = ''
  if code:
    stack = _parse_pushes(code)
    stack_input = "(By order) "
    stack_input += ", ".join([f"[{i}] {val}" for i, val in enumerate(stack, start=1)])
    stack_input += '.\n' + ' ' * 13

  add_dot = lambda line: '.' if not line.endswith('.') else ''

  descrpt = description or 'no description'
  descrpt = descrpt.capitalize() + add_dot(descrpt)
  descrpt = f"; Descrpt: {descrpt}"

  if not input:
    if not code:
      input = 'no input'.capitalize()
    else:
      input = ''
      stack_input = stack_input.strip()

  input = "; Input  : " + stack_input + input.capitalize()
  input += add_dot(input)

  output = output or 'no output'
  output = output.capitalize() + add_dot(output)
  output = f"; Output : {output}"

  maxlen = max(len(descrpt), len(input), len(output))
  return "\n".join([
    '; ' + '=' * (maxlen - 2),
    descrpt,
    input,
    output,
    '; ' + '=' * (maxlen - 2)
  ])


if __name__ == '__main__':
  tests = dict(
    stack=False,
    proc=True
  )

  if tests['stack']:
    # GENERATE STACK DESCRIPTION FOR PROCEDURE CALL
    CODE = """
      push offset array
      push arraySize
      push offset sum
      push x
      call SumArrayPositive
      """
    c = stack_state(CODE)
    print(c)

  if tests['proc']:
    # GENERATE STACK DESCRIPTION FOR PROCEDURE CALL
    CODE = """
          push offset array
          push arraySize
          push offset sum
          push x
          call SumArrayPositive
          """

    pd = procedure_description(
      description="sums positive values in pushed array into a variable",
      output="sum in [Sum] at DSEG",
      code=CODE
    )

    print(pd)
