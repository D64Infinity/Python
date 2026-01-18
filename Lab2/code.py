import re

class PascalToPythonTranslator:
    def __init__(self):
        self.python_code = ""

    def translate(self, pascal_code):
        lines = pascal_code.splitlines()
        py_lines = []

        indent = 0
        skip_var_block = False
        save_else_indent = False
        prev_row_was_else = False
        prev_row_was_if = False
        prev_row_was_cycle = False

        for line in lines:
            line = line.strip()

            # empty line proccessing
            if not line:
                if len(py_lines) > 0 and py_lines[-1] != "":
                    py_lines.append("")
                continue

            # var block skip
            if line.lower().startswith("var"):
                skip_var_block = True
                continue
            if skip_var_block:
                if line.lower() == "begin":
                    skip_var_block = False
                else:
                    continue  

            # procedure / function keywords proccessing
            proc_match = re.match(r'(procedure|function)\s+(\w+)', line, re.I)
            if proc_match:
                name = proc_match.group(2)
                py_lines.append(" " * (indent*4) + f"def {name}():")
                indent += 1
                continue
            
            # begin / end keywords proccessing
            if line.lower() == "begin":
                prev_row_was_else = False
                prev_row_was_if = False
                prev_row_was_cycle = False
                continue
            if line.lower().startswith("end"):
                indent -= 1
                save_else_indent = True
                continue

            # comments proccessing
            line = re.sub(r'{(.*?)}', r'# \1', line)

            # print proccessing
            line = re.sub(r'writeln\((.*)\)\s*;?', r'print(\1)', line, flags=re.I)

            # bool values proccessing
            line = re.sub(r'true', 'True', line)
            line = re.sub(r'false', 'False', line)

            # div / mod keywords proccessing
            line = re.sub(r' mod ', ' % ', line) 
            line = re.sub(r' div ', ' // ', line)  

            # is equal operator processing
            line = re.sub(r'\s=\s', ' == ', line)

            # for-loop proccessing
            match_for = re.match(r'for\s+(\w+)\s*:=\s*(.+?)\s+to\s+(.+?)\s+do', line, re.I)
            if match_for:
                var, start, end = match_for.groups()
                py_lines.append(" " * (indent*4) + f"for {var} in range({start}, {end}+1):")
                indent += 1
                prev_row_was_cycle = True
                continue
            
            # while-loop proccessing
            match_while = re.match(r'while (.+) do', line, re.I)
            if match_while:
                condition = match_while.group(1)
                py_lines.append(" " * (indent*4) + f"while {condition}:")
                indent += 1
                prev_row_was_cycle = True
                continue

            # if-else proccessing
            if_match = re.match(r'if (.+) then', line, re.I)
            else_match = re.match(r'else', line, re.I)

            if if_match:
                py_lines.append(" " * (indent*4) + f"if {if_match.group(1)}:")
                indent += 1
                prev_row_was_if = True
                continue
            if else_match:
                if save_else_indent:
                    indent += 1
                indent -= 1
                py_lines.append(" " * (indent*4) + "else:")
                indent += 1
                prev_row_was_else = True
                continue   

            # assignment operator procesing
            line = re.sub(r':=', '=', line)      

            py_lines.append(" " * (indent*4) + line)

            save_else_indent = False
            if prev_row_was_else:
                indent -= 1
                prev_row_was_else = False
            elif prev_row_was_if:
                indent -= 1
                prev_row_was_if = False
                save_else_indent = True
            elif prev_row_was_cycle:
                indent -= 1
                prev_row_was_cycle = False


        self.python_code += "\n".join(py_lines) + "\n\n"

