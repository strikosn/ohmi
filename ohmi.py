import numpy
import pint
import quantulum3.parser
import readline
import sys


def input_error(results):
  print('2 units expected. %d units parsed: %s' % (len(results), repr(results)))


def evaluate(line):
  results = quantulum3.parser.parse(line)

  if len(results) != 2:
    input_error(results)
    return

  results.sort(key=lambda r: r.unit.entity.name)
  ureg = pint.UnitRegistry()

  if (results[0].unit.entity.name == 'current' and
      results[1].unit.entity.name == 'electric potential'):
    current = results[0].value * ureg(results[0].unit.name)
    voltage = results[1].value * ureg(results[1].unit.name)
    power = (current * voltage).to('W')
    resistance = (voltage / current).to('Ω')

  elif (results[0].unit.entity.name == 'current' and
        results[1].unit.entity.name == 'electrical resistance'):
    current = results[0].value * ureg(results[0].unit.name)
    resistance = results[1].value * ureg(results[1].unit.name)
    voltage = (current * resistance).to('V')
    power = (current * voltage).to('W')

  elif (results[0].unit.entity.name == 'current' and
        results[1].unit.entity.name == 'power'):
    current = results[0].value * ureg(results[0].unit.name)
    power = results[1].value * ureg(results[1].unit.name)
    voltage = (power / current).to('V')
    resistance = (voltage / current).to('Ω')

  elif (results[0].unit.entity.name == 'electric potential' and
        results[1].unit.entity.name == 'electrical resistance'):
    voltage = results[0].value * ureg(results[0].unit.name)
    resistance = results[1].value * ureg(results[1].unit.name)
    current = (voltage / resistance).to('A')
    power = (voltage * current).to('W')

  elif (results[0].unit.entity.name == 'electric potential' and
        results[1].unit.entity.name == 'power'):
    voltage = results[0].value * ureg(results[0].unit.name)
    power = results[1].value * ureg(results[1].unit.name)
    current = (power / voltage).to('A')
    resistance = (voltage / current).to('Ω')

  elif (results[0].unit.entity.name == 'electrical resistance' and
        results[1].unit.entity.name == 'power'):
    resistance = results[0].value * ureg(results[0].unit.name)
    power = results[1].value * ureg(results[1].unit.name)
    current = numpy.sqrt(power / resistance).to('A')
    voltage = (power / current).to('V')

  else:
    print_error(results)
    return

  print('{:.3g~P}  {:.3g~P}  {:.3g~P}  {:.3g~P}'.format(
      voltage.to_compact(), current.to_compact(), power.to_compact(),
      resistance.to_compact()))


def main():
  while True:
    try:
      evaluate(input('>> '))
    except EOFError:
      break


if __name__ == '__main__':
  main()