# Pascal procedure 1 (factorial + buffs)
factorial_pascal = """
procedure FactorialFoo;

var
  i, j, fact, n, sumSteps: integer;
  sumFactorials: integer;
  maxFactorial: integer;
  minFactorial: integer;
  averageFactorial: real;

begin
  n := 10;
  sumFactorials := 0;
  maxFactorial := 0;
  minFactorial := 0;

  writeln('Computing factorials from 1 to ', n);
  writeln('--------------------------------');

  for i := 1 to n do
  begin
    fact := 1;
    sumSteps := 0;
    writeln('Factorial of ', i, ':');

    for j := 1 to i do
    begin
      fact := fact * j;
      sumSteps := sumSteps + fact;
      writeln(' Step ', j, ': factorial = ', fact, ', sum of steps = ', sumSteps);

      if fact mod 2 = 0 then
        writeln('  Even factorial')
      else
        writeln('  Odd factorial');
    end;

    sumFactorials := sumFactorials + fact;

    if i = 1 then
      minFactorial := fact;

    if fact > maxFactorial then
      maxFactorial := fact;

    if fact < minFactorial then
      minFactorial := fact;

    if i mod 2 = 0 then
      writeln('Finished even factorial for i=', i)
    else 
      writeln('Finished odd factorial for i=', i);

    writeln('  Square of factorial: ', fact*fact);
    writeln('  Cube of factorial: ', fact*fact*fact);
    writeln('  i*i = ', i*i, ', i*i*i = ', i*i*i);
    writeln('  i + fact = ', i+fact, ', fact - i = ', fact-i);
    writeln('  sumSteps mod 3 = ', sumSteps mod 3);
    writeln('  sumSteps div 5 = ', sumSteps div 5);
    writeln('  -------------------------');
  end;

  if n > 0 then
    averageFactorial := sumFactorials / n
  else
    averageFactorial := 0;

  writeln('Summary statistics:');
  writeln('  Sum of all factorials: ', sumFactorials);
  writeln('  Maximum factorial: ', maxFactorial);
  writeln('  Minimum factorial: ', minFactorial);
  writeln('  Average factorial value: ', averageFactorial);

  if sumFactorials mod 2 = 0 then
    writeln('Total sum of factorials is even')
  else
    writeln('Total sum of factorials is odd');

  writeln('Execution completed.');
end;
"""
# Pascal procedure 2 (sum)
sum_pascal = """
procedure SumFoo;

var
  i, j, sum, n: integer;
  square, cube: integer;
  fact: integer;
  sumSquares: integer;
  sumCubes: integer;
  evenCount: integer;
  oddCount: integer;
  average: real;

begin
  n := 20;
  sum := 0;
  sumSquares := 0;
  sumCubes := 0;
  evenCount := 0;
  oddCount := 0;

  writeln('Summing numbers from 1 to ', n);
  writeln('----------------------------');

  for i := 1 to n do
  begin
    sum := sum + i;
    square := i * i;
    cube := i * i * i;
    sumSquares := sumSquares + square;
    sumCubes := sumCubes + cube;

    writeln('Number: ', i, ', sum so far: ', sum);
    writeln('  Square: ', square, ', Cube: ', cube);

    if i mod 2 = 0 then
    begin
      evenCount := evenCount + 1;
      writeln('  Even number');
    end
    else
    begin
      oddCount := oddCount + 1;
      writeln('  Odd number');
    end;

    if i mod 3 = 0 then
      writeln('   Divisible by 3');

    if i mod 5 = 0 then
      writeln('   Divisible by 5');

    if i mod 7 = 0 then
      writeln('   Divisible by 7');

    writeln('   i + sum = ', i + sum, ', sum - i = ', sum - i);
    writeln('   i * sum = ', i * sum);
    writeln('   -------------------------');
  end;

  if n > 0 then
    average := sum / n
  else
    average := 0;

  writeln('Summary statistics:');
  writeln('  Total sum: ', sum);
  writeln('  Sum of squares: ', sumSquares);
  writeln('  Sum of cubes: ', sumCubes);
  writeln('  Average value: ', average);
  writeln('  Even numbers count: ', evenCount);
  writeln('  Odd numbers count: ', oddCount);

  writeln('Computing extra factorials:');

  for i := 1 to 5 do
  begin
    fact := 1;

    for j := 1 to i do
      fact := fact * j;

    writeln('  Factorial of ', i, ' = ', fact);
  end;

  writeln('Execution completed.');
end;
"""
# Pascal procedure 3 (prime nums)
primes_pascal = """
procedure PrimesFoo;

var
  i, j, countPrimes: integer;
  sumPrimes: integer;
  maxPrime: integer;
  isPrime: boolean;
  divisorCount: integer;
  averagePrime: real;

begin
  countPrimes := 0;
  sumPrimes := 0;
  maxPrime := 0;

  writeln('Listing prime numbers from 2 to 50');
  writeln('----------------------------------');

  for i := 2 to 50 do
  begin
    isPrime := true;
    divisorCount := 0;

    for j := 2 to i-1 do
    begin
      if i mod j = 0 then
      begin
        isPrime := false;
        divisorCount := divisorCount + 1;
        writeln(i, ' is divisible by ', j);
      end;
    end;

    if isPrime then
    begin
      writeln(i, ' is prime');
      countPrimes := countPrimes + 1;
      sumPrimes := sumPrimes + i;
      maxPrime := i;
    end
    else
      writeln(i, ' is not prime');

    writeln('  divisor count = ', divisorCount);
    writeln('  i squared = ', i*i, ', i cubed = ', i*i*i);
    writeln('  i mod 2 = ', i mod 2, ', i mod 3 = ', i mod 3);
    writeln('  -------------------------');
  end;

  if countPrimes > 0 then
    averagePrime := sumPrimes / countPrimes
  else
    averagePrime := 0;

  writeln('Total prime numbers found: ', countPrimes);
  writeln('Sum of prime numbers: ', sumPrimes);
  writeln('Maximum prime number: ', maxPrime);
  writeln('Average prime value: ', averagePrime);

  if countPrimes mod 2 = 0 then
    writeln('The count of primes is even')
  else
    writeln('The count of primes is odd');

  writeln('Execution completed.');
end;
"""

# translator for 3 procedures
translator = PascalToPythonTranslator()
translator.translate(factorial_pascal)
translator.translate(sum_pascal)
translator.translate(primes_pascal)

# writing in "translated.py"
with open("translated.py", "w", encoding="utf-8") as f:
    f.write(translator.python_code)

print("Successful")